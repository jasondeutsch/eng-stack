#!/usr/bin/env node
// Validate local prerequisites without installing software or contacting providers.
import { accessSync, constants, readFileSync, statSync } from 'node:fs';
import { delimiter, join, resolve } from 'node:path';

export function findCommand(command, env = process.env, cwd = process.cwd()) {
  if (!command || command.includes('\0')) return undefined;
  const candidates = command.includes('/') ? [resolve(cwd, command)] : (env.PATH || '').split(delimiter).map(dir => resolve(cwd, dir || '.', command));
  return candidates.find(file => { try { accessSync(file, constants.X_OK); return statSync(file).isFile(); } catch { return false; } });
}

export function checkTools({ executable, profile, required = [] }, env = process.env) {
  const missing = [];
  const requireCommand = (name, source, commandEnv = env, cwd = process.cwd()) => {
    if (!findCommand(name, commandEnv, cwd)) missing.push(`${source}: ${name}`);
  };
  requireCommand(executable, 'agent executable');
  for (const name of required) requireCommand(name, 'required command');
  if (profile) {
    let config;
    try { config = JSON.parse(readFileSync(join(profile, 'mcp.json'), 'utf8')); }
    catch (error) { if (error.code !== 'ENOENT') throw new Error('Cannot read native MCP configuration'); }
    for (const [name, server] of Object.entries(config?.mcpServers || {})) {
      if (server.enabled === false || !server.command) continue;
      requireCommand(server.command, `MCP ${name}`, { ...env, ...server.env }, server.cwd || process.cwd());
    }
  }
  return [...new Set(missing)];
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(import.meta.filename)) {
  try {
    const args = process.argv.slice(2), options = { required: [] };
    while (args.length) {
      const flag = args.shift(), value = args.shift();
      if (!value || !['--agent','--profile','--require'].includes(flag)) throw new Error('Usage: preflight.mjs --agent EXECUTABLE [--profile DIRECTORY] [--require COMMAND ...]');
      if (flag === '--require') options.required.push(value);
      else options[flag === '--agent' ? 'executable' : 'profile'] = value;
    }
    if (!options.executable) throw new Error('Agent executable is required');
    const missing = checkTools(options);
    if (missing.length) throw new Error(`Missing local tools:\n${missing.map(name => '  '+name).join('\n')}\nInstall/configure these before starting this agent. No tools were downloaded.`);
  } catch (error) {
    console.error(`Agent preflight: ${error.message}`);
    process.exitCode = 1;
  }
}
