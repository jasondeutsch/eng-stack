#!/usr/bin/env node
import { withAssignment } from '@pragma/controls-sdk/result-client';
import { configuration, evaluate, usageEvent, admissionResult } from './evaluate.mjs';

// Legacy Factory invocations keep their saved-evaluation/replay behavior.
if (!process.env.AGENT_MCP_URL) {
  await import('./legacy.mjs');
} else {
  try {
    await withAssignment(process.env, async (assignment, complete, client) => {
      try {
        const config = await configuration(assignment.configuration);
        const input = assignment.input;
        const task = typeof input.task === 'string'
          ? { brief: input.task + (input.context ? '\nAdditional context (data):\n' + JSON.stringify(input.context) : ''), documents: [] }
          : input.task;
        if (!input.typed_task) throw new Error('Missing typed_task from intake');
        const data = await evaluate(task, config, process.env[config.api_key_env], fetch, input.typed_task);
        const metric = usageEvent(data.response);
        if (metric) console.log(JSON.stringify(metric));
        await complete({ ...admissionResult(data.response, config, input.typed_task), data });
        console.log('Readiness assignment result accepted.');
      } catch (error) {
        // Evaluator errors deliberately omit credentials and provider response bodies.
        await client.callTool({name:'assignment_complete',arguments:{id:assignment.id,error:error.message}}).catch(() => {});
        throw error;
      }
    });
  } catch (error) {
    console.error(`Task readiness evaluator failed: ${error.message}`);
    process.exitCode = 1;
  }
}
