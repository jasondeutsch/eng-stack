// Bounded request construction and validation. Optional admission policy maps
// validated answers to outcomes; Factory owns the configured workflow routes.
import { validateTask } from '../../skills/task-intake/scripts/task.mjs';
import { readFile, stat, open } from 'node:fs/promises';
import { isAbsolute } from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const defaultsURL = new URL('./config.json', import.meta.url);
const questionsURL = new URL('./questions.json', import.meta.url);
const probability = value => typeof value === 'number' && Number.isFinite(value) && value >= 0 && value <= 1;
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const integer = value => Number.isSafeInteger(value) && value >= 0;

export async function configuration(overrides = {}) {
  if (!object(overrides)) throw new Error('Package settings must be a JSON object');
  const defaults = JSON.parse(await readFile(defaultsURL, 'utf8'));
  for (const key of Object.keys(overrides)) {
    if (!Object.hasOwn(defaults, key)) throw new Error(`Unknown task-readiness setting: ${key}`);
  }
  const config = { ...defaults, ...overrides };
  if (config.provider !== 'openrouter') throw new Error('task-readiness currently supports provider openrouter only');
  if (typeof config.model !== 'string' || !config.model.trim()) throw new Error('A model ID is required');
  if (typeof config.api_key_env !== 'string' || !/^[A-Za-z_][A-Za-z0-9_]*$/.test(config.api_key_env)) throw new Error('api_key_env must name an environment variable');
  if (typeof config.endpoint !== 'string') throw new Error('endpoint must be a URL string');
  const endpoint = new URL(config.endpoint);
  if (endpoint.username || endpoint.password || endpoint.search || endpoint.hash) throw new Error('Endpoint must not contain credentials, query parameters or fragments');
  if (endpoint.protocol !== 'https:' && !(endpoint.protocol === 'http:' && ['localhost', '127.0.0.1', '[::1]'].includes(endpoint.hostname))) {
    throw new Error('Endpoint must use HTTPS, or loopback HTTP for local testing');
  }
  for (const name of ['timeout_ms', 'max_request_bytes', 'max_response_bytes']) {
    const limit = name === 'timeout_ms' ? 120000 : 24000;
    if (!integer(config[name]) || config[name] < 1 || config[name] > limit) throw new Error(`${name} must be between 1 and ${limit}`);
  }
  if (config.admission !== null) {
    const policy = config.admission;
    if (!object(policy) || Object.keys(policy).some(key => key !== 'minimum_probability') || !probability(policy.minimum_probability)) {
      throw new Error('admission must be null or an object with minimum_probability between 0 and 1');
    }
  }
  return config;
}

export async function buildRequest(task, config, typedTask) {
  if (!object(task) || typeof task.brief !== 'string' || (task.documents != null && !Array.isArray(task.documents))) {
    throw new Error('task must be the execution input binding: brief and captured documents');
  }
  if (typedTask !== undefined) await validateTask(typedTask, task);
  // Check before reading files; large tasks are rejected explicitly, never truncated.
  if (Buffer.byteLength(task.brief) > config.max_request_bytes) throw new Error('Task exceeds the configured request byte limit');
  const documents = [];
  let documentBytes = Buffer.byteLength(task.brief);
  for (const document of task.documents ?? []) {
    if (!object(document) || typeof document.name !== 'string' || typeof document.uri !== 'string' || !/^[0-9a-f]{64}$/.test(document.digest ?? '')) throw new Error('Captured input document metadata is invalid');
    const path = document.uri?.startsWith('file:') ? fileURLToPath(document.uri) : document.uri;
    if (typeof path !== 'string' || !isAbsolute(path)) throw new Error('Captured input documents must have absolute local paths');
    const info = await stat(path);
    if (!info.isFile() || info.size + documentBytes > config.max_request_bytes) throw new Error('Task documents exceed the configured request byte limit');
    const file = await open(path, 'r');
    let bytes;
    try {
      bytes = Buffer.alloc(info.size + 1);
      const { bytesRead } = await file.read(bytes, 0, bytes.length, 0);
      bytes = bytes.subarray(0, bytesRead);
    } finally { await file.close(); }
    if (createHash('sha256').update(bytes).digest('hex') !== document.digest) throw new Error('Captured input document digest changed');
    documentBytes += bytes.length;
    documents.push({ name: document.name, content: new TextDecoder('utf-8', { fatal: true }).decode(bytes) });
  }
  if (!task.brief.trim() && documents.length === 0) throw new Error('Task has no brief or captured documents');
  const request = {
    model: config.model,
    state: { task_phase: typedTask?.relationship ?? 'new', user_message: task.brief, documents, ...(typedTask ? { typed_task: typedTask } : {}) },
    questions: JSON.parse(await readFile(questionsURL, 'utf8')),
  };
  if (Buffer.byteLength(JSON.stringify(request)) > config.max_request_bytes) throw new Error('Task and questions exceed the configured request byte limit');
  return request;
}

