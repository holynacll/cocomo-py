"""
This module centralizes all data, constants, and descriptions
related to the COCOMO (Constructive Cost Model).
"""

# Dictionary with parameters for Basic COCOMO project modes.
# The keys 'a', 'b', 'c', 'd' are the coefficients and exponents used in the formulas.
COCOMO_MODES = {
    "organic": {
        "a": 2.4, "b": 1.05, "c": 2.5, "d": 0.38,
        "name": "Organic",
        "description": "Relatively small, simple projects developed by small, experienced teams with good domain knowledge. Requirements are flexible and the development environment is stable."
    },
    "semi-detached": {
        "a": 3.0, "b": 1.12, "c": 2.5, "d": 0.35,
        "name": "Semi-Detached",
        "description": "A project of intermediate size and complexity. The team may have a mix of experience levels, and requirements may be a combination of rigid and flexible."
    },
    "embedded": {
        "a": 3.6, "b": 1.20, "c": 2.5, "d": 0.32,
        "name": "Embedded",
        "description": "Projects developed under tight hardware, software, and operational constraints. They are often complex, innovative, and have strict reliability and performance requirements."
    }
}

# Dictionary with the 15 cost drivers for Intermediate COCOMO.
# Each driver has a description and effort multipliers for each rating level.
COST_DRIVERS = {
    'rely': {
        'name': "Required Software Reliability",
        'description': "Measures the degree to which the software must perform reliably. A failure can range from a minor inconvenience to a financial or human catastrophe.",
        'ratings': {'vlow': 0.75, 'low': 0.88, 'nom': 1.00, 'high': 1.15, 'vhigh': 1.40}
    },
    'data': {
        'name': "Database Size",
        'description': "Measures the size and complexity of the database used in relation to the program size.",
        'ratings': {'low': 0.94, 'nom': 1.00, 'high': 1.08, 'vhigh': 1.16}
    },
    'cplx': {
        'name': "Product Complexity",
        'description': "Assesses the project's complexity in five areas: control, computation, I/O operations, user interface, and data management.",
        'ratings': {'vlow': 0.70, 'low': 0.85, 'nom': 1.00, 'high': 1.15, 'vhigh': 1.30, 'xhigh': 1.65}
    },
    'time': {
        'name': "Execution Time Constraints",
        'description': "Measures the time constraint imposed on the software during its execution. The higher the percentage of available time used, the higher the multiplier.",
        'ratings': {'nom': 1.00, 'high': 1.11, 'vhigh': 1.30, 'xhigh': 1.66}
    },
    'stor': {
        'name': "Main Storage Constraints",
        'description': "Measures the main memory (RAM) constraint imposed on the software.",
        'ratings': {'nom': 1.00, 'high': 1.06, 'vhigh': 1.21, 'xhigh': 1.56}
    },
    'virt': {
        'name': "Virtual Machine Volatility",
        'description': "Assesses the frequency with which the hardware and software platform (virtual machine) changes during development.",
        'ratings': {'low': 0.87, 'nom': 1.00, 'high': 1.15, 'vhigh': 1.30}
    },
    'turn': {
        'name': "Computer Turnaround Time",
        'description': "Measures the response time required of the system, from query to response, especially in interactive systems.",
        'ratings': {'low': 0.87, 'nom': 1.00, 'high': 1.07, 'vhigh': 1.15}
    },
    'acap': {
        'name': "Analyst Capability",
        'description': "Assesses the capability, efficiency, and experience of the requirements analysis team.",
        'ratings': {'vlow': 1.46, 'low': 1.19, 'nom': 1.00, 'high': 0.86, 'vhigh': 0.71}
    },
    'aexp': {
        'name': "Application Experience",
        'description': "Assesses the development team's experience with the type of application being developed.",
        'ratings': {'vlow': 1.29, 'low': 1.13, 'nom': 1.00, 'high': 0.91, 'vhigh': 0.82}
    },
    'pcap': {
        'name': "Programmer Capability",
        'description': "Assesses the capability and talent of the programming team.",
        'ratings': {'vlow': 1.42, 'low': 1.17, 'nom': 1.00, 'high': 0.86, 'vhigh': 0.70}
    },
    'vexp': {
        'name': "Virtual Machine Experience",
        'description': "Assesses the team's experience with the development platform (hardware, OS, etc.).",
        'ratings': {'vlow': 1.21, 'low': 1.10, 'nom': 1.00, 'high': 0.90}
    },
    'lexp': {
        'name': "Programming Language Experience",
        'description': "Assesses the team's experience with the programming language and tools used.",
        'ratings': {'vlow': 1.14, 'low': 1.07, 'nom': 1.00, 'high': 0.95}
    },
    'modp': {
        'name': "Use of Modern Programming Practices",
        'description': "Assesses the degree to which the team uses modern practices like structured programming, top-down design, etc.",
        'ratings': {'vlow': 1.24, 'low': 1.10, 'nom': 1.00, 'high': 0.91, 'vhigh': 0.82}
    },
    'tool': {
        'name': "Use of Software Tools",
        'description': "Measures the level of use of software tools that assist in development (e.g., advanced IDEs, debuggers, testing tools).",
        'ratings': {'vlow': 1.24, 'low': 1.10, 'nom': 1.00, 'high': 0.91, 'vhigh': 0.83}
    },
    'sced': {
        'name': "Required Development Schedule",
        'description': "Measures the tightness of the project schedule. An accelerated schedule increases the required effort.",
        'ratings': {'vlow': 1.23, 'low': 1.08, 'nom': 1.00, 'high': 1.04, 'vhigh': 1.10}
    }
}
