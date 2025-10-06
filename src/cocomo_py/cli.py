"""
Command-Line Interface (CLI) module for cocomo-py.
This is the presentation layer that interacts with the user.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

# Import business logic and constants
from . import __version__
from .calculator import calculate
from .analyzer import analyze_kloc
from .models import ProjectMode, AnalysisError, ClocNotFoundError
from .constants import COCOMO_MODES, COST_DRIVERS

app = typer.Typer(
    name="cocomo-py",
    help="A CLI tool to estimate software costs using the COCOMO model.",
    add_completion=False
)
console = Console()

def version_callback(value: bool):
    """Displays the application version and exits."""
    if value:
        console.print(f"cocomo-py version: [bold green]{__version__}[/bold green]")
        raise typer.Exit()

@app.command(name="estimate", help="Estimate the effort and cost of a software project.")
def estimate_project(
    project_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="The path to the project folder to be analyzed."
    ),
    mode: ProjectMode = typer.Option(
        ProjectMode.SEMI_DETACHED,
        "--mode", "-m",
        case_sensitive=False,
        help="The COCOMO project mode."
    ),
    cost_per_month: float = typer.Option(
        8000.0,
        "--cost-per-month", "-c",
        help="Average cost of a developer per month (e.g., 8000.0)."
    ),
    intermediate: bool = typer.Option(
        False,
        "--intermediate", "-i",
        help="Enables interactive mode for Intermediate COCOMO calculation."
    ),
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True,
        help="Displays the application version."
    ),
):
    """
    Analyzes a project, calculates the COCOMO estimate, and displays the results.
    """
    try:
        with console.status("[bold green]Analyzing lines of code...[/bold green]"):
            kloc = analyze_kloc(project_path)
        console.print(f"✅ Analysis complete: [bold cyan]{kloc:.2f} KLOC[/bold cyan]")

        drivers = {}
        if intermediate:
            console.print("\n--- [bold]Cost Driver Assessment (Intermediate COCOMO)[/bold] ---")
            console.print("Rate each item. Press Enter to use the default value 'nominal (nom)'.")
            for code, details in COST_DRIVERS.items():
                valid_ratings = list(details['ratings'].keys())
                console.print(f"-> [yellow]{details['name']} ({code.upper()})[/yellow]", end=" ")
                prompt_text = f"[{'/'.join(valid_ratings)}]"
                rating = typer.prompt(prompt_text, default="nom", show_default=True)
                if rating.lower() not in valid_ratings:
                    console.print(f"[yellow]Warning: Invalid rating '{rating}' for '{details['name']}'. Using 'nom'.[/yellow]")
                    rating = "nom"
                if rating.lower() != "nom":
                    drivers[code] = rating

        # Calculate the result
        result = calculate(kloc, mode, cost_per_month, drivers)

        # Display the results table
        console.print("\n--- [bold green]COCOMO Estimation Result[/bold green] ---")
        table = Table(show_header=False)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")

        table.add_row("Project Mode", COCOMO_MODES[result.mode]['name'])
        table.add_row("Lines of Code (KLOC)", f"{result.kloc:.2f}")
        if result.is_intermediate:
            table.add_row("Effort Adjustment Factor (EAF)", f"{result.eaf:.3f}")
        
        table.add_row("Estimated Effort", f"{result.effort_person_months:.2f} person-months")
        table.add_row("Development Time", f"{result.development_time_months:.2f} months")
        table.add_row("Recommended People", f"{result.people_required:.2f} people")
        table.add_row("Cost per Month (Unit)", f"$ {result.cost_per_month:,.2f}")
        table.add_row("[bold]Total Estimated Cost[/bold]", f"[bold]$ {result.total_cost:,.2f}[/bold]")

        console.print(table)

    except ClocNotFoundError:
        console.print("[bold red]Error: The 'cloc' command was not found.[/bold red]")
        console.print("Please install 'cloc' and ensure it is in your PATH.")
        raise typer.Exit(code=1)
    except AnalysisError as e:
        console.print(f"[bold red]Error during analysis: {e}[/bold red]")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        raise typer.Exit(code=1)


@app.command(name="explain", help="Explains the concepts of the COCOMO model.")
def explain_cocomo(
    topic: str = typer.Argument(
        None,
        case_sensitive=False,
        help="The topic to be explained ('modes' or 'drivers'). If omitted, explains both."
    )
):
    """
    Displays detailed descriptions of COCOMO project modes and cost drivers.
    """
    if not topic or topic == "modes":
        console.print("\n--- [bold green]COCOMO Project Modes[/bold green] ---")
        for mode, details in COCOMO_MODES.items():
            console.print(f"\n[bold cyan]{details['name']} ({mode})[/bold cyan]")
            console.print(f"{details['description']}")

    if not topic or topic == "drivers":
        console.print("\n--- [bold green]COCOMO Cost Drivers[/bold green] ---")
        for code, details in COST_DRIVERS.items():
            ratings_str = ", ".join(details['ratings'].keys())
            console.print(f"\n[bold cyan]{details['name']} ({code.upper()})[/bold cyan]")
            console.print(f"{details['description']}")
            console.print(f"[italic]Ratings: {ratings_str}[/italic]")

if __name__ == "__main__":
    app()

