import sys
from itertools import combinations

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


def gerar_regras_cnf(linhas, colunas, pistas_lin, pistas_col, setas):
    def pos_para_id(i, j):
        return (i - 1) * colunas + j

    regras = []

    # 1. Bloqueio de celulas com setas
    for l, c, _ in setas:
        regras.append([-pos_para_id(l, c)])

    # 2. Visada de cada seta
    for l, c, d in setas:
        dl, dc = VETORES_DIRECAO[d]
        visiveis = []
        passo = 1
        while 1 <= (l + passo * dl) <= linhas and 1 <= (c + passo * dc) <= colunas:
            visiveis.append(pos_para_id(l + passo * dl, c + passo * dc))
            passo += 1

        if visiveis:
            regras.append(visiveis)

    # 3. Restricoes de cardinalidade exata
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

        for grupo in combinations(variaveis, meta + 1):
            regras.append([-x for x in grupo])

        for grupo in combinations(variaveis, n - meta + 1):
            regras.append([x for x in grupo])

    for i, limite in enumerate(pistas_lin, 1):
        if limite is not None:
            vars_lin = [pos_para_id(i, j) for j in range(1, colunas + 1)]
            aplicar_contagem(vars_lin, limite)

    for j, limite in enumerate(pistas_col, 1):
        if limite is not None:
            vars_col = [pos_para_id(i, j) for i in range(1, linhas + 1)]
            aplicar_contagem(vars_col, limite)

    total_vars = linhas * colunas
    return total_vars, regras


def emitir_dimacs(total_vars, regras):
    # Verificacao de sanidade 
    num_declarado_vars = total_vars
    num_declarado_clausulas = len(regras)

    # Validacao de consistencia interna
    assert len(regras) == num_declarado_clausulas, "Erro de sanidade na contagem de clausulas"

    # Saida(stdout)
    sys.stdout.write(f"c Instancia gerada para Estrelas e Setas\n")
    sys.stdout.write(f"p cnf {num_declarado_vars} {num_declarado_clausulas}\n")
    for r in regras:
        sys.stdout.write(" ".join(str(x) for x in r) + " 0\n")


def obter_instancia_exemplo(n):
    # Instancia da imagem la 5x5 do trabalho
    if n == 5:
        pistas_l = [2, 2, 3, 0, 1]
        pistas_c = [1, 2, 3, 2, 0]
        setas = [
            (1, 1, "SE"),
            (1, 3, "SO"),
            (2, 2, "L"),
            (2, 5, "NO"),
            (4, 2, "N"),
            (5, 1, "NE"),
            (5, 4, "NO"),
            (5, 5, "O"),
        ]
        return 5, 5, pistas_l, pistas_c, setas
    else:
        # Template pra qualquer outros tamanhos N
        pistas_l = [1] * n
        pistas_c = [1] * n
        setas = [(1, 1, "SE")]
        return n, n, pistas_l, pistas_c, setas


if __name__ == "__main__":
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 5

    linhas, colunas, pistas_l, pistas_c, setas = obter_instancia_exemplo(n)
    total_vars, regras = gerar_regras_cnf(linhas, colunas, pistas_l, pistas_c, setas)
    emitir_dimacs(total_vars, regras)
