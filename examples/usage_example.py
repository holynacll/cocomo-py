from pathlib import Path

# Import the public components of the library
from cocomo_py import (
    analyze_kloc,
    calculate,
    ProjectMode,
    ClocNotFoundError,
    AnalysisError
)

def main():
    """
    Main function demonstrating the use of the cocomo-py library.
    """
    print("🚀 Demonstrating the use of the cocomo-py library 🚀")

    # NOTE: Change this path to a real project folder on your machine.
    # For this example, let's try to analyze the cocomo-py project itself.
    project_path = Path(__file__).parent.parent 

    if not project_path.exists() or not project_path.is_dir():
        print(f"❌ The path '{project_path}' is not a valid directory.")
        return

    try:
        # --- 1. Source Code Analysis ---
        print(f"\n[1] Analyzing source code in: {project_path}...")
        kloc = analyze_kloc(project_path)
        print(f"✅ Analysis complete: {kloc:.2f} KLOC")

        # --- 2. Basic Calculation Example ---
        print("\n[2] Running a Basic COCOMO calculation (Organic Mode)...")
        basic_result = calculate(
            kloc=kloc,
            mode=ProjectMode.ORGANIC,
            cost_per_month=10000
        )
        print("--- Results (Basic) ---")
        print(f"  Effort: {basic_result.effort_person_months:.2f} person-months")
        print(f"  Total Cost: $ {basic_result.total_cost:,.2f}")

        # --- 3. Intermediate Calculation Example ---
        print("\n[3] Running an Intermediate COCOMO calculation...")
        drivers = {
            "rely": "high",  # The project requires high reliability
            "cplx": "high",  # The complexity is high
            "tool": "vhigh"  # We use very good tools
        }
        intermediate_result = calculate(
            kloc=kloc,
            mode=ProjectMode.SEMI_DETACHED,
            cost_per_month=10000,
            drivers=drivers
        )
        print("--- Results (Intermediate) ---")
        print(f"  Adjustment Factor (EAF): {intermediate_result.eaf:.3f}")
        print(f"  Effort: {intermediate_result.effort_person_months:.2f} person-months")
        print(f"  Total Cost: $ {intermediate_result.total_cost:,.2f}")

    except ClocNotFoundError:
        print("\n❌ Error: The 'cloc' command was not found.")
        print("   Please install it and ensure it is in your PATH.")
    except AnalysisError as e:
        print(f"\n❌ Error during analysis: {e}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
