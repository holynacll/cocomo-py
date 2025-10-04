# Módulo para encapsular toda a lógica de cálculo do COCOMO.

# Constantes para os modos do COCOMO Básico e Intermediário
COCOMO_PARAMS = {
    'organic': {'a': 2.4, 'b': 1.05, 'c': 2.5, 'd': 0.38},
    'semi-detached': {'a': 3.0, 'b': 1.12, 'c': 2.5, 'd': 0.35},
    'embedded': {'a': 3.6, 'b': 1.20, 'c': 2.5, 'd': 0.32}
}

# Tabela de Drivers de Custo para o COCOMO Intermediário
COST_DRIVERS = {
    # Chave: (Descrição, {Níveis de Classificação})
    'rely': ("Confiabilidade exigida", {'vlow': 0.75, 'low': 0.88, 'nom': 1.00, 'high': 1.15, 'vhigh': 1.40}),
    'data': ("Tamanho da base de dados", {'low': 0.94, 'nom': 1.00, 'high': 1.08, 'vhigh': 1.16}),
    'cplx': ("Complexidade do produto", {'vlow': 0.70, 'low': 0.85, 'nom': 1.00, 'high': 1.15, 'vhigh': 1.30, 'xhigh': 1.65}),
    'time': ("Restrições de tempo de execução", {'nom': 1.00, 'high': 1.11, 'vhigh': 1.30, 'xhigh': 1.66}),
    'stor': ("Restrições de armazenamento", {'nom': 1.00, 'high': 1.06, 'vhigh': 1.21, 'xhigh': 1.56}),
    'virt': ("Volatilidade da máquina virtual", {'low': 0.87, 'nom': 1.00, 'high': 1.15, 'vhigh': 1.30}),
    'turn': ("Tempo de resposta do computador", {'low': 0.87, 'nom': 1.00, 'high': 1.07, 'vhigh': 1.15}),
    'acap': ("Capacidade do analista", {'vlow': 1.46, 'low': 1.19, 'nom': 1.00, 'high': 0.86, 'vhigh': 0.71}),
    'aexp': ("Experiência na aplicação", {'vlow': 1.29, 'low': 1.13, 'nom': 1.00, 'high': 0.91, 'vhigh': 0.82}),
    'pcap': ("Capacidade do programador", {'vlow': 1.42, 'low': 1.17, 'nom': 1.00, 'high': 0.86, 'vhigh': 0.70}),
    'vexp': ("Experiência com a máquina virtual", {'vlow': 1.21, 'low': 1.10, 'nom': 1.00, 'high': 0.90}),
    'lexp': ("Experiência na linguagem", {'vlow': 1.14, 'low': 1.07, 'nom': 1.00, 'high': 0.95}),
    'modp': ("Uso de práticas modernas", {'vlow': 1.24, 'low': 1.10, 'nom': 1.00, 'high': 0.91, 'vhigh': 0.82}),
    'tool': ("Uso de ferramentas de software", {'vlow': 1.24, 'low': 1.10, 'nom': 1.00, 'high': 0.91, 'vhigh': 0.83}),
    'sced': ("Cronograma de desenvolvimento exigido", {'vlow': 1.23, 'low': 1.08, 'nom': 1.00, 'high': 1.04, 'vhigh': 1.10}),
}


def calculate_basic_cocomo(kloc: float, mode: str) -> dict:
    """
    Calcula o esforço, tempo e pessoas para um projeto usando o COCOMO Básico.
    """
    params = COCOMO_PARAMS[mode]
    effort = params['a'] * (kloc ** params['b'])
    dev_time = params['c'] * (effort ** params['d'])
    people = effort / dev_time if dev_time > 0 else 0
    
    return {
        'effort_person_months': effort,
        'development_time_months': dev_time,
        'people_required': people,
    }


def calculate_intermediate_cocomo(kloc: float, mode: str, driver_ratings: dict) -> dict:
    """
    Calcula o esforço para um projeto usando o COCOMO Intermediário.
    `driver_ratings` é um dicionário como {'rely': 'high', 'data': 'low', ...}
    """
    # 1. Calcular o Esforço Nominal (igual ao Básico)
    params = COCOMO_PARAMS[mode]
    nominal_effort = params['a'] * (kloc ** params['b'])

    # 2. Calcular o EAF (Effort Adjustment Factor)
    eaf = 1.0
    for driver, rating in driver_ratings.items():
        if driver in COST_DRIVERS and rating in COST_DRIVERS[driver][1]:
            eaf *= COST_DRIVERS[driver][1][rating]
        
    # 3. Calcular o Esforço Ajustado
    adjusted_effort = nominal_effort * eaf

    # 4. Calcular tempo e pessoas com base no esforço ajustado
    dev_time = params['c'] * (adjusted_effort ** params['d'])
    people = adjusted_effort / dev_time if dev_time > 0 else 0

    return {
        'eaf': eaf,
        'effort_person_months': adjusted_effort,
        'development_time_months': dev_time,
        'people_required': people,
    }
