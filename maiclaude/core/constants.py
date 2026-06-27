"""MaicLaude 常量定义。"""

PLUGIN_ID = "qr0w.maiclaude"
TERMINAL_STATUSES = {"succeeded", "failed", "cancelled"}
ACTIVE_STATUSES = {"queued", "running"}
SUPPORTED_COMMAND_PREFIXES = ("/claude",)
DEFAULT_CLAUDE_ENV_ALLOWLIST = {
    "PATH",
    "HOME",
    "USER",
    "USERNAME",
    "SHELL",
    "COMSPEC",
    "SYSTEMROOT",
    "WINDIR",
    "PATHEXT",
    "TEMP",
    "TMP",
    "TMPDIR",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "TERM",
    "COLORTERM",
    "CLAUDE_HOME",
}
STATUS_ALIASES = {
    "complete": "succeeded",
    "completed": "succeeded",
    "done": "succeeded",
    "ok": "succeeded",
    "success": "succeeded",
    "error": "failed",
    "failure": "failed",
    "canceled": "cancelled",
}
