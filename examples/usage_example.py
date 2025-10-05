from pathlib import Path

# Importa os componentes públicos da biblioteca
from cocomo_py import (
    analyze_kloc,
    calculate,
    ProjectMode,
    ClocNotFoundError,
    AnalysisError
)

def main():
    """
    Função principal que demonstra o uso da biblioteca cocomo-py.
    """
    print("🚀 Demonstrando o uso da biblioteca cocomo-py 🚀")

    # NOTA: Altere este caminho para uma pasta de projeto real na sua máquina.
    # Para este exemplo, vamos tentar analisar o próprio projeto cocomo-py.
    project_path = Path(__file__).parent.parent 

    if not project_path.exists() or not project_path.is_dir():
        print(f"❌ O caminho '{project_path}' não é um diretório válido.")
        return

    try:
        # --- 1. Análise do Código-Fonte ---
        print(f"\n[1] Analisando o código-fonte em: {project_path}...")
        kloc = analyze_kloc(project_path)
        print(f"✅ Análise concluída: {kloc:.2f} KLOC")

        # --- 2. Exemplo de Cálculo Básico ---
        print("\n[2] Executando um cálculo COCOMO Básico (Modo Orgânico)...")
        basic_result = calculate(
            kloc=kloc,
            mode=ProjectMode.ORGANIC,
            cost_per_month=10000
        )
        print("--- Resultados (Básico) ---")
        print(f"  Esforço: {basic_result.effort_person_months:.2f} pessoas-mês")
        print(f"  Custo Total: R$ {basic_result.total_cost:,.2f}")

        # --- 3. Exemplo de Cálculo Intermediário ---
        print("\n[3] Executando um cálculo COCOMO Intermediário...")
        drivers = {
            "rely": "high",  # O projeto exige alta fiabilidade
            "cplx": "high",  # A complexidade é alta
            "tool": "vhigh"  # Usamos ferramentas muito boas
        }
        intermediate_result = calculate(
            kloc=kloc,
            mode=ProjectMode.SEMI_DETACHED,
            cost_per_month=10000,
            drivers=drivers
        )
        print("--- Resultados (Intermediário) ---")
        print(f"  Fator de Ajuste (EAF): {intermediate_result.eaf:.3f}")
        print(f"  Esforço: {intermediate_result.effort_person_months:.2f} pessoas-mês")
        print(f"  Custo Total: R$ {intermediate_result.total_cost:,.2f}")

    except ClocNotFoundError:
        print("\n❌ Erro: O comando 'cloc' não foi encontrado.")
        print("   Por favor, instale-o e garanta que está no seu PATH.")
    except AnalysisError as e:
        print(f"\n❌ Erro durante a análise: {e}")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()
