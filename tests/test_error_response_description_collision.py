"""
Regression test: ErrorResponse collision detection must honor the
"include descriptions in collision detection" preference.
"""

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.legacy_converter import LegacyConverter


@pytest.fixture
def converter():
    """Return a minimal LegacyConverter for unit testing."""
    conv = LegacyConverter.__new__(LegacyConverter)
    conv.include_descriptions_in_collision = False
    conv.error_response_variant_rows = {}
    conv.error_response_description_candidates = {}
    conv._clean_value = LegacyConverter._clean_value.__get__(conv, LegacyConverter)
    conv._normalize_description_spacing = LegacyConverter._normalize_description_spacing.__get__(conv, LegacyConverter)
    conv._description_collision_key = LegacyConverter._description_collision_key.__get__(conv, LegacyConverter)
    conv._description_preference_score = LegacyConverter._description_preference_score.__get__(conv, LegacyConverter)
    conv._prefer_description_variant = LegacyConverter._prefer_description_variant.__get__(conv, LegacyConverter)
    conv._accumulate_error_response_descriptions = LegacyConverter._accumulate_error_response_descriptions.__get__(conv, LegacyConverter)
    conv._select_canonical_error_response_description = LegacyConverter._select_canonical_error_response_description.__get__(conv, LegacyConverter)
    conv._apply_canonical_error_response_descriptions = LegacyConverter._apply_canonical_error_response_descriptions.__get__(conv, LegacyConverter)
    return conv


def _candidate_rows(description: str):
    return [
        ["dateTime", "ErrorResponse", description, "schema", "", "DateTime", "", "M"],
        ["errorCode", "ErrorResponse", "The relevant error code", "schema", "", "ErrorCode", "", "M"],
        ["errorCodeDescription", "ErrorResponse", "The description of the error", "schema", "", "ErrorCodeDescription", "", "M"],
    ]


def test_error_response_fingerprint_ignores_descriptions_when_disabled(converter):
    fp_a = converter._build_error_response_fingerprint(
        _candidate_rows("Creation date and time of the bad request")
    )
    fp_b = converter._build_error_response_fingerprint(
        _candidate_rows("The date and time of the API Response creation")
    )

    assert fp_a == fp_b


def test_error_response_fingerprint_includes_descriptions_when_enabled(converter):
    converter.include_descriptions_in_collision = True

    fp_a = converter._build_error_response_fingerprint(
        _candidate_rows("Creation date and time of the bad request")
    )
    fp_b = converter._build_error_response_fingerprint(
        _candidate_rows("The date and time of the API Response creation")
    )

    assert fp_a == fp_b


def test_error_response_fingerprint_ignores_case_whitespace_and_punctuation_only(converter):
    converter.include_descriptions_in_collision = True

    fp_a = converter._build_error_response_fingerprint(
        _candidate_rows("creation date and time of the bad request")
    )
    fp_b = converter._build_error_response_fingerprint(
        _candidate_rows("  Creation   date and time of the bad request. ")
    )

    assert fp_a == fp_b


def test_capture_error_response_variant_rows_keeps_descriptions(converter):
    converter._capture_error_response_variant_rows("ErrorResponse7", _candidate_rows("Some specific 400 description"))

    assert "ErrorResponse7" in converter.error_response_variant_rows
    stored_rows = converter.error_response_variant_rows["ErrorResponse7"]
    assert stored_rows[0][0] == "dateTime"
    assert stored_rows[0][1] == "ErrorResponse7"
    assert stored_rows[0][2] == "Some specific 400 description"


def test_prefer_description_variant_prefers_uppercase_and_punctuation(converter):
    chosen = converter._prefer_description_variant(
        "creation date and time of the bad request",
        "Creation date and time of the bad request."
    )

    assert chosen == "Creation date and time of the bad request."


def test_error_response_canonical_description_prefers_best_quality_before_frequency(converter):
    rows_a = [
        ("dateTime", "ErrorResponse", "Creation date and time of the bad request", "schema", "", "DateTime", "M"),
    ]
    rows_b = [
        ("dateTime", "ErrorResponse", "Creation date and time of the bad request", "schema", "", "DateTime", "M"),
    ]
    rows_c = [
        ("dateTime", "ErrorResponse", "The date and time of the API Response creation", "schema", "", "DateTime", "M"),
    ]

    converter._accumulate_error_response_descriptions("ErrorResponse", rows_a)
    converter._accumulate_error_response_descriptions("ErrorResponse", rows_b)
    converter._accumulate_error_response_descriptions("ErrorResponse", rows_c)

    canonical = converter._apply_canonical_error_response_descriptions("ErrorResponse", rows_a)
    assert canonical[0][2] == "The date and time of the API Response creation"
