from collections import deque


class GrafoCurricular:
    """DAG com listas de adjacência; evita overhead do NetworkX em grafos pequenos."""

    __slots__ = ("_pred", "_succ", "_ordem", "_memo_anc", "_memo_desc")

    def __init__(self, disciplinas: dict[str, list[str]]) -> None:
        self._pred: dict[str, set[str]] = {}
        self._succ: dict[str, set[str]] = {}
        self._ordem: list[str] | None = None
        self._memo_anc: dict[str, list[str]] = {}
        self._memo_desc: dict[str, list[str]] = {}

        for disciplina, prereqs in disciplinas.items():
            self._pred.setdefault(disciplina, set())
            self._succ.setdefault(disciplina, set())
            for prereq in prereqs:
                self._pred.setdefault(prereq, set())
                self._succ.setdefault(prereq, set())
                self._pred[disciplina].add(prereq)
                self._succ[prereq].add(disciplina)

    def _invalidar_cache(self) -> None:
        self._ordem = None
        self._memo_anc.clear()
        self._memo_desc.clear()

    def nodes(self):
        return self._pred.keys()

    def edges(self):
        for origem, destinos in self._succ.items():
            for destino in destinos:
                yield origem, destino

    def add_edge(self, origem: str, destino: str) -> None:
        self._pred.setdefault(origem, set())
        self._pred.setdefault(destino, set())
        self._succ.setdefault(origem, set())
        self._succ.setdefault(destino, set())
        if destino not in self._succ[origem]:
            self._succ[origem].add(destino)
            self._pred[destino].add(origem)
            self._invalidar_cache()

    def remove_edge(self, origem: str, destino: str) -> None:
        if destino in self._succ.get(origem, ()):
            self._succ[origem].discard(destino)
            self._pred[destino].discard(origem)
            self._invalidar_cache()

    def __contains__(self, disciplina: str) -> bool:
        return disciplina in self._pred


def construir_DAG(disciplinas: dict[str, list[str]]) -> GrafoCurricular:
    return GrafoCurricular(disciplinas)


def _bfs(adj: dict[str, set[str]], inicio: str) -> list[str]:
    visitados: list[str] = []
    fila = deque(adj.get(inicio, ()))
    vistos = set(fila)

    while fila:
        no = fila.popleft()
        visitados.append(no)
        for vizinho in adj.get(no, ()):
            if vizinho not in vistos:
                vistos.add(vizinho)
                fila.append(vizinho)

    return visitados


def verificar_ciclos(G: GrafoCurricular) -> list[str]:
    estado: dict[str, int] = {}
    pai: dict[str, str] = {}

    def dfs(no: str) -> list[str] | None:
        estado[no] = 1
        for vizinho in G._succ.get(no, ()):
            if estado.get(vizinho) == 1:
                ciclo = [vizinho, no]
                atual = no
                while atual != vizinho:
                    atual = pai[atual]
                    ciclo.append(atual)
                ciclo.reverse()
                return ciclo
            if estado.get(vizinho, 0) == 0:
                pai[vizinho] = no
                encontrado = dfs(vizinho)
                if encontrado:
                    return encontrado
        estado[no] = 2
        return None

    for no in G.nodes():
        if estado.get(no, 0) == 0:
            ciclo = dfs(no)
            if ciclo:
                return ciclo
    return []


def _ordenacao_kahn(G: GrafoCurricular) -> list[str]:
    grau_entrada = {no: len(G._pred[no]) for no in G.nodes()}
    fila = deque(no for no, grau in grau_entrada.items() if grau == 0)
    ordem: list[str] = []

    while fila:
        no = fila.popleft()
        ordem.append(no)
        for sucessor in G._succ.get(no, ()):
            grau_entrada[sucessor] -= 1
            if grau_entrada[sucessor] == 0:
                fila.append(sucessor)

    return ordem


def ordenacao_topologica(G: GrafoCurricular) -> list[str]:
    if G._ordem is not None:
        return G._ordem
    G._ordem = _ordenacao_kahn(G)
    return G._ordem


def prereqs_diretos(G: GrafoCurricular, disciplina: str) -> list[str]:
    return sorted(G._pred.get(disciplina, ()))


def prereqs_transitivos(G: GrafoCurricular, disciplina: str) -> list[str]:
    if disciplina not in G._memo_anc:
        G._memo_anc[disciplina] = _bfs(G._pred, disciplina)
    return G._memo_anc[disciplina]


def disciplinas_desbloqueadas(G: GrafoCurricular, disciplina: str) -> list[str]:
    if disciplina not in G._memo_desc:
        G._memo_desc[disciplina] = _bfs(G._succ, disciplina)
    return G._memo_desc[disciplina]


def caminho_entre(G: GrafoCurricular, origem: str, destino: str) -> list[str] | None:
    if origem not in G or destino not in G:
        return None

    fila = deque([origem])
    pai = {origem: None}

    while fila:
        no = fila.popleft()
        if no == destino:
            caminho: list[str] = []
            atual: str | None = destino
            while atual is not None:
                caminho.append(atual)
                atual = pai[atual]
            caminho.reverse()
            return caminho

        for vizinho in G._succ.get(no, ()):
            if vizinho not in pai:
                pai[vizinho] = no
                fila.append(vizinho)

    return None
