from typing import Dict, Any


class TransitionRules:
    """
    Scenario-scoped, outcome-based stage transition rules.
    Each scenario has its own checker. Stage advancement is based on
    what actually happened (response content, data returned, session established),
    never on what string the learner typed.
    """

    def check_transition(self, current_stage: Dict[str, Any], action_context: Dict[str, Any], scenario_id: str) -> bool:
        stage_id = current_stage.get("id")

        if scenario_id == "operation_phantom_firmware":
            return self._opf_check(stage_id, action_context)
        elif scenario_id == "silent_exfiltration":
            return self._se_check(stage_id, action_context)

        # Unknown scenario — allow transition (safe default for future scenarios in development)
        return True

    # ─────────────────────────────────────────────
    # Operation Phantom Firmware
    # ─────────────────────────────────────────────
    def _opf_check(self, stage_id: int, ctx: Dict[str, Any]) -> bool:
        if stage_id == 1:
            # Device record for Line 2 was read — outcome: the device exists and was returned
            return True

        elif stage_id == 2:
            # Employee record was returned — outcome: data was served (IDOR vulnerability exposed)
            return True

        elif stage_id == 3:
            # Injection: check that out-of-scope data actually came back in the response
            # The endpoint sets leaked_data=True when the injected results list was served
            return ctx.get("leaked_data", False)

        elif stage_id == 4:
            # Session escalation: firmware push succeeded via escalated privileges
            # The endpoint sets escalation_succeeded=True when the push goes through with admin role
            return ctx.get("escalation_succeeded", False)

        return True

    # ─────────────────────────────────────────────
    # Silent Exfiltration
    # ─────────────────────────────────────────────
    def _se_check(self, stage_id: int, ctx: Dict[str, Any]) -> bool:
        if stage_id == 1:
            # Brute-force authentication: successful login AFTER >= 5 failed attempts
            # The auth endpoint sets brute_force_pattern=True when this pattern is detected
            return ctx.get("brute_force_pattern", False)

        elif stage_id == 2:
            # Injection: search response contained out-of-scope rows (backup filename reference)
            # The search endpoint sets injection_leak=True when out-of-scope results were served
            return ctx.get("injection_leak", False)

        elif stage_id == 3:
            # Path traversal: the actual returned file content contains the planted secret marker
            # A request with ../ syntax that doesn't escape the dir must NOT pass
            return ctx.get("traversal_succeeded", False)

        elif stage_id == 4:
            # Stolen-key export: full unredacted dataset returned to a non-admin using the stolen key
            # Admin legitimately calling export must NOT trigger this
            return ctx.get("stolen_key_export", False)

        return True
