from src.oas_diff_dialog import REPORT_TYPES, normalize_selected_reports


def test_normalize_selected_reports_preserves_valid_selection_order():
    selected = normalize_selected_reports(["impact", "synthesis", "impact", "unknown"])

    assert selected == ["impact", "synthesis"]


def test_normalize_selected_reports_defaults_to_all_reports_for_empty_or_invalid_values():
    assert normalize_selected_reports([]) == list(REPORT_TYPES)
    assert normalize_selected_reports(["unknown"]) == list(REPORT_TYPES)
    assert normalize_selected_reports(None) == list(REPORT_TYPES)
