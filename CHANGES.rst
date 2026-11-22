CHANGES
=======

1.0.0 (unreleased)
------------------

- Add type annotations for tests and integrate ``mypy`` and ``pyright``.

- Update project setup.

- Add support for Python 3.15 and Pypy 3.12.

- Switch from black, flake8, isort and pyupgrade to Ruff_ linter and formatter.

  .. _Ruff: https://docs.astral.sh/ruff

- Replace ``pre-commit`` integration with our custom tracked
  pre-commit git hook for Ruff checks on staged Python files.

- Fix linting errors.

- Update CI workflow.

- Adjust the deployment strategy:
  
  * Move the Pypi upload from ``zest.release`` to ``gh-actions``.

  * Use ``v`` + version as release tags like ``v1.0.0``.

  * So we still use ``zest.release`` but without publishing to Pypi.
    The Pypi upload is triggered by pushing the new release tag to GitHub.
    This happens in the Release workflow in ``.github/workflows/release.yml``.
    With this workflow we get Trusted Publishing with short-lived OIDC tokens
    that PyPI issues to one specific repository, workflow file and environment (``pypi``).
    We also get PEP 740 provenance and can set required reviewers for the environment
    and a ruleset who can create release tags and trigger releases.

- Make an overall cleanup.


0.2.0 (2026-05-06)
------------------

- Switch to src-layout.
- Add pre-commit and tox environment for it.


0.1.2 (2026-04-16)
------------------

- Add missing typings and declare more.next as typed package.


0.1.1 (2026-04-16)
------------------

- Remove support for pypy3 and adjust configuration
- Adjust allowed python version to minimum 3.12


0.1.0 (2026-04-15)
------------------

- Initial release
