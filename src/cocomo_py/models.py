from dataclasses import dataclass
from enum import StrEnum

class ProjectMode(StrEnum):
    ORGANIC = "organic"
    SEMI_DETACHED = "semi-detached"
    EMBEDDED = "embedded"

@dataclass(frozen=True)
class CocomoResult:
    """
    Estrutura de dados para armazenar os resultados do cálculo COCOMO.
    É 'frozen=True' para garantir a imutabilidade dos resultados.
    """
    kloc: float
    mode: ProjectMode
    effort_person_months: float
    development_time_months: float
    people_required: float
    total_cost: float
    cost_per_month: float
    eaf: float
    is_intermediate: bool

# Exceções personalizadas para a biblioteca
class AnalysisError(Exception):
    """Erro genérico durante a análise do código-fonte."""
    pass

class ClocNotFoundError(AnalysisError):
    """Exceção levantada quando o comando 'cloc' não é encontrado."""
    pass

