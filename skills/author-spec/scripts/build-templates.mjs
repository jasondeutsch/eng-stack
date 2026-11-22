#!/usr/bin/env node
// Registry maintenance only. Agents use the generated, self-contained HTML.
import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../..');
const check = process.argv.slice(2);
if (check.length > 1 || (check.length === 1 && check[0] !== '--check')) {
  console.error('Usage: node skills/author-spec/scripts/build-templates.mjs [--check]');
  process.exit(1);
}
const shell = await readFile(path.join(here, '../assets/document.html'), 'utf8');
const styles = await readFile(path.join(here, '../assets/document.css'), 'utf8');
const escapeHTML = text => text.replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);

for (const kind of ['spec', 'plan']) {
  const type = kind === 'spec' ? 'Specification' : 'Implementation plan';
  const companion = kind === 'spec' ? 'plan.html' : 'spec.html';
  const templates = [
    { directory: path.join(root, `skills/author-${kind}/assets`), title: '[Document title]', reference: '[Assignment reference]', state: 'Draft', source: '[Brief / source reference]', revision: '[Document revision]', related: '[Companion revision]' },
    { directory: path.join(root, `skills/author-${kind}/examples/small`), title: 'Case-insensitive status filtering', reference: 'EXAMPLE-01', state: 'Illustrative', source: 'Fictional CLI brief; not a repository finding', revision: '1', related: '1' },
    { directory: path.join(root, `skills/author-${kind}/examples/service`), title: 'Idempotent job submission', reference: 'EXAMPLE-02', state: 'Illustrative', source: 'Fictional service brief and project rules', revision: '1', related: '1' },
  ];
  for (const document of templates) {
    const content = await readFile(path.join(document.directory, `${kind}.body.html`), 'utf8');
    const sections = [...content.matchAll(/<section id="([\w-]+)">\s*<h2><span class="section-number">\d+<\/span>([^<]+)<\/h2>/g)];
    if (!sections.length) throw new Error(`No navigable sections in ${document.directory}/${kind}.body.html`);
    const navigation = sections.map(([, id, label]) => `  <a href="#${id}">${escapeHTML(label.trim())}</a>`).join('\n');
    const fields = { TITLE: escapeHTML(document.title), TYPE: type, REFERENCE: escapeHTML(document.reference), REVISION: escapeHTML(document.revision), STATE: document.state, SOURCE: escapeHTML(document.source), COMPANION_REVISION: escapeHTML(document.related), COMPANION: document.state === 'Illustrative' ? `../../../author-${kind === 'spec' ? 'plan' : 'spec'}/examples/${path.basename(document.directory)}/${companion}` : companion, NAVIGATION: navigation, STYLES: styles.trimEnd(), CONTENT: content.trimEnd(), FOOTER: document.state === 'Illustrative' ? 'Illustrative design fixture. Requirements and project rules are fictional. No implementation, verification run, or approval is claimed.' : 'Draft design artifact. Execution evidence and any required decisions are recorded separately by the assignment.' };
    const output = shell.replace(/\{\{([A-Z_]+)\}\}/g, (_, name) => {
      if (!(name in fields)) throw new Error(`Unknown shell field: ${name}`);
      return fields[name];
    });
    const destination = path.join(document.directory, `${kind}.html`);
    if (check.length) {
      let existing;
      try { existing = await readFile(destination, 'utf8'); } catch { /* Report a missing generated template as stale. */ }
      if (existing !== output) throw new Error(`Stale template: ${path.relative(root, destination)}; run build-templates.mjs`);
    } else {
      await writeFile(destination, output);
    }
  }
}
console.log(check.length ? 'Planning templates are current.' : 'Built planning templates and examples.');
