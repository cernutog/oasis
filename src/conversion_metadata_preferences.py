"""Shared preference mapping for template conversion metadata."""

METADATA_PREFERENCE_KEYS = {
    "contact_name": "tools_legacy_contact_name",
    "contact_url": "tools_legacy_contact_url",
    "release": "tools_legacy_release",
    "filename_pattern": "tools_legacy_filename_pattern",
    "swift_service": "tools_legacy_swift_service",
}


def empty_metadata_defaults() -> dict[str, str]:
    return {field_name: "" for field_name in METADATA_PREFERENCE_KEYS}


def load_metadata_preferences(prefs_manager) -> dict[str, str]:
    defaults = empty_metadata_defaults()
    if not prefs_manager:
        return defaults

    for field_name, preference_key in METADATA_PREFERENCE_KEYS.items():
        defaults[field_name] = str(prefs_manager.get(preference_key, "") or "").strip()
    return defaults


def save_metadata_preferences(prefs_manager, values: dict) -> None:
    if not prefs_manager:
        return

    for field_name, preference_key in METADATA_PREFERENCE_KEYS.items():
        if field_name not in values:
            continue
        prefs_manager.set(preference_key, str(values.get(field_name, "") or "").strip())
    prefs_manager.save()
