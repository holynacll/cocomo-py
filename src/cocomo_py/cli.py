"""
Módulo da Interface de Linha de Comando (CLI) para o cocomo-py.
Esta é a camada de apresentação que interage com o utilizador.
"""
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

# Importa a lógica de negócio e as constantes
from . import __version__
from .calculator import calculate
from .analyzer import analyze_kloc
from .models import ProjectMode, AnalysisError, ClocNotFoundError
from .constants import COCOMO_MODES, COST_DRIVERS

app = typer.Typer(
    name="cocomo-py",
    help="Uma ferramenta CLI para estimar o custo de software usando o modelo COCOMO.",
    add_completion=False
)
console = Console()

def version_callback(value: bool):
    """Exibe a versão da aplicação e termina."""
    if value:
        console.print(f"cocomo-py versão: [bold green]{__version__}[/bold green]")
        raise typer.Exit()

@app.command(name="estimate", help="Estima o esforço e custo de um projeto de software.")
def estimate_project(
    project_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="O caminho para a pasta do projeto a ser analisado."
    ),
    mode: ProjectMode = typer.Option(
        ProjectMode.SEMI_DETACHED,
        "--mode", "-m",
        case_sensitive=False,
        help="O modo do projeto COCOMO."
    ),
    cost_per_month: float = typer.Option(
        8000.0,
        "--cost-per-month", "-c",
        help="Custo médio de um desenvolvedor por mês (ex: 8000.0)."
    ),
    intermediate: bool = typer.Option(
        False,
        "--intermediate", "-i",
        help="Ativa o modo interativo para o cálculo COCOMO Intermediário."
    ),
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True,
        help="Exibe a versão da aplicação."
    ),
):
    """
    Analisa um projeto, calcula a estimativa COCOMO e exibe os resultados.
    """
    try:
        with console.status("[bold green]Analisando linhas de código...[/bold green]"):
            kloc = analyze_kloc(project_path)
        console.print(f"✅ Análise concluída: [bold cyan]{kloc:.2f} KLOC[/bold cyan]")

        drivers = {}
        if intermediate:
            console.print("\n--- [bold]Avaliação dos Drivers de Custo (COCOMO Intermediário)[/bold] ---")
            console.print("Avalie cada item. Pressione Enter para usar o valor padrão 'nominal (nom)'.")
            for code, details in COST_DRIVERS.items():
                valid_ratings = list(details['ratings'].keys())
                console.print(f"-> [yellow]{details['name']} ({code.upper()})[/yellow]", end=" ")
                prompt_text = f"[{'/'.join(valid_ratings)}]"
                rating = typer.prompt(prompt_text, default="nom", show_default=True)
                if rating.lower() not in valid_ratings:
                    console.print(f"[yellow]Aviso: Classificação '{rating}' inválida para '{details['name']}'. Usando 'nom'.[/yellow]")
                    rating = "nom"
                if rating.lower() != "nom":
                    drivers[code] = rating

        # Calcula o resultado
        result = calculate(kloc, mode, cost_per_month, drivers)

        # Exibe a tabela de resultados
        console.print("\n--- [bold green]Resultado da Estimativa COCOMO[/bold green] ---")
        table = Table(show_header=False)
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="magenta")

        table.add_row("Modo do Projeto", COCOMO_MODES[result.mode]['name'])
        table.add_row("Linhas de Código (KLOC)", f"{result.kloc:.2f}")
        if result.is_intermediate:
            table.add_row("Fator de Ajuste de Esforço (EAF)", f"{result.eaf:.3f}")
        
        table.add_row("Esforço Estimado", f"{result.effort_person_months:.2f} pessoas-mês")
        table.add_row("Tempo de Desenvolvimento", f"{result.development_time_months:.2f} meses")
        table.add_row("Pessoas Recomendadas", f"{result.people_required:.2f} pessoas")
        table.add_row("Custo por Mês (Unitário)", f"R$ {result.cost_per_month:,.2f}".replace(',', '.'))
        table.add_row("[bold]Custo Total Estimado[/bold]", f"[bold]R$ {result.total_cost:,.2f}[/bold]".replace(',', '.'))

        console.print(table)

    except ClocNotFoundError:
        console.print("[bold red]Erro: O comando 'cloc' não foi encontrado.[/bold red]")
        console.print("Por favor, instale o 'cloc' e certifique-se de que está no seu PATH.")
        raise typer.Exit(code=1)
    except AnalysisError as e:
        console.print(f"[bold red]Erro durante a análise: {e}[/bold red]")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Ocorreu um erro inesperado: {e}[/bold red]")
        raise typer.Exit(code=1)


@app.command(name="explain", help="Explica os conceitos do modelo COCOMO.")
def explain_cocomo(
    topic: str = typer.Argument(
        None,
        case_sensitive=False,
        help="O tópico a ser explicado ('modes' ou 'drivers'). Se omitido, explica ambos."
    )
):
    """
    Exibe descrições detalhadas sobre os modos de projeto e os drivers de custo do COCOMO.
    """
    if not topic or topic == "modes":
        console.print("\n--- [bold green]Modos de Projeto COCOMO[/bold green] ---")
        for mode, details in COCOMO_MODES.items():
            console.print(f"\n[bold cyan]{details['name']} ({mode})[/bold cyan]")
            console.print(f"{details['description']}")

    if not topic or topic == "drivers":
        console.print("\n--- [bold green]Drivers de Custo COCOMO[/bold green] ---")
        for code, details in COST_DRIVERS.items():
            ratings_str = ", ".join(details['ratings'].keys())
            console.print(f"\n[bold cyan]{details['name']} ({code.upper()})[/bold cyan]")
            console.print(f"{details['description']}")
            console.print(f"[italic]Classificações: {ratings_str}[/italic]")

if __name__ == "__main__":
    app()

