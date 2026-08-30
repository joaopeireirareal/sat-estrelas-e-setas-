# Resolução do Puzzle Estrelas e Setas via SAT Solver

Este repositório contém a implementação do gerador de instâncias em formato DIMACS CNF e o pipeline de testes empíricos com SAT solver para o problema **Estrelas e Setas** (*Stars and Arrows*).

---

## Requisitos

- **Python 3.8+**
- Biblioteca **PySAT** (necessária para executar o solver integrado)

Para instalar a biblioteca no seu ambiente:

```bash
pip install python-sat
```
Estrutura do Repositório
estrelaeseta.py: Gerador de instâncias DIMACS CNF com verificação de sanidade do cabeçalho e suporte a parâmetros de linha de comando.

experimentos.py: Bateria de testes automatizados (4x4 até 8x8) com medição de tempo e reconstrução das matrizes resolvidas.

Instruções de Uso
1. Gerar arquivo CNF (DIMACS)
O gerador recebe o tamanho da grade como argumento e imprime o CNF no formato padrão, permitindo redirecionar para um arquivo .cnf:

```Bash
python estrelaeseta.py 5 > instancia_5x5.cnf
2. Executar os Experimentos com o Solver CaDiCaL
Para rodar as instâncias de teste, coletar as métricas de tempo de CPU e ver as soluções impressas:
```
```Bash
python experimentos.py
Ferramentas Utilizadas
Linguagem: Python 3
```
Solver SAT: CaDiCaL 1.5.3 (via PySAT)

Codificação: Direct Binomial Encoding (via itertools.combinations)


---

