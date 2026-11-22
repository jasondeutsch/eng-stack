#!/usr/bin/env node
// Render content sections with the canonical, offline planning-document shell.
import { readFileSync, realpathSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { parseArgs } from 'node:util';

const here = dirname(import.meta.filename);
const escape = text => String(text).replace(/[&<>"']/g, character => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
}[character]));

export function bodyOf(html) {
  const marker = '<main id="content">';
  const start = html.indexOf(marker);
  const end = html.lastIndexOf('</main>');
  if (start < 0 || end < start) {
    throw new Error('Expected the standard planning document with <main id="content">');
  }
  return html.slice(start + marker.length, end).trim();
}

export function readDocument(html) {
  const header = html.match(/<header class="document-header">[\s\S]*?<\/header>/)?.[0];
  if (!header) throw new Error('Expected the standard document metadata header');
  return `${header}\n${bodyOf(html)}`;
}

export function render(kind, content, metadata) {
  if (!['spec', 'plan'].includes(kind)) throw new Error('Document kind must be spec or plan');
  if (!metadata.title?.trim()) throw new Error('Document title is required');
  // This accepts the canonical flat-section format, not arbitrary HTML layouts.
  const sections = [...content.matchAll(/<section id="([\w-]+)">\s*<h2>(?:<span class="section-number">\d+<\/span>)?([^<]+)<\/h2>/g)];
  if (!sections.length) {
    throw new Error('Body needs named sections: <section id="scope"><h2>Scope</h2>…</section>');
  }
  if (new Set(sections.map(section => section[1])).size !== sections.length) {
    throw new Error('Section IDs must be unique');
  }
  if (/<script\b|<style\b|<link\b|<!doctype\b|<html\b|<main\b|<header\b/i.test(content)) {
    throw new Error('Supply content sections only; the renderer owns the shell and styles');
  }
  const fields = {
    TITLE: escape(metadata.title),
    TYPE: kind === 'spec' ? 'Specification' : 'Implementation plan',
    REFERENCE: escape(metadata.reference || 'Not supplied'),
    REVISION: escape(metadata.revision || '1'),
    STATE: 'Draft',
    SOURCE: escape(metadata.source || 'Assignment brief'),
    COMPANION_REVISION: escape(metadata['companion-revision'] || 'Not supplied'),
    COMPANION: kind === 'spec' ? 'plan.html' : 'spec.html',
    STYLES: readFileSync(join(here, '../assets/document.css'), 'utf8').trimEnd(),
    CONTENT: content.trim(),
    NAVIGATION: sections.map(([, id, label]) => `  <a href="#${id}">${label.trim()}</a>`).join('\n'),
    FOOTER: 'Design artifact. Execution evidence and any required decisions are recorded separately by the assignment.',
  };
  return readFileSync(join(here, '../assets/document.html'), 'utf8')
    .replace(/\{\{([A-Z_]+)\}\}/g, (_, name) => fields[name]);
}

function main() {
  const names = ['body', 'output', 'title', 'reference', 'revision', 'source', 'companion-revision'];
  const { positionals, values } = parseArgs({
    allowPositionals: true,
    options: Object.fromEntries(names.map(name => [name, { type: 'string' }])),
  });
  const [command, kindOrPath] = positionals;
  if (command === 'read' && positionals.length === 2) {
    // Include actual revision/source metadata without the presentation markup.
    process.stdout.write(readDocument(readFileSync(kindOrPath, 'utf8')) + '\n');
  } else if (command === 'render' && positionals.length === 2 && values.body && values.output && values.title) {
    writeFileSync(values.output, render(kindOrPath, readFileSync(values.body, 'utf8'), values));
    console.log(`Rendered ${values.output} from ${values.body}`);
  } else {
    throw new Error('Usage: document.mjs read DOCUMENT | render spec|plan --body BODY.html --output DOCUMENT.html --title TITLE [--revision REV --companion-revision REV --reference REF --source SOURCE]');
  }
}

if (process.argv[1] && realpathSync(process.argv[1]) === import.meta.filename) {
  try { main(); }
  catch (error) {
    console.error(`Planning document: ${error.message}`);
    process.exitCode = 1;
  }
}
