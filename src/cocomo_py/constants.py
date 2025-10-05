"""
Este módulo centraliza todos os dados, constantes e descrições
relacionadas com o modelo COCOMO (Constructive Cost Model).
"""

# Dicionário com os parâmetros para os modos de projeto do COCOMO Básico.
# As chaves 'a', 'b', 'c', 'd' são os coeficientes e expoentes usados nas fórmulas.
COCOMO_MODES = {
    "organic": {
        "a": 2.4, "b": 1.05, "c": 2.5, "d": 0.38,
        "name": "Orgânico",
        "description": "Projetos relativamente pequenos e simples, desenvolvidos por equipes pequenas e experientes com bons conhecimentos do domínio. Os requisitos são flexíveis e o ambiente de desenvolvimento é estável."
    },
    "semi-detached": {
        "a": 3.0, "b": 1.12, "c": 2.5, "d": 0.35,
        "name": "Semi-Acoplado",
        "description": "Um projeto de tamanho e complexidade intermédios. A equipe pode ter uma mistura de níveis de experiência e os requisitos podem ser uma combinação de rígidos e flexíveis."
    },
    "embedded": {
        "a": 3.6, "b": 1.20, "c": 2.5, "d": 0.32,
        "name": "Embutido",
        "description": "Projetos desenvolvidos sob restrições apertadas de hardware, software e operacionais. São frequentemente complexos, inovadores e com requisitos rigorosos de fiabilidade e desempenho."
    }
}

# Dicionário com os 15 drivers de custo do COCOMO Intermediário.
# Cada driver tem uma descrição e os multiplicadores de esforço para cada nível de classificação.
COST_DRIVERS = {
    'rely': {
        'name': "Fiabilidade Exigida do Software",
        'description': "Mede o grau em que o software deve funcionar de forma fiável. Uma falha pode variar de um pequeno inconveniente a uma catástrofe financeira ou humana.",
        'ratings': {'vlow': 0.75, 'low': 0.88, 'nom': 1.00, 'high': 1.15, 'vhigh': 1.40}
    },
    'data': {
        'name': "Tamanho da Base de Dados",
        'description': "Mede o tamanho e a complexidade da base de dados utilizada em relação ao tamanho do programa.",
        'ratings': {'low': 0.94, 'nom': 1.00, 'high': 1.08, 'vhigh': 1.16}
    },
    'cplx': {
        'name': "Complexidade do Produto",
        'description': "Avalia a complexidade do projeto em cinco áreas: controlo, computação, operações de E/S, interface de utilizador e gestão de dados.",
        'ratings': {'vlow': 0.70, 'low': 0.85, 'nom': 1.00, 'high': 1.15, 'vhigh': 1.30, 'xhigh': 1.65}
    },
    'time': {
        'name': "Restrições de Tempo de Execução",
        'description': "Mede a restrição de tempo imposta ao software durante a sua execução. Quanto maior a percentagem de tempo disponível utilizada, maior o multiplicador.",
        'ratings': {'nom': 1.00, 'high': 1.11, 'vhigh': 1.30, 'xhigh': 1.66}
    },
    'stor': {
        'name': "Restrições de Armazenamento Principal",
        'description': "Mede a restrição de memória principal (RAM) imposta ao software.",
        'ratings': {'nom': 1.00, 'high': 1.06, 'vhigh': 1.21, 'xhigh': 1.56}
    },
    'virt': {
        'name': "Volatilidade da Máquina Virtual",
        'description': "Avalia a frequência com que a plataforma de hardware e software (máquina virtual) muda durante o desenvolvimento.",
        'ratings': {'low': 0.87, 'nom': 1.00, 'high': 1.15, 'vhigh': 1.30}
    },
    'turn': {
        'name': "Tempo de Resposta do Computador",
        'description': "Mede o tempo de resposta exigido ao sistema, desde a consulta até à resposta, especialmente em sistemas interativos.",
        'ratings': {'low': 0.87, 'nom': 1.00, 'high': 1.07, 'vhigh': 1.15}
    },
    'acap': {
        'name': "Capacidade do Analista",
        'description': "Avalia a capacidade, eficiência e experiência da equipe de análise de requisitos.",
        'ratings': {'vlow': 1.46, 'low': 1.19, 'nom': 1.00, 'high': 0.86, 'vhigh': 0.71}
    },
    'aexp': {
        'name': "Experiência na Aplicação",
        'description': "Avalia a experiência da equipe de desenvolvimento com o tipo de aplicação a ser desenvolvida.",
        'ratings': {'vlow': 1.29, 'low': 1.13, 'nom': 1.00, 'high': 0.91, 'vhigh': 0.82}
    },
    'pcap': {
        'name': "Capacidade do Programador",
        'description': "Avalia a capacidade e talento da equipe de programação.",
        'ratings': {'vlow': 1.42, 'low': 1.17, 'nom': 1.00, 'high': 0.86, 'vhigh': 0.70}
    },
    'vexp': {
        'name': "Experiência com a Máquina Virtual",
        'description': "Avalia a experiência da equipe com a plataforma de desenvolvimento (hardware, SO, etc.).",
        'ratings': {'vlow': 1.21, 'low': 1.10, 'nom': 1.00, 'high': 0.90}
    },
    'lexp': {
        'name': "Experiência na Linguagem de Programação",
        'description': "Avalia a experiência da equipe com a linguagem de programação e as ferramentas utilizadas.",
        'ratings': {'vlow': 1.14, 'low': 1.07, 'nom': 1.00, 'high': 0.95}
    },
    'modp': {
        'name': "Uso de Práticas Modernas de Programação",
        'description': "Avalia o grau de utilização de práticas modernas como programação estruturada, design top-down, etc., pela equipe.",
        'ratings': {'vlow': 1.24, 'low': 1.10, 'nom': 1.00, 'high': 0.91, 'vhigh': 0.82}
    },
    'tool': {
        'name': "Uso de Ferramentas de Software",
        'description': "Mede o nível de utilização de ferramentas de software que auxiliam no desenvolvimento (ex: IDEs avançadas, depuradores, ferramentas de teste).",
        'ratings': {'vlow': 1.24, 'low': 1.10, 'nom': 1.00, 'high': 0.91, 'vhigh': 0.83}
    },
    'sced': {
        'name': "Cronograma de Desenvolvimento Exigido",
        'description': "Mede o aperto do cronograma do projeto. Um cronograma acelerado aumenta o esforço necessário.",
        'ratings': {'vlow': 1.23, 'low': 1.08, 'nom': 1.00, 'high': 1.04, 'vhigh': 1.10}
    }
}
