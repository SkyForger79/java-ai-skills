# Serena Navigation Reference

Use this reference only when Serena MCP tools are available and source-code
symbol navigation will reduce broad file reading.

## Availability And Index

1. Call `initial_instructions` before source-code discovery.
2. If the repository has project instructions for Serena, follow them first.
3. Refresh the index when starting from a new or rebased checkout, after large
   refactors, after branch switches with many source changes, or when symbol
   results look stale:
   ```bash
   serena project index
   serena project health-check
   ```
4. If index commands fail or Serena tools are unavailable, continue with
   `scan.py`, `rg`, targeted file reads, and tests. Do not block the whole skill
   on Serena.

## Navigation Pattern

- Start with `search_for_pattern` when you do not know the symbol or file.
- Use `get_symbols_overview` on the smallest relevant source file before reading
  implementation bodies.
- Use `find_symbol` for known classes, functions, methods, records, enums, graph
  nodes, adapters, controllers, DTOs, and tests.
- Set `include_body=false` until the body is needed for a claim.
- Use `find_referencing_symbols` when documenting API boundaries, framework
  entry points, state keys, routing nodes, persistence adapters, or shared
  helpers.
- Remember Serena line numbers are 0-based; convert carefully if the final docs
  include line references.

## Documentation Mapping

- `STACK.md`: prefer manifests, build files, lockfiles, container config, and
  scan output; use Serena only to confirm framework entry points.
- `STRUCTURE.md`: use file layout plus symbol overviews for representative
  packages/modules.
- `ARCHITECTURE.md`: use symbol overviews and references for controllers,
  runtimes, routers, services, adapters, persistence, and integration boundaries.
- `CONVENTIONS.md`: compare representative symbols across production and tests;
  avoid overgeneralizing from one file.
- `INTEGRATIONS.md`: inspect API clients, repositories, messaging clients,
  configuration classes, and test fakes/stubs.
- `TESTING.md`: inspect test classes, fixtures, base classes, fake clients, and
  targeted test commands.
- `CONCERNS.md`: combine scan metrics, churn, TODO searches, test gaps, and
  symbol reference hotspots.

## Evidence Rule

Serena identifies where to look; it does not prove behavior by itself. Every
non-trivial documentation claim must still cite real files, config, tests, or
terminal output. If a claim cannot be confirmed, write `[TODO]`; if it depends
on team intent, write `[ASK USER]`.
