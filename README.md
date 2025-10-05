# **cocomo-py: Estimador de Custo de Software**

cocomo-py é uma ferramenta e biblioteca Python que estima o esforço, tempo e custo para desenvolver um projeto de software. A análise é baseada no modelo **COCOMO (Constructive Cost Model)**.

## **Funcionalidades**

* **Dupla Utilização:** Funciona como uma **CLI** pronta a usar ou como uma **biblioteca** para integrar nos seus próprios scripts.  
* **Análise Rápida:** Calcula o custo a partir de uma pasta de código-fonte local.  
* **Modelo COCOMO:** Utiliza o modelo COCOMO Básico e Intermediário.  
* **Modo Interativo:** Permite ajustar a estimativa com 15 "drivers de custo" para maior precisão.  
* **Interface Amigável:** Usa rich para exibir os resultados da CLI de forma clara.

## **Pré-requisitos**

* Python 3.11+  
* **cloc:** Uma ferramenta externa para contar linhas de código. É essencial que o cloc esteja instalado e acessível no seu PATH.  
  * **Ubuntu/Debian:** sudo apt install cloc  
  * **macOS (Homebrew):** brew install cloc

## **Instalação**

Pode instalar o cocomo-py diretamente do PyPI (quando publicado) usando pip, uv ou o seu gestor de pacotes Python preferido.

```
# Com uv  
uv pip install cocomo-py

# Com pip  
pip install cocomo-py
```

Após a instalação, o comando cocomo estará disponível globalmente.

## **Uso como CLI**

Execute o comando cocomo seguido do caminho para a pasta do projeto.

```
### **Exemplo (Modo Básico)**

cocomo /caminho/para/meu/projeto```

### **Exemplo (Modo Intermediário)**

cocomo /caminho/para/meu/projeto --intermediate --cost-per-month 9500

# Obtenha ajuda sobre os conceitos do COCOMO
cocomo explain
```

## **Uso como Biblioteca**

Importe e utilize as funções analyze_kloc e calculate nos seus projetos Python.
```
from cocomo_py import calculate, analyze_kloc, ProjectMode

try:
    kloc = analyze_kloc("./meu-projeto")
    result = calculate(
        kloc=kloc,
        mode=ProjectMode.SEMI_DETACHED,
        cost_per_month=10000,
        drivers={"rely": "high", "cplx": "vhigh"}
    )
    print(f"Custo Total Estimado: R$ {result.total_cost:,.2f}")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
```

## **Desenvolvimento**

Para contribuir com o projeto:

1. Clone o repositório.  
2. Crie um ambiente virtual: `uv venv`
3. Ative o ambiente: `source .venv/bin/activate`
4. Instale em modo editável: `uv pip install -e .`
5. Execute os testes com pytest: `pytest`

## **Licença**

Este projeto está licenciado sob a Licença MIT.