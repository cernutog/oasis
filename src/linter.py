import subprocess
import json
import os
import tempfile


class OASLinter:
    """
    Unified OpenAPI linter supporting both Spectral and Vacuum engines.
    Both produce Spectral-compatible JSON output, so parsing is identical.
    """

    ENGINES = ("spectral", "vacuum")

    def __init__(self, cmd, engine="spectral"):
        self.cmd = cmd
        self.engine = engine if engine in self.ENGINES else "spectral"

    def run_lint(self, file_path, log_callback=None):
        """
        Runs linting on the given file using the configured engine.
        """

        def log(msg):
            if log_callback:
                log_callback(msg)

        if not os.path.exists(file_path):
            log(f"Error: File not found: {file_path}")
            return {
                "success": False,
                "error_msg": "File not found",
                "summary": {},
                "details": [],
            }

        fd, temp_out = tempfile.mkstemp(suffix=".json")
        os.close(fd)

        # Determine ruleset path
        ruleset_path = os.path.abspath(".spectral.yaml")
        temp_ruleset = None

        if not os.path.exists(ruleset_path):
            log("Ruleset not found. Creating temporary default ruleset...")
            fd_r, temp_ruleset = tempfile.mkstemp(suffix=".yaml")
            os.close(fd_r)
            with open(temp_ruleset, "w") as f:
                f.write("extends: spectral:oas\n")
            ruleset_path = temp_ruleset

        # Build command based on engine
        if self.engine == "vacuum":
            command = f'"{self.cmd}" spectral-report -r "{ruleset_path}" "{file_path}" "{temp_out}"'
        else:
            command = f'"{self.cmd}" lint "{file_path}" --ruleset "{ruleset_path}" -f json --output "{temp_out}"'

        log(f"[{self.engine.upper()}] Executing: {command}")

        try:
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,
                stdin=subprocess.DEVNULL,
            )

            # Cleanup temp ruleset if we created one
            if temp_ruleset and os.path.exists(temp_ruleset):
                os.remove(temp_ruleset)

            log(f"Process ended. Return Code: {process.returncode}")
            if process.stderr:
                log(f"STDERR: {process.stderr[:200]}...")

            if not os.path.exists(temp_out) or os.path.getsize(temp_out) == 0:
                log("Error: Output file empty or missing.")
                return {
                    "success": False,
                    "error_msg": f"{self.engine.capitalize()} output missing.",
                    "summary": {},
                    "details": [],
                }

            log("Parsing JSON output...")
            with open(temp_out, "r", encoding="utf-8") as f:
                results = json.load(f)

            log(f"Found {len(results)} issues.")

            # Analyze results - identical format for both engines
            summary = {"error": 0, "warning": 0, "info": 0, "hint": 0}
            code_summary = {}
            simplified_details = []

            for item in results:
                severity_map = {0: "error", 1: "warning", 2: "info", 3: "hint"}
                severity_code = item.get("severity", 0)
                severity_str = severity_map.get(severity_code, "error")

                code = item.get("code", "unknown")
                summary[severity_str] = summary.get(severity_str, 0) + 1

                if code not in code_summary:
                    code_summary[code] = {"count": 0, "severity": severity_str}
                code_summary[code]["count"] += 1

                raw_path = item.get("path", [])
                path_str = (
                    " > ".join([str(p) for p in raw_path]) if raw_path else "Root"
                )

                simplified_details.append(
                    {
                        "code": code,
                        "message": item.get("message"),
                        "path": path_str,
                        "line": item.get("range", {}).get("start", {}).get("line", 0)
                        + 1,
                        "severity": severity_str,
                    }
                )

            return {
                "success": True,
                "summary": summary,
                "code_summary": code_summary,
                "details": simplified_details,
                "raw_count": len(results),
                "raw_data": results,
                "engine": self.engine,
            }

        except subprocess.TimeoutExpired:
            log("Error: Timeout Expired!")
            return {
                "success": False,
                "error_msg": "Timeout (120s)",
                "summary": {},
                "details": [],
            }
        except Exception as e:
            log(f"Exception: {str(e)}")
            return {"success": False, "error_msg": str(e), "summary": {}, "details": []}
        finally:
            if os.path.exists(temp_out):
                try:
                    os.remove(temp_out)
                except (OSError, PermissionError):
                    pass


# Backward compatibility alias
SpectralRunner = OASLinter
