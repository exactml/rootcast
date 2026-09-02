---
name: dev
description: "Design criteria and engineering conventions for rootcast — architecture principles, module/package layout, error-handling and testing conventions specific to this project. Use when writing, reviewing, or designing new rootcast code."
---

# dev

Design criteria for rootcast. This is the place to check before making an
architectural call in this repo — and the place to add a new rule right
after making one, so it doesn't have to be re-decided next time.

## Architecture

- TODO

## Module / package layout

- Backend lives under `rootcast/`.
- Frontend (when it exists) lives under a sibling `rootcast-ui/`, not
  nested inside `rootcast/`.

## Data-provider contracts

- `rootcast/data/contract.yaml` documents every provider client, section
  by section (currently only `massive`). Each client section lists its
  APIs one by one; each API entry has `enabled: true/false`, the request
  params (structured: type/required/default/description), and the
  response shape.
- Kept alongside the code, not generated from it — when an API is added
  or changed in a provider client, update its `contract.yaml` entry in
  the same change.

## Error handling

- TODO

## Testing

- Framework: pytest.
- Split into `tests/unit/` and `tests/integration/`:
  - `tests/unit/` is mocked, no network, and mirrors `rootcast/`'s package
    structure (one test file per module/class under test).
  - `tests/integration/` hits real downstream services and is *not*
    class-mirrored — it's flat, one file per compound action / downstream
    service under test, named for what's being exercised (e.g.
    `test_massive_api.py`), not for the internal class that happens to
    call it.
- Integration tests should skip themselves when required credentials
  aren't set, so a bare `pytest` run stays green without secrets (see
  `tests/integration/test_massive_api.py`).

## Naming

- TODO

## Docstrings

- Google or NumPy style.

## Environment & tooling

- Env/package management: `uv` (this repo's `.venv` has no `pip` —
  install/sync with `uv pip install -e ".[dev]" --python .venv/bin/python`).
- Linting: ruff (`ruff check .`).
