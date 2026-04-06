TABLE_NAMES = (
    "events",
    "segments",
    "results",
    "elements",
    "program_components",
)

DEFAULT_MANIFEST_URL = "https://storage.googleapis.com/cleanskate/latest.json"

DEFAULT_ELEMENT_COLUMNS = (
    "event_label",
    "event_series",
    "segment_label",
    "name",
    "noc",
    "element_number",
    "element_code",
    "element_family",
    "valid_element",
    "info_flags",
    "base_value",
    "second_half_bonus",
    "goe",
    "panel_score",
    "judge_scores",
)

DEFAULT_PROGRAM_COMPONENT_COLUMNS = (
    "event_label",
    "event_series",
    "segment_label",
    "name",
    "noc",
    "component_name",
    "factor",
    "average",
    "judge_scores",
)

DEFAULT_SEGMENT_COLUMNS = (
    "event_label",
    "event_series",
    "discipline",
    "segment_name",
    "segment_label",
    "is_team_event",
    "base_discipline",
    "result_count",
    "segment_order",
)

DEFAULT_RESULT_COLUMNS = (
    "event_label",
    "event_series",
    "segment_label",
    "rank",
    "name",
    "noc",
    "starting_number",
    "total_segment_score",
    "total_element_score",
    "total_program_component_score",
    "total_deductions",
    "element_base_value_sum",
    "element_panel_score_sum",
    "program_component_score_factored",
    "deduction_detail",
)
