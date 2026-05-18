from pyvis.network import Network


def html(G, ordem, arquivo="grade.html"):
    net = Network(height="750px", width="100%", directed=True, bgcolor="#bcbcfa")

    total = len(ordem)
    escala = max(total - 1, 1)

    for i, disciplina in enumerate(ordem):
        ratio = i / escala
        vermelho = int(255 * ratio)
        verde = int(255 * (1 - ratio))
        net.add_node(
            disciplina,
            label=disciplina,
            color=f"#{vermelho:02x}{verde:02x}33",
            title=f"Posição na sequência: {i + 1}",
        )

    for origem, destino in G.edges():
        net.add_edge(origem, destino)

    net.write_html(arquivo)
    print(f"Visualização salva em: {arquivo}")