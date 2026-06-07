"""Tests for django-docutils settings reload behavior."""

from __future__ import annotations

import typing as t

import pytest
from django.test import override_settings

from django_docutils.lib.settings import DJANGO_DOCUTILS_LIB_RST, reload_settings


class ReloadCase(t.NamedTuple):
    """An ``override_settings`` payload for ``DJANGO_DOCUTILS_LIB_RST``."""

    test_id: str
    override: dict[str, object]


RELOAD_CASES: list[ReloadCase] = [
    ReloadCase(
        test_id="replace-docutils",
        override={"docutils": {"raw_enabled": True}},
    ),
    ReloadCase(
        test_id="empty-dict",
        override={},
    ),
    ReloadCase(
        test_id="unsafe-flag",
        override={"allow_unsafe_docutils_settings": True},
    ),
]


@pytest.mark.parametrize(
    ReloadCase._fields,
    RELOAD_CASES,
    ids=[case.test_id for case in RELOAD_CASES],
)
def test_override_settings_round_trip_restores_rst_settings(
    test_id: str,
    override: dict[str, object],
) -> None:
    """``override_settings`` enter/exit must restore the original settings."""
    before = dict(DJANGO_DOCUTILS_LIB_RST)
    assert before

    with override_settings(DJANGO_DOCUTILS_LIB_RST=override):
        assert dict(DJANGO_DOCUTILS_LIB_RST) == override

    assert dict(DJANGO_DOCUTILS_LIB_RST) == before


def test_reload_settings_with_self_as_value_preserves_contents() -> None:
    """Reloading with the module state itself as ``value`` must not empty it.

    ``override_settings`` teardown fires ``setting_changed`` with the restored
    original object; if that object is the module state, a clear-then-update
    sequence reads from an already-emptied dict.
    """
    before = dict(DJANGO_DOCUTILS_LIB_RST)
    assert before

    reload_settings(
        signal=None,
        sender=None,
        setting="DJANGO_DOCUTILS_LIB_RST",
        value=DJANGO_DOCUTILS_LIB_RST,
        enter=False,
    )

    assert dict(DJANGO_DOCUTILS_LIB_RST) == before
