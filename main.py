from dados import DISCIPLINAS
from grafo import (
    construir_DAG,
    verificar_ciclos,
    ordenacao_topologica,
    prereqs_diretos,
    prereqs_transitivos,
    disciplinas_desbloqueadas,
    caminho_entre
)
from visualizer import html


def menu():
    print("\n" + "=" * 50)
    print("   PLANEJADOR DE MATRIZ CURRICULAR")
    print("=" * 50)
    print("  [1] Ver sequência válida de disciplinas")
    print("  [2] Consultar pré-requisitos de uma disciplina")
    print("  [3] Ver caminho entre duas disciplinas")
    print("  [4] Simular erro de ciclo na grade")
    print("  [5] Exportar visualização HTML")
    print("  [0] Sair")
    print("=" * 50)
    return input("  Escolha: ").strip()


def main():
    G = construir_DAG(DISCIPLINAS)

    # Verifica ciclos antes de qualquer coisa
    ciclo = verificar_ciclos(G)
    if ciclo:
        print("\nERRO: Ciclo detectado na grade!")
        print("Disciplinas envolvidas:", " -> ".join(ciclo))
        return

    ordem = ordenacao_topologica(G)

    while True:
        opcao = menu()

        if opcao == "1":
            print("\nSequência válida de estudos:\n")
            for i, disciplina in enumerate(ordem, 1):
                prereqs = prereqs_diretos(G, disciplina)
                if prereqs:
                    print(f"  {i:2}. {disciplina}")
                    print(f"      Requer: {', '.join(prereqs)}")
                else:
                    print(f"  {i:2}. {disciplina}  (sem pré-requisitos)")

        elif opcao == "2":
            nome = input("\nNome da disciplina: ").strip()
            if nome not in G:
                print(f"Disciplina '{nome}' não encontrada.")
            else:
                diretos    = prereqs_diretos(G, nome)
                transitivos = prereqs_transitivos(G, nome)
                desbloqueadas = disciplinas_desbloqueadas(G, nome)

                print(f"\nPré-requisitos diretos de '{nome}':")
                if diretos:
                    for d in diretos:
                        print(f"  - {d}")
                else:
                    print("  Nenhum.")

                print(f"\nTodos os pré-requisitos (incluindo indiretos):")
                if transitivos:
                    for d in transitivos:
                        print(f"  - {d}")
                else:
                    print("  Nenhum.")

                print(f"\nDisciplinas que dependem de '{nome}':")
                if desbloqueadas:
                    for d in desbloqueadas:
                        print(f"  - {d}")
                else:
                    print("  Nenhuma.")

        elif opcao == "3":
            origem  = input("\nDisciplina de origem: ").strip()
            destino = input("Disciplina de destino: ").strip()
            caminho = caminho_entre(G, origem, destino)

            if caminho:
                print("\nCaminho encontrado:")
                print("  " + " -> ".join(caminho))
            else:
                print("\nNão há caminho entre essas disciplinas.")

        elif opcao == "4":
            print("\nSimulando ciclo: adicionando aresta TCC -> Fundamentos da Programação...")
            G.add_edge("TCC", "Fundamentos da Programação")
            ciclo = verificar_ciclos(G)
            if ciclo:
                print("Ciclo detectado:", " -> ".join(ciclo))
            G.remove_edge("TCC", "Fundamentos da Programação")
            print("Aresta removida. Grade restaurada.")

        elif opcao == "5":
            html(G, ordem)

        elif opcao == "0":
            print("\nSaindo...")
            break

        else:
            print("Opção inválida.")


main()