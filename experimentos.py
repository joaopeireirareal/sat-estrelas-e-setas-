import time
from itertools import combinations
from pysat.solvers import Solver

# offsets de linha e coluna pra cada direcao
VETORES_DIRECAO = {
    "N": (-1, 0),
    "NE": (-1, 1),
    "L": (0, 1),
    "SE": (1, 1),
    "S": (1, 0),
    "SO": (1, -1),
    "O": (0, -1),
    "NO": (-1, -1),
}


def gerar_cnf(linhas, colunas, pistas_lin, pistas_col, setas):
    # converte coordenada da matriz em id 1D pra variavel booleana
    def pos_para_id(i, j):
        return (i - 1) * colunas + j

    regras = []

    # onde tem seta nao pode colocar estrela
    for l, c, _ in setas:
        regras.append([-pos_para_id(l, c)])

    # pega as casas na mira de cada seta ate a borda
    for l, c, d in setas:
        dl, dc = VETORES_DIRECAO[d]
        visiveis = []
        passo = 1
        while 1 <= (l + passo * dl) <= linhas and 1 <= (c + passo * dc) <= colunas:
            visiveis.append(pos_para_id(l + passo * dl, c + passo * dc))
            passo += 1

        # pelo menos uma dessas casas precisa ter estrela
        if visiveis:
            regras.append(visiveis)

    # restricoes pra bater a quantidade exata de estrelas
    def aplicar_contagem(variaveis, meta):
        n = len(variaveis)
        if meta == 0:
            for v in variaveis:
                regras.append([-v])
            return
        if meta == n:
            for v in variaveis:
                regras.append([v])
            return

        # no maximo meta estrelas
        for grupo in combinations(variaveis, meta + 1):
            regras.append([-x for x in grupo])

        # no minimo meta estrelas
        for grupo in combinations(variaveis, n - meta + 1):
            regras.append([x for x in grupo])

    # aplica as regras pras linhas
    for i, limite in enumerate(pistas_lin, 1):
        if limite is not None:
            vars_lin = [pos_para_id(i, j) for j in range(1, colunas + 1)]
            aplicar_contagem(vars_lin, limite)

    # aplica as regras pras colunas
    for j, limite in enumerate(pistas_col, 1):
        if limite is not None:
            vars_col = [pos_para_id(i, j) for i in range(1, linhas + 1)]
            aplicar_contagem(vars_col, limite)

    return linhas * colunas, regras


def renderizar_solucao(linhas, colunas, setas, solucao):
    dict_setas = {(l, c): d for l, c, d in setas}
    conj_sol = set(solucao)

    linhas_str = []
    for i in range(1, linhas + 1):
        linha = []
        for j in range(1, colunas + 1):
            vid = (i - 1) * colunas + j
            if (i, j) in dict_setas:
                linha.append(f"[{dict_setas[(i, j)]:^2}]")
            elif vid in conj_sol:
                linha.append("[ *]")
            else:
                linha.append("[ .]")
        linhas_str.append(" ".join(linha))
    return "\n".join(linhas_str)


# 5 testes com tamanhos diferentes pra bater o requisito do relatorio
INSTANCIAS = [
    {
        "nome": "Instância 1 (4x4)",
        "dim": (4, 4),
        "lin": [1, 2, 1, 0],
        "col": [1, 1, 2, 0],
        "setas": [(1, 1, "SE"), (2, 2, "L"), (4, 1, "NE")],
    },
    {
        "nome": "Instância 2 (5x5 - Original)",
        "dim": (5, 5),
        "lin": [2, 2, 3, 0, 1],
        "col": [1, 2, 3, 2, 0],
        "setas": [
            (1, 1, "SE"),
            (1, 3, "SO"),
            (2, 2, "L"),
            (2, 5, "NO"),
            (4, 2, "N"),
            (5, 1, "NE"),
            (5, 4, "NO"),
            (5, 5, "O"),
        ],
    },
    {
        "nome": "Instância 3 (6x6)",
        "dim": (6, 6),
        "lin": [2, 1, 3, 1, 0, 2],
        "col": [1, 2, 2, 1, 3, 0],
        "setas": [
            (1, 2, "S"),
            (2, 6, "O"),
            (3, 3, "SE"),
            (4, 1, "L"),
            (5, 5, "NO"),
            (6, 4, "N"),
        ],
    },
    {
        "nome": "Instância 4 (7x7)",
        "dim": (7, 7),
        "lin": [2, 2, 1, 3, 0, 2, 1],
        "col": [1, 3, 0, 2, 2, 1, 2],
        "setas": [
            (1, 1, "SE"),
            (1, 7, "SO"),
            (2, 3, "L"),
            (3, 5, "S"),
            (4, 2, "NE"),
            (5, 4, "NO"),
            (6, 7, "O"),
            (7, 1, "N"),
        ],
    },
    {
        "nome": "Instância 5 (8x8)",
        "dim": (8, 8),
        "lin": [2, 3, 1, 2, 0, 3, 1, 2],
        "col": [2, 1, 3, 0, 2, 2, 3, 1],
        "setas": [
            (1, 1, "SE"),
            (2, 4, "L"),
            (3, 8, "SO"),
            (4, 2, "N"),
            (5, 6, "NO"),
            (6, 1, "NE"),
            (7, 5, "S"),
            (8, 8, "O"),
        ],
    },
]


def rodar_testes():
    print(f"{'Instância':<25} | {'Vars':<6} | {'Cláusulas':<10} | {'Status':<8} | {'Tempo (ms)':<10}")
    print("-" * 72)

    for inst in INSTANCIAS:
        r, c = inst["dim"]
        n_vars, cnf = gerar_cnf(r, c, inst["lin"], inst["col"], inst["setas"])

        # roda o solver e mede o tempo de resolucao
        inicio = time.perf_counter()
        with Solver(name="cadical153", bootstrap_with=cnf) as solver:
            satisfativel = solver.solve()
            tempo_ms = (time.perf_counter() - inicio) * 1000

            status_str = "SAT" if satisfativel else "UNSAT"
            print(f"{inst['nome']:<25} | {n_vars:<6} | {len(cnf):<10} | {status_str:<8} | {tempo_ms:<10.3f}")

            # se achou modelo, desenha a grade com as estrelas
            if satisfativel:
                modelo = solver.get_model()
                estrelas = [v for v in modelo if v > 0]
                grid_visual = renderizar_solucao(r, c, inst["setas"], estrelas)
                print(f"\nSolução reconstruída para {inst['nome']}:")
                print(grid_visual)
                print("-" * 72)


if __name__ == "__main__":
    rodar_testes()
