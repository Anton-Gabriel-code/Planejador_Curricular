from dados import DISCIPLINAS
from grafo import construir_DAG, verificar_ciclos, ordenacao_topologica
from visualizer import html

G = construir_DAG(DISCIPLINAS)

ciclo = verificar_ciclos(G)


if ciclo:
    print("Ciclo detectado: ", ciclo)

else:
    ordem = ordenacao_topologica(G)
    for i, disciplina in enumerate(ordem, 1):
        print(i, disciplina)
    html(G, ordem)