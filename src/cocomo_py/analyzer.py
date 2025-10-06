import subprocess
import json
from pathlib import Path
from .models import AnalysisError, ClocNotFoundError

def analyze_kloc(project_path: Path) -> float:
    """
    Analyzes a local directory to count lines of code using 'cloc'.

    Args:
        project_path: The path to the project directory.

    Returns:
        The total thousands of lines of code ('KLOC').

    Raises:
        ClocNotFoundError: If the 'cloc' executable is not found.
        AnalysisError: If the directory does not exist or if there is an error running cloc.
    """
    if not project_path.is_dir():
        raise AnalysisError(f"The specified directory does not exist: {project_path}")

    try:
        cloc_command = [
            'cloc',
            str(project_path),
            '--json',
            '--exclude-dir=node_modules,vendor,venv,target,.venv'
        ]
        result = subprocess.run(
            cloc_command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        cloc_output = json.loads(result.stdout)

        if 'SUM' in cloc_output and 'code' in cloc_output['SUM']:
            total_loc = cloc_output['SUM']['code']
            return total_loc / 1000.0
        return 0.0

    except FileNotFoundError:
        raise ClocNotFoundError(
            "'cloc' command not found. "
            "Please install it and ensure it is in your system's PATH."
        )
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        raise AnalysisError(f"An error occurred while analyzing the code with cloc: {e}")
