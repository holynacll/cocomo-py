# Módulo para contar as linhas de código em um diretório local.

import subprocess
import json
import os

def analyze_directory(project_path: str) -> float:
    """
    Analisa um diretório local e conta as linhas de código fonte usando 'cloc'.
    Retorna o total de linhas de código em KLOC (milhares de linhas de código).
    """
    if not os.path.isdir(project_path):
        print(f"[bold red]Erro: O caminho '{project_path}' não é um diretório válido.[/bold red]")
        return -2.0 # Código de erro para caminho inválido

    try:
        # Executa o cloc com output em JSON, ignorando diretórios comuns de dependências
        cloc_command = [
            'cloc',
            project_path,
            '--json',
            '--exclude-dir=node_modules,vendor,venv,.venv,target,build,dist'
        ]
        result = subprocess.run(cloc_command, capture_output=True, text=True, check=True)
        cloc_output = json.loads(result.stdout)

        # A chave 'SUM' contém o total de todas as linguagens
        if 'SUM' in cloc_output and 'code' in cloc_output['SUM']:
            total_loc = cloc_output['SUM']['code']
            return total_loc / 1000.0  # Converte para KLOC
        else:
            print("[yellow]Aviso: 'cloc' não conseguiu sumarizar as linhas de código.[/yellow]")
            return 0.0
            
    except FileNotFoundError:
        print("\n[bold red]Erro Crítico: O comando 'cloc' não foi encontrado.[/bold red]")
        print("Por favor, instale-o e garanta que ele esteja no PATH do seu sistema.")
        return -1.0 # Código de erro para cloc não encontrado
        
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Erro ao executar ou processar a saída do cloc: {e}")
        return 0.0

