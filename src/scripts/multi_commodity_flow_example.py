import networkx as nx
from matplotlib import pyplot as plt
from numpy import partition

# \begin{figure}[ht]
#     \centering
#     \begin{tikzpicture}[node distance=4cm,
#             every path/.style={->,thick}]
#         % Nodes
#         \node[network] (s_b) [fill=blue!30] {$s_b$};
#         \node[network] (s_r) [fill=red!30, below of=s_b] {$s_r$};

#         \node[network] (1) [right of=s_b] {$1$};
#         \node[network] (2) [right of=1] {$2$};
#         \node[network] (3) [right of=s_r] {$3$};
#         \node[network] (4) [right of=3] {$4$};

#         \node[network] (r_b) [fill=blue!30, right of=2] {$r_b$};
#         \node[network] (r_r) [fill=red!30, right of=4] {$r_r$};

#         % Edges
#         \draw (s_b) -- node[above] {\textcolor{blue}{$b_1$},\textcolor{red}{$0$}/$\infty$} (1);
#         \draw (s_b) -- node[above right] {\textcolor{blue}{$b_3$},\textcolor{red}{$0$}/$\infty$} (3);
#         \draw (s_r) -- node[below] {\textcolor{blue}{$0$},\textcolor{red}{$r_3$}/$\infty$} (3);
#         \draw (s_r) -- node[below right] {\textcolor{blue}{$0$},\textcolor{red}{$r_1$}/$\infty$} (1);

#         \draw (1) -- node[above] {\textcolor{blue}{$b_{12}$},\textcolor{red}{$r_{12}$}/$c_{12}$} (2);
#         \draw (1) -- node[above right] {\textcolor{blue}{$b_{32}$},\textcolor{red}{$r_{32}$}/$c_{32}$} (4);
#         \draw (3) -- node[below] {\textcolor{blue}{$b_{34}$},\textcolor{red}{$r_{34}$}/$c_{34}$} (4);
#         \draw (3) -- node[below right] {\textcolor{blue}{$b_{14}$},\textcolor{red}{$r_{14}$}/$c_{14}$} (2);


#         \draw (2) -- node[above] {\textcolor{blue}{$b_{r2}$},\textcolor{red}{$0$}/$\infty$} (r_b);
#         \draw (2) -- node[above right] {\textcolor{blue}{$b_{r4}$},\textcolor{red}{$0$}/$\infty$} (r_r);
#         \draw (4) -- node[below] {\textcolor{blue}{$0$},\textcolor{red}{$r_{r4}$}/$\infty$} (r_r);
#         \draw (4) -- node[below right] {\textcolor{blue}{$0$},\textcolor{red}{$r_{r2}$}/$\infty$} (r_b);
#     \end{tikzpicture}
# \end{figure}

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
