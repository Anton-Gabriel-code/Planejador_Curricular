from pyvis.network import Network


def html(G, ordem, arquivo="grade.html"):
    net = Network(height="750px", width="100%", directed=True, bgcolor="#bcbcfa")

    total = len(ordem)

    posicao = {disciplina: i for i, disciplina in enumerate(ordem)}

    for disciplina in G.nodes():
        i = posicao.get(disciplina, 0)

        ratio    = i / max(total - 1, 1)
        vermelho = int(255 * ratio)
        verde    = int(255 * (1 - ratio))
        cor      = f"#{vermelho:02x}{verde:02x}33"

        net.add_node(
            disciplina,
            label=disciplina,
            color=cor,
            title=f"Posição na sequência: {i + 1}"
        )

    # Adiciona as arestas
    for origem, destino in G.edges():
        net.add_edge(origem, destino)

    net.write_html(arquivo)
    print(f"Visualização salva em: {arquivo}")