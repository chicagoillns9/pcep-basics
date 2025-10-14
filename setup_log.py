from __future__ import annotations
import os, sys, platform, datetime, json, pathlib, subprocess

LOG_DIR = pathlib.Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "project_log.txt"
STATE_FILE = LOG_DIR / "last_state.json"

def shell(cmd: str) -> str:
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except Exception:
        return ""

def snapshot() -> dict:
    return {
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "cwd": str(pathlib.Path.cwd()),
        "venv": os.environ.get("VIRTUAL_ENV", ""),
        "pip_freeze": shell("python -m pip freeze"),
        "git_branch": shell("git rev-parse --abbrev-ref HEAD"),
        "git_status": shell("git status --porcelain"),
    }

def write_log(snap: dict) -> None:
    header = f"[{snap['timestamp']}] Python {snap['python']} | {snap['platform']}\n"
    venv = f"VENV: {snap['venv'] or 'None'}\n"
    branch = f"GIT: branch={snap['git_branch'] or '—'} pending={bool(snap['git_status'])}\n"
    prev = LOG_FILE.read_text() if LOG_FILE.exists() else ""
    LOG_FILE.write_text(prev + header + venv + branch + "\n")
    STATE_FILE.write_text(json.dumps(snap, indent=2))
    print(f"✅ Logged to {LOG_FILE} and saved state to {STATE_FILE}")

if __name__ == "__main__":
    write_log(snapshot())
