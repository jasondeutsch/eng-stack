// Compatibility for protocol: legacy; new assignments use MCP only.
import { readFile, writeFile } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { configuration, buildRequest, validateResponse, evaluate, usageEvent, admissionResult } from './evaluate.mjs';
import { withController } from '@pragma/controls-sdk/result-client';

async function main() {
  for (const name of ['FACTORY_INPUTS_PATH', 'FACTORY_PACKAGE_CONFIG', 'FACTORY_INVOCATION_DIR', 'FACTORY_MCP_URL', 'FACTORY_MCP_TOKEN', 'FACTORY_THREAD_ID', 'FACTORY_PARTICIPANT_ID']) {
    if (!process.env[name]) throw new Error(`Missing Factory runtime variable: ${name}`);
  }
  const config = await configuration(JSON.parse(await readFile(process.env.FACTORY_PACKAGE_CONFIG, 'utf8')));
  const inputs = JSON.parse(await readFile(process.env.FACTORY_INPUTS_PATH, 'utf8'));
  await withController(process.env, async submit => {
    const directory = resolve(process.env.FACTORY_INVOCATION_DIR);
    const pairPath = join(directory, 'evaluation.json');
    let data;
    try { data = JSON.parse(await readFile(pairPath, 'utf8')); }
    catch (error) { if (error.code !== 'ENOENT') throw new Error('Saved evaluation is invalid; inspect before retrying'); }
    if (data) {
      const expected = await buildRequest(inputs.task, config, inputs.typed_task);
      if (JSON.stringify(data.request) !== JSON.stringify(expected)) throw new Error('Saved evaluation does not match the assigned input and configuration');
      validateResponse(data.response, expected.questions);
    } else {
      data = await evaluate(inputs.task, config, process.env[config.api_key_env], fetch, inputs.typed_task);
      await writeFile(pairPath, JSON.stringify(data), { mode: 0o600, flag: 'wx' });
    }
    const metric = usageEvent(data.response);
    if (metric) console.log(JSON.stringify(metric));
    await submit({ ...admissionResult(data.response, config, inputs.typed_task), data });
    console.log('Task readiness evaluation accepted by controller.');
  });
}
main().catch(error => { console.error(`Task readiness evaluator failed: ${error.message}`); process.exitCode = 1; });
