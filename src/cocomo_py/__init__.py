"""
Cocomo-py: Uma ferramenta e biblioteca Python para estimar o custo de software usando o modelo COCOMO.
"""

__version__ = "0.2.0"

# Expõe as funções e classes principais para quem for usar como biblioteca
from .calculator import calculate
from .analyzer import analyze_kloc
from .models import CocomoResult, ProjectMode, ClocNotFoundError, AnalysisError
from .constants import COCOMO_MODES, COST_DRIVERS

# Define explicitamente a API pública do pacote.
# Isto controla o que é importado quando se usa 'from cocomo_py import *'
__all__ = [
    "calculate",
    "analyze_kloc",
    "ProjectMode",
    "COCOMO_MODES",
    "COST_DRIVERS",
    "AnalysisError",
    "CocomoResult",
    "ClocNotFoundError",
    "AnalysisError",
]