export function validateResponse(response, questions) {
  if (!object(response) || response.error || !object(response.answers) || typeof response.model !== 'string' || !response.model) throw new Error('Provider did not return a valid decision response');
  for (const [name, question] of Object.entries(questions)) {
    const answer = response.answers[name];
    if (!object(answer) || answer.type !== question.type) throw new Error(`Invalid or missing answer type: ${name}`);
    if (question.type === 'noul') {
      if (!probability(answer.noul)) throw new Error(`Invalid yes/no probability: ${name}`);
      continue;
    }
    const labels = Object.keys(question.criteria);
    if (!labels.includes(answer.choice) || !object(answer.probabilities) || !probability(answer.confidence)) throw new Error(`Invalid choice answer: ${name}`);
    if (Object.keys(answer.probabilities).length !== labels.length || !labels.every(label => probability(answer.probabilities[label]))) throw new Error(`Invalid choice probabilities: ${name}`);
    const sum = labels.reduce((total, label) => total + answer.probabilities[label], 0);
    if (answer.probabilities[answer.choice] < Math.max(...Object.values(answer.probabilities))) throw new Error(`Choice does not match the highest probability: ${name}`);
    if (Math.abs(sum - 1) > 0.02) throw new Error(`Choice probabilities do not sum to one: ${name}`);
  }
  return response;
}

async function responseJSON(response, limit) {
  if (!response.body) throw new Error('Provider returned an empty response');
  const reader = response.body.getReader();
  const chunks = [];
  let size = 0;
  try {
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > limit) throw new Error('Provider response exceeds the configured byte limit');
      chunks.push(value);
    }
    return JSON.parse(Buffer.concat(chunks).toString('utf8'));
  } finally { await reader.cancel().catch(() => {}); }
}

export async function evaluate(task, config, apiKey, fetchAPI = fetch, typedTask) {
  if (typeof apiKey !== 'string' || !apiKey.trim()) throw new Error(`Missing credential environment variable: ${config.api_key_env}`);
  const request = await buildRequest(task, config, typedTask);
  // Never forward a credential accidentally pasted into the task or provider output.
  if (JSON.stringify(request).includes(apiKey)) throw new Error('Task contains the configured provider credential');
  let response;
  try {
    response = await fetchAPI(config.endpoint, {
      method: 'POST', redirect: 'error',
      headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(request), signal: AbortSignal.timeout(config.timeout_ms),
    });
  } catch { throw new Error('Decision provider request failed or timed out'); }
  if (!response.ok) { await response.body?.cancel(); throw new Error(`Decision provider returned HTTP ${response.status}`); }
  let body;
  try { body = await responseJSON(response, config.max_response_bytes); }
  catch { throw new Error('Decision provider returned invalid, oversized or incomplete JSON'); }
  if (JSON.stringify(body).includes(apiKey)) throw new Error('Provider response contains the configured credential');
  validateResponse(body, request.questions);
  return { request, response: body };
}

export function usageEvent(response) {
  const usage = response.usage;
  if (!object(usage) || !integer(usage.input_tokens) || !integer(usage.output_tokens)) return undefined;
  const event = {
    type: 'factory.telemetry.v1', sequence: 1, kind: 'usage',
    provider: response.provider, model: response.model,
    tokens: { input: usage.input_tokens, output: usage.output_tokens, cache_read: 0, cache_write: 0 },
  };
  if (typeof usage.cost === 'number' && Number.isFinite(usage.cost) && usage.cost >= 0) event.cost_usd = usage.cost;
  return event;
}

// This policy is code, not an LLM interpretation. All non-admitted valid
// answers require an explicit operator decision; transport errors never enter it.
export function admissionResult(response, config, typedTask) {
  if (config.admission === null) return {
    outcome: 'completed',
    summary: 'Task readiness evaluated; consume the original request and response as fallible assessment data.',
  };
  const answer = response.answers.readiness;
  const threshold = config.admission.minimum_probability;
  const investigation = typedTask?.type === 'investigation';
  const typeConfirmed = response.answers.type_match?.choice === 'match' && !typedTask?.classification.uncertain;
  if (typeConfirmed && answer.choice === 'accept' && answer.probabilities.accept >= threshold) return {
    outcome: investigation ? 'investigation_admitted' : 'admitted',
    summary: `Admission granted: readiness accept probability ${answer.probabilities.accept} meets ${threshold}.`,
  };
  return {
    outcome: investigation ? 'investigation_review_required' : 'review_required',
    summary: `Admission withheld: type ${response.answers.type_match?.choice}, readiness ${answer.choice}, accept probability ${answer.probabilities.accept}, required ${threshold}. Operator approval is required before downstream work.`,
  };
}
