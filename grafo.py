import networkx as nx


def construir_DAG(disciplinas):
    G = nx.DiGraph()

    for disciplina, prereqs in disciplinas.items():
        G.add_node(disciplina)

        for prereq in prereqs:

            G.add_edge(prereq, disciplina)
    return G


def verificar_ciclos(G):
    try:
        ciclo = nx.find_cycle(G, orientation ="original")
        return  [aresta[0] for aresta in ciclo]
    except nx.NetworkXNoCycle:
        return []
    
def ordenacao_topologica (G):

    return list(nx.topological_sort(G))

def prereqs_diretos(G, disciplina):
    return list(G.predecessors(disciplina))

def prereqs_transitivos(G, disciplina):
    return list(nx.ancestors(G, disciplina))

def disciplinas_desbloqueadas(G, disciplina):
    return list(nx.descendants(G, disciplina))

def caminho_entre(G, origem, destino):

    try:
        return nx.shortest_path(G, origem, destino)

    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None