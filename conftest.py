"""Root pytest configuration for django-docutils."""

from __future__ import annotations

import pytest


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Skip runtime smoke tests unless explicitly requested via ``-m``.

    The smoke test builds the project and resolves dependencies in a throwaway
    environment, which is too slow for the default ``pytest`` loop. CI runs it
    as its own step.
    """
    marker_name = "scripts__runtime_dep_smoketest"
    markexpr = getattr(config.option, "markexpr", "") or ""
    if marker_name in markexpr:
        return

    skip_marker = pytest.mark.skip(
        reason=f"pass -m {marker_name} to run runtime dependency smoke tests",
    )
    for item in items:
        if marker_name in item.keywords:
            item.add_marker(skip_marker)
