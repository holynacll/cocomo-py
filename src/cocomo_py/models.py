from dataclasses import dataclass
from enum import StrEnum

class ProjectMode(StrEnum):
    ORGANIC = "organic"
    SEMI_DETACHED = "semi-detached"
    EMBEDDED = "embedded"

@dataclass(frozen=True)
class CocomoResult:
    """
    Data structure to store the results of the COCOMO calculation.
    It is 'frozen=True' to ensure the immutability of the results.
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

# Custom exceptions for the library
class AnalysisError(Exception):
    """Generic error during source code analysis."""
    pass

class ClocNotFoundError(AnalysisError):
    """Exception raised when the 'cloc' command is not found."""
    pass

