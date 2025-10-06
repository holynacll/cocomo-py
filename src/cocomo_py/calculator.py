"""
Main module for COCOMO calculations.
This is the core business logic of the library.
"""
from typing import Dict, Optional

from .models import CocomoResult, ProjectMode
from .constants import COCOMO_MODES, COST_DRIVERS

def calculate(
    kloc: float,
    mode: ProjectMode,
    cost_per_month: float,
    drivers: Optional[Dict[str, str]] = None
) -> CocomoResult:
    """
    Calculates the effort, time, and cost estimate using the COCOMO model.

    Args:
        kloc: Kilo Lines of Code.
        mode: The project mode ('organic', 'semi-detached', 'embedded').
        cost_per_month: The average monthly cost of a developer.
        drivers: An optional dictionary with the ratings of the cost drivers
                 for the Intermediate calculation. Ex: {'rely': 'high', 'cplx': 'low'}

    Returns:
        A CocomoResult object with all the estimation data.
    """
    if mode not in COCOMO_MODES:
        raise ValueError(f"Invalid mode '{mode}'. Choose from {', '.join(COCOMO_MODES.keys())}")

    params = COCOMO_MODES[mode]

    # 1. Calculate Nominal Effort (base for both models)
    nominal_effort = params['a'] * (kloc ** params['b'])

    # 2. Calculate EAF if it is an intermediate calculation
    eaf = 1.0
    if drivers:
        for driver_code, rating in drivers.items():
            driver_code_lower = driver_code.lower()
            rating_lower = rating.lower()
            if driver_code_lower in COST_DRIVERS and rating_lower in COST_DRIVERS[driver_code_lower]['ratings']:
                eaf *= COST_DRIVERS[driver_code_lower]['ratings'][rating_lower]
            # Ignores invalid drivers or ratings, keeping the multiplier 1.0
    
    # 3. Calculate Adjusted Effort
    adjusted_effort = nominal_effort * eaf

    # 4. Calculate development time based on adjusted effort
    dev_time_months = params['c'] * (adjusted_effort ** params['d'])

    # 5. Calculate the number of people and the total cost
    people_required = adjusted_effort / dev_time_months if dev_time_months > 0 else 0
    total_cost = adjusted_effort * cost_per_month

    return CocomoResult(
        kloc=kloc,
        mode=mode,
        effort_person_months=adjusted_effort,
        development_time_months=dev_time_months,
        people_required=people_required,
        total_cost=total_cost,
        cost_per_month=cost_per_month,
        eaf=eaf,
        is_intermediate=bool(drivers)
    )

