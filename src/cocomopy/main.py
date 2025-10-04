import typer
from typing_extensions import Annotated
from rich import print
from rich.console import Console
from rich.table import Table
import os

# Importa as funções dos outros módulos
from code_analyze import analyze_directory
from cocomo_calculator import (
    calculate_basic_cocomo,
    calculate_intermediate_cocomo,
    COST_DRIVERS,
)

app = typer.Typer(help="Uma ferramenta CLI para estimar o custo de software usando o modelo COCOMO a partir de uma pasta local.")
console = Console()

def _prompt_for_drivers() -> dict:
    """Pede interativamente ao usuário para avaliar cada driver de custo."""
    console.rule("[bold cyan]Avaliação dos Drivers de Custo (COCOMO Intermediário)[/bold cyan]")
    print("\nAvalie cada item. O padrão é 'nom' (nominal).\n")
    
    ratings = {}
    for driver_code, (description, valid_options_dict) in COST_DRIVERS.items():
        valid_options = list(valid_options_dict.keys())
        prompt_text = f"-> [bold]{description}[/bold] ({driver_code.upper()}) [{'/'.join(valid_options)}]"
        
        choice = typer.prompt(
            prompt_text,
            type=str,
            default='nom',
            show_choices=False,
        ).lower()

        while choice not in valid_options:
            print(f"[bold red]Opção inválida! Escolha entre: {', '.join(valid_options)}[/bold red]")
            choice = typer.prompt(prompt_text, type=str, default='nom').lower()

        ratings[driver_code] = choice
    return ratings

@app.command()
def estimate(
    project_path: Annotated[str, typer.Argument(help="Caminho para a pasta do projeto de código-fonte.", exists=True, file_okay=False, dir_okay=True, readable=True)],
    mode: Annotated[str, typer.Option(help="Modo do projeto COCOMO.")] = "semi-detached",
    cost_per_month: Annotated[float, typer.Option(help="Custo médio de um desenvolvedor por mês (salário + encargos).")] = 7000.0,
    intermediate: Annotated[bool, typer.Option("--intermediate", help="Usar o modelo COCOMO Intermediário (interativo).")] = False,
):
    """
    Estima o custo de um software baseado em uma pasta de código-fonte local.
    """
    kloc = analyze_directory(project_path)
    
    # Se analyze_directory retornou -1, cloc não está instalado.
    if kloc == -1.0:
        raise typer.Exit(code=1)
    # Se analyze_directory retornou -2, o caminho é inválido (embora Typer já verifique).
    if kloc == -2.0:
        raise typer.Exit(code=1)
        
    if kloc == 0:
        console.print("[yellow]Não foi possível contar as linhas de código ou o diretório não contém código fonte analisável.[/yellow]")
        raise typer.Exit()

    console.print(f"\n[green]Análise concluída:[/green] {kloc:.2f} KLOC (milhares de linhas de código).")
    
    if intermediate:
        driver_ratings = _prompt_for_drivers()
        result = calculate_intermediate_cocomo(kloc, mode, driver_ratings)
        title = f"Estimativa COCOMO Intermediário (Modo: {mode.capitalize()})"
    else:
        result = calculate_basic_cocomo(kloc, mode)
        title = f"Estimativa COCOMO Básico (Modo: {mode.capitalize()})"

    total_cost = result['effort_person_months'] * cost_per_month

    # Exibe os resultados em uma tabela bonita com Rich
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Métrica", style="cyan")
    table.add_column("Valor", style="green")

    if 'eaf' in result:
            table.add_row("Fator de Ajuste (EAF)", f"{result['eaf']:.2f}")

    table.add_row("Esforço Estimado", f"{result['effort_person_months']:.2f} pessoas-mês")
    table.add_row("Tempo de Desenvolvimento", f"{result['development_time_months']:.2f} meses")
    table.add_row("Equipe Recomendada", f"{result['people_required']:.2f} pessoas")
    table.add_row("Custo Total Estimado", f"R$ {total_cost:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

    print("\n")
    console.print(table)


if __name__ == "__main__":
    app()
