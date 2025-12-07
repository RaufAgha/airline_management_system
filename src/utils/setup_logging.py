import logging
import os
import sys
import io
import subprocess
from datetime import datetime


def setup_logging():
    """Configure application logging.

    - Primary log file: `src/cli/logs/app.log`.
    - Console logging enabled.
    - When a new git commit is detected, append a timestamped line to
      `src/cli/logs/commits.log` and update `src/cli/logs/last_commit.txt`.

    This function is safe to call multiple times; it will no-op if handlers exist.
    Failures while running `git` are suppressed so logging setup never raises.
    """

    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        return

    cli_logs_dir = os.path.join("src", "cli", "logs")
    os.makedirs(cli_logs_dir, exist_ok=True)

    root_logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    # File handler -> src/cli/logs/app.log
    fh_path = os.path.join(cli_logs_dir, "app.log")
    file_handler = logging.FileHandler(fh_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(stream=io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8"))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Attempt to write commit metadata to the CLI logs (app.log + commits.log)
    try:
        commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
        author = subprocess.check_output(["git", "log", "-1", "--pretty=format:%an <%ae>"], stderr=subprocess.DEVNULL).decode().strip()
        message = subprocess.check_output(["git", "log", "-1", "--pretty=format:%s"], stderr=subprocess.DEVNULL).decode().strip()

        marker_path = os.path.join(cli_logs_dir, "last_commit.txt")
        prev = None
        if os.path.exists(marker_path):
            try:
                with open(marker_path, "r", encoding="utf-8") as f:
                    prev = f.read().strip()
            except Exception:
                prev = None

        if commit and commit != prev:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            line = f"{timestamp} - {commit} - {author} - {message}\n"

            # Ensure app.log contains the commit line
            try:
                with open(fh_path, "a", encoding="utf-8") as f:
                    f.write(line)
            except Exception:
                pass

            # Append to commits.log (persistent history per-step)
            try:
                commits_path = os.path.join(cli_logs_dir, "commits.log")
                with open(commits_path, "a", encoding="utf-8") as cfile:
                    cfile.write(line)
            except Exception:
                pass

            # Update marker file
            try:
                with open(marker_path, "w", encoding="utf-8") as f:
                    f.write(commit)
            except Exception:
                pass

    except Exception:
        # Don't raise if git is not available or commands fail
        pass

setup_logging()
