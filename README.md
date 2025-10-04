# **CocomoPy: Estimador de Custo de Software**

CocomoPy é uma ferramenta de linha de comando (CLI) que estima o esforço, tempo e custo para desenvolver um projeto de software. A análise é baseada no modelo **COCOMO (Constructive Cost Model)** e utiliza o número de linhas de código-fonte (KLOC) de um projeto local como principal métrica.

## **Funcionalidades**

* **Análise Rápida:** Calcula o custo a partir de uma pasta de código-fonte local.  
* **Modelo COCOMO:** Utiliza o modelo COCOMO Básico e Intermediário.  
* **Modo Interativo:** Permite ajustar a estimativa com 15 "drivers de custo" para maior precisão (modo intermediário).  
* **Flexível:** Permite configurar o custo mensal de um desenvolvedor para se adequar à sua realidade.  
* **Interface Amigável:** Usa rich para exibir os resultados de forma clara e organizada.

## **Pré-requisitos**

* Python 3.8+  
* pip  
* **cloc:** Uma ferramenta externa para contar linhas de código. É essencial que o cloc esteja instalado e acessível no seu PATH.  
  * **Ubuntu/Debian:** sudo apt install cloc  
  * **macOS (Homebrew):** brew install cloc  
  * **Windows (Scoop):** scoop install cloc

## **Instalação**

Para instalar o CocomoPy e torná-lo disponível como um comando global no seu sistema, siga estes passos:

1. Clone este repositório (ou descarregue os ficheiros para uma pasta).  
2. Navegue até à pasta do projeto no seu terminal.  
3. Execute o seguinte comando para instalar a aplicação:  
   pip install .

   *Dica: Se preferir instalar apenas para o seu utilizador atual sem precisar de permissões de administrador, use pip install \--user .*  
4. Verifique se a instalação foi bem-sucedida:  
   cocomopy \--help

## **Como Usar**

O uso é simples. Basta executar o comando cocomopy seguido do caminho para a pasta do projeto que deseja analisar.

### **Exemplo (Modo Básico)**

cocomopy /caminho/para/meu/projeto

### **Exemplo (Modo Intermediário e com Custo Personalizado)**

O modo intermediário iniciará um assistente interativo para avaliar os drivers de custo.

cocomopy /caminho/para/meu/projeto \--intermediate \--cost-per-month 9500

## **Licença**

Este projeto está licenciado sob a Licença MIT. Veja o ficheiro LICENSE para mais detalhes.

## Roadmap and Status

The high-level ambitious plan for the project, in order:

|  #  | Step                                                       | Status |
| :-: | --------------------------------------------------------- | :----: |
|  1  | Cocomo basic calculation                                  |   ✅   |
|  2  | Cocomo intermediate calculation                           |   ✅   |
|  3  | Intuitive TUI                                             |   ⚠️   |
|  4  | Competitive performance                                   |   ⚠️   |
|  5  | Explainable AI (XAI) for cost drivers                     |   ❌   |
|  6  | Report generation (PDF, HTML, etc.)                       |   ❌   |
|  N  | Fancy features (to be expanded upon later)                |   ❌   |

