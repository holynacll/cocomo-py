"""
Módulo principal para os cálculos do COCOMO.
Esta é a lógica de negócio principal da biblioteca.
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
    Calcula a estimativa de esforço, tempo e custo usando o modelo COCOMO.

    Args:
        kloc: Milhares de linhas de código (Kilo Lines of Code).
        mode: O modo do projeto ('organic', 'semi-detached', 'embedded').
        cost_per_month: O custo médio mensal de um desenvolvedor.
        drivers: Um dicionário opcional com as classificações dos drivers de custo
                 para o cálculo Intermediário. Ex: {'rely': 'high', 'cplx': 'low'}

    Returns:
        Um objeto CocomoResult com todos os dados da estimativa.
    """
    if mode not in COCOMO_MODES:
        raise ValueError(f"Modo '{mode}' inválido. Escolha entre {', '.join(COCOMO_MODES.keys())}")

    params = COCOMO_MODES[mode]

    # 1. Calcular o Esforço Nominal (base para ambos os modelos)
    nominal_effort = params['a'] * (kloc ** params['b'])

    # 2. Calcular o EAF se for um cálculo intermediário
    eaf = 1.0
    if drivers:
        for driver_code, rating in drivers.items():
            driver_code_lower = driver_code.lower()
            rating_lower = rating.lower()
            if driver_code_lower in COST_DRIVERS and rating_lower in COST_DRIVERS[driver_code_lower]['ratings']:
                eaf *= COST_DRIVERS[driver_code_lower]['ratings'][rating_lower]
            # Ignora drivers ou ratings inválidos, mantendo o multiplicador 1.0
    
    # 3. Calcular o Esforço Ajustado
    adjusted_effort = nominal_effort * eaf

    # 4. Calcular o tempo de desenvolvimento com base no esforço ajustado
    dev_time_months = params['c'] * (adjusted_effort ** params['d'])

    # 5. Calcular o número de pessoas e o custo total
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

