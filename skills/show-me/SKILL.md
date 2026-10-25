---
name: show-me
description: Explain something visually in chat — flowcharts, sequence diagrams, ERDs, architecture, interactive explainers. Picks the right diagram form, renders it so it actually displays inline, and offers to install the right connector when the tool for the job is missing. Trigger on "show me visually", "explain this visually", "draw this", "diagram this", "visualize this as a diagram", "visualise this as a diagram", "map this out visually". Not for showing file contents, diffs, logs or command output, and not for data charts or dashboards (the dataviz skill covers those when installed).
---

# Show me

The user wants to see it, not read it. Pick the form, render it inline, keep the prose in the reply and the picture in the tool.

## 1. Pick the form

| They want to understand... | Use | Rendered with |
|---|---|---|
| Steps, decisions, a pipeline | Mermaid `flowchart` | `show_widget` + mermaid.js |
| Who talks to whom, in what order, over time | Mermaid `sequenceDiagram` | `show_widget` + mermaid.js |
| Tables, fields, relationships | Mermaid `erDiagram` / `classDiagram` | `show_widget` + mermaid.js |
| Parts and how they connect (overview) | SVG structural diagram | `show_widget` (SVG) |
| "How does X actually work" (a feel for it) | Illustrative or interactive widget | `show_widget` (HTML + inline SVG) |

Numeric charts and dashboards are out of scope: use `dataviz` if it's installed.

If the first diagram would need more than about 7 nodes, split it: an overview, then one diagram per sub-flow, with a short paragraph between each. Only promise the diagrams you actually draw.

## 2. Render Mermaid through `show_widget`, not the Mermaid connector

The Mermaid connector tool (`validate_and_render_mermaid_diagram`) returns the whole rendered SVG inside its tool result: 60–100k characters per diagram. That exceeds the result limit, so the result is dumped to a file and the diagram often never shows in chat. In practice, three connector calls in one turn displayed nothing. Do not use it for display.

What works: load the widget guidance once (`mcp__visualize__read_me`, modules `diagram`; do not narrate it), then call `show_widget` with an HTML fragment that imports mermaid.js, pinned to an exact version so a CDN change can't silently blank the widget (bump it deliberately). One diagram per call. Keep the init block below exactly as written, since the font and size are used for layout measurement. Replace only the Mermaid source inside the `mermaid.render` template literal (the `flowchart TD ...` body is a placeholder), and the `<h2>` summary:

```html
<h2 class="sr-only">One sentence describing the diagram</h2>
<div id="d" style="width:100%"></div>
<script type="module">
import mermaid from 'https://esm.sh/mermaid@11.17.2/dist/mermaid.esm.min.mjs';
const themeMode = document.documentElement.dataset.mode;
const dark = themeMode ? themeMode === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
await document.fonts.ready;
mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  fontFamily: '"anthropic-sans", sans-serif',
  themeVariables: {
    darkMode: dark,
    fontSize: '13px',
    fontFamily: '"anthropic-sans", sans-serif',
    lineColor: dark ? '#9c9a92' : '#73726c',
    textColor: dark ? '#c2c0b6' : '#3d3d3a',
  },
});
const { svg } = await mermaid.render('d-svg', `flowchart TD
  a["Step one"] --> b["Step two"]`);
document.getElementById('d').innerHTML = svg;
</script>
```

Mermaid tips:
- Quote every node label (`a["like this"]`) and use `<br/>` for line breaks.
- Don't use `classDef` colours; the base theme already follows light and dark mode.
- Give each widget a unique render id (`fc-svg`, `sq-svg`) if you draw more than one.

If you must use the connector anyway (for example, to validate syntax), never read its result. It lands in a saved file; if `jq` is available, check `jq '.valid'` on that file and stop there, otherwise treat the diagram as unvalidated and render it with `show_widget`.

## 3. Rules for what goes in the chat

- Explanation goes in the reply text. The widget holds only the visual.
- Sentence case labels, no emoji, no mid-sentence bold.
- Short labels in boxes (title plus at most five words of subtitle).
- After rendering, say in one line what each diagram shows. Don't re-describe it.
- If a diagram doesn't appear for the user, say what you tried and switch method (see the ladder below). Don't repeat the same call.

## 4. When the tool is missing, offer the right connector

Before drawing, check which render tools are in this session: `mcp__visualize__show_widget` (inline widgets) and any diagram, Figma or docs connector. Then:

1. **`show_widget` present:** use it. No connector needed, even for Mermaid.
2. **`show_widget` absent and the user wants live diagrams:** search for a connector with `mcp__mcp-registry__search_mcp_registry` (keywords such as `diagram`, `mermaid`, `whiteboard`), then show the match with `mcp__mcp-registry__suggest_connectors`. These are deferred tools, so load their schemas with ToolSearch first. If the registry isn't available, try `SearchPlugins` then `SuggestPluginInstall`.
3. **Nothing installable or the user declines:** fall back, in this order:
   1. A fenced ` ```mermaid ` block in the reply (renders in claude.ai, GitHub and Notion).
   2. A Notion page or doc if the picture should be kept and shared.
   3. An ASCII/Unicode box diagram in a code block.

Say plainly which route you took and why, in one line, so the user knows whether the connector is worth installing.

## 5. Offer a keep-and-share step

If the diagram is something the user will return to or hand to someone else, offer once to publish it (an artifact or a Notion page). Don't publish unasked.
