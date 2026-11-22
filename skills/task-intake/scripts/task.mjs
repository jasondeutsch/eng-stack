import { readFile } from 'node:fs/promises';
import { isDeepStrictEqual } from 'node:util';
import { pathToFileURL } from 'node:url';

export const taskTypes = ['bug-fix', 'feature', 'refactor', 'performance', 'investigation'];
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const nonempty = value => typeof value === 'string' && Boolean(value.trim());
const strings = value => Array.isArray(value) && value.every(nonempty);
const fail = path => { throw new Error(`Invalid typed task: ${path}`); };
export async function template(type) {
  if (!taskTypes.includes(type)) fail('type');
  return JSON.parse(await readFile(new URL(`../assets/${type}.json`, import.meta.url), 'utf8'));
}
function keys(value, expected, path) {
  if (!object(value) || !isDeepStrictEqual(Object.keys(value).sort(), Object.keys(expected).sort())) fail(path);
}
// The selected template defines its own nested structure. Unknown prose remains
// null; evidence/steps/drivers are lists of nonempty statements or references.
function validateDetails(value, shape, path) {
  if (shape === null) {
    if (value !== null && !nonempty(value)) fail(path);
  } else if (Array.isArray(shape)) {
    if (!strings(value)) fail(path);
  } else if (object(shape)) {
    keys(value, shape, path);
    for (const field of Object.keys(shape)) validateDetails(value[field], shape[field], `${path}.${field}`);
  } else if (value !== shape) fail(path);
}
export async function validateTask(task, original) {
  if (!object(task)) fail('object required');
  const shape = await template(task.type);
  keys(task, shape, 'fields');
  if (task.version !== shape.version) fail('version');
  if (!['new', 'follow_up'].includes(task.relationship)) fail('relationship');
  keys(task.source, shape.source, 'source');
  if (typeof task.source.brief !== 'string' || !Array.isArray(task.source.documents)) fail('source');
  for (const doc of task.source.documents) {
    if (!object(doc) || !nonempty(doc.name) || !nonempty(doc.uri) || !/^[0-9a-f]{64}$/.test(doc.digest ?? '')) fail('source.documents');
  }
  if (!task.source.brief.trim() && task.source.documents.length === 0) fail('empty source');
  if (original && !isDeepStrictEqual(task.source, { brief: original.brief, documents: original.documents ?? [] })) fail('source differs from execution input');
  for (const field of ['objective', 'target']) {
    if (task[field] !== null && !nonempty(task[field])) fail(field);
  }
  for (const field of ['references', 'constraints', 'acceptance_criteria', 'assumptions', 'unknowns']) {
    if (!strings(task[field])) fail(field);
  }
  keys(task.scope, shape.scope, 'scope');
  if (!strings(task.scope.included) || !strings(task.scope.excluded)) fail('scope');
  keys(task.classification, shape.classification, 'classification');
  const classification = task.classification;
  if (!nonempty(classification.rationale) || typeof classification.uncertain !== 'boolean' || !strings(classification.alternatives)) fail('classification');
  if (classification.alternatives.some(type => !taskTypes.includes(type) || type === task.type) || new Set(classification.alternatives).size !== classification.alternatives.length) fail('classification.alternatives');
  validateDetails(task.details, shape.details, 'details');
  return task;
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    const [command, value, original, ...extra] = process.argv.slice(2);
    if (command === 'template' && value && !original) console.log(JSON.stringify(await template(value), null, 2));
    else if (command === 'validate' && value && extra.length === 0) {
      await validateTask(JSON.parse(await readFile(value, 'utf8')), original ? JSON.parse(await readFile(original, 'utf8')) : undefined);
      console.log('Typed task structure and supplied source are valid.');
    } else throw new Error('Usage: task.mjs template TYPE | validate FILE [ORIGINAL_INPUT_JSON]');
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
