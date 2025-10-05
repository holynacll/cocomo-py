import subprocess
import json
from pathlib import Path
from .models import AnalysisError, ClocNotFoundError

def analyze_kloc(project_path: Path) -> float:
    """
    Analisa um diretório local para contar as linhas de código usando 'cloc'.

    Args:
        project_path: O caminho para o diretório do projeto.

    Returns:
        O total de milhares de linhas de código ('KLOC').

    Raises:
        ClocNotFoundError: Se o executável 'cloc' não for encontrado.
        AnalysisError: Se o diretório não existir ou se houver um erro ao executar o cloc.
    """
    if not project_path.is_dir():
        raise AnalysisError(f"O diretório especificado não existe: {project_path}")

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
            "Comando 'cloc' não encontrado. "
            "Por favor, instale-o e garanta que está no seu PATH do sistema."
        )
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        raise AnalysisError(f"Ocorreu um erro ao analisar o código com cloc: {e}")
