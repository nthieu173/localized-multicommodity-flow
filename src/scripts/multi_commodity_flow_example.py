import networkx as nx
from matplotlib import pyplot as plt


def main():
    G = nx.DiGraph()

    G.add_node("s_b", demand=2, partition=0)
    G.add_node("s_r", demand=3, partition=0)
    G.add_node("1", partition=1)
    G.add_node("3", partition=1)
    G.add_node("2", partition=2)
    G.add_node("4", partition=2)
    G.add_node("t_b", demand=-2, partition=3)
    G.add_node("t_r", demand=-3, partition=3)

    G.add_edge("s_b", "1", capacity=2, weight=0)
    G.add_edge("s_b", "3", capacity=2, weight=0)
    G.add_edge("s_r", "1", capacity=3, weight=0)
    G.add_edge("s_r", "3", capacity=3, weight=0)

    G.add_edge("1", "2", capacity=3, weight=1)
    G.add_edge("1", "4", capacity=3, weight=3)
    G.add_edge("3", "2", capacity=3, weight=3)
    G.add_edge("3", "4", capacity=3, weight=1)

    G.add_edge("2", "t_b", capacity=2, weight=0)
    G.add_edge("2", "t_r", capacity=2, weight=0)
    G.add_edge("4", "t_b", capacity=3, weight=0)
    G.add_edge("4", "t_r", capacity=3, weight=0)

    nx.draw(
        G,
        with_labels=True,
        pos=nx.multipartite_layout(G, subset_key="partition"),
        node_color=["blue", "red", "gray", "gray", "gray", "gray", "blue", "red"],
        node_size=2000,
        font_color="white",
    )

    plt.savefig("../images/multi_commodity_flow_example.png")


if __name__ == "__main__":
    main()
