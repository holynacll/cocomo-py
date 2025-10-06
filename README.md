# **cocomo-py: Software Cost Estimator**

cocomo-py is a Python tool and library that estimates the effort, time, and cost to develop a software project. The analysis is based on the **COCOMO (Constructive Cost Model)**.

## **Features**

* **Dual Use:** Works as a ready-to-use **CLI** or as a **library** to integrate into your own scripts.
* **Quick Analysis:** Calculates the cost from a local source code folder.
* **COCOMO Model:** Uses the Basic and Intermediate COCOMO models.
* **Interactive Mode:** Allows you to adjust the estimate with 15 "cost drivers" for greater accuracy.
* **User-Friendly Interface:** Uses rich to display CLI results clearly.

## **Prerequisites**

* Python 3.11+
* **cloc:** An external tool for counting lines of code. It is essential that cloc is installed and accessible in your PATH.
  * **Ubuntu/Debian:** `sudo apt install cloc`
  * **macOS (Homebrew):** `brew install cloc`

## **Installation**

You can install cocomo-py directly from PyPI (when published) using pip, uv, or your favorite Python package manager.

```
# With uv
uv pip install cocomo-py

# With pip
pip install cocomo-py
```

After installation, the `cocomo` command will be available globally.

## **Usage as CLI**

Run the `cocomo` command followed by the path to the project folder.

```
### **Example (Basic Mode)**

cocomo /path/to/my/project

### **Example (Intermediate Mode)**

cocomo /path/to/my/project --intermediate --cost-per-month 9500

# Get help on COCOMO concepts
cocomo explain
```

## **Usage as a Library**

Import and use the `analyze_kloc` and `calculate` functions in your Python projects.
```
from cocomo_py import calculate, analyze_kloc, ProjectMode

try:
    kloc = analyze_kloc("./my-project")
    result = calculate(
        kloc=kloc,
        mode=ProjectMode.SEMI_DETACHED,
        cost_per_month=10000,
        drivers={"rely": "high", "cplx": "vhigh"}
    )
    print(f"Estimated Total Cost: $ {result.total_cost:,.2f}")
except Exception as e:
    print(f"An error occurred: {e}")
```

## **Development**

To contribute to the project:

1. Clone the repository.
2. Create a virtual environment: `uv venv`
3. Activate the environment: `source .venv/bin/activate`
4. Install in editable mode: `uv pip install -e .`
5. Run tests with pytest: `pytest`

## **License**

This project is licensed under the MIT License.