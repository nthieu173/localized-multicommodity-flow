from typing import cast
from networkx import DiGraph
from matplotlib import pyplot as plt
import networkx as nx
import math
from matplotlib.animation import FuncAnimation


def calculate_heights(
    graph: DiGraph, flow: dict[tuple[str, str], dict[str, float]]
) -> dict[str, dict[str, float]]:
    """Calculate the heights of the node for each commodity."""
    heights: dict[str, dict[str, float]] = {node: {} for node in graph.nodes}
    for node in graph.nodes:
        if "demand" in graph.nodes[node]:
            for commodity in graph.nodes[node]["demand"]:
                if commodity not in heights[node]:
                    heights[node][commodity] = 0
                heights[node][commodity] += graph.nodes[node]["demand"][commodity]

    for edge in graph.edges:
        edge = cast(tuple[str, str], edge)
        source, target = edge
        for commodity in flow[edge]:
            if commodity not in heights[source]:
                heights[source][commodity] = 0

            if commodity not in heights[target]:
                heights[target][commodity] = 0

            heights[source][commodity] -= flow[edge][commodity]
            heights[target][commodity] += flow[edge][commodity]

    return heights


def calculate_congestion(
    graph: DiGraph, flow: dict[tuple[str, str], dict[str, float]]
) -> dict[tuple[str, str], float]:
    """Calculate the congestion of the edges for all commodities."""
    congestion: dict[tuple[str, str], float] = {}
    for edge in graph.edges:
        edge = cast(tuple[str, str], edge)
        sum_flow = sum(flow[edge].values())
        capacity = graph.edges[edge]["capacity"]
        congestion[edge] = max(0, sum_flow - capacity)
    return congestion


def calculate_potential_difference(
    graph: DiGraph, flow: dict[tuple[str, str], dict[str, float]]
) -> dict[tuple[str, str], dict[str, float]]:
    """Calculate the potential difference of the edges."""
    heights = calculate_heights(graph, flow)
    congestion = calculate_congestion(graph, flow)
    potential_difference: dict[tuple[str, str], dict[str, float]] = {}
    for edge in graph.edges:
        edge = cast(tuple[str, str], edge)
        source, target = edge
        potential_difference[edge] = {}
        for commodity in flow[edge]:
            potential_difference[edge][commodity] = (
                heights[source][commodity]
                - heights[target][commodity]
                - congestion[edge]
            )
    return potential_difference


def compute_gradient(
    graph: DiGraph,
    beta: float,
    current_flow: dict[tuple[str, str], dict[str, float]],
    current_potential_difference: dict[tuple[str, str], dict[str, float]],
    new_flow: dict[tuple[str, str], dict[str, float]],
    new_potential_difference: dict[tuple[str, str], dict[str, float]],
) -> float:
    """Compute the gradient of the flow."""
    gradient_numerator = 0
    gradient_denominator = 0
    for edge in graph.edges:
        edge = cast(tuple[str, str], edge)
        for commodity in current_flow[edge]:
            gradient_numerator += (
                current_potential_difference[edge][commodity]
                - new_potential_difference[edge][commodity]
            ) ** 2
            gradient_denominator += (
                current_flow[edge][commodity] - new_flow[edge][commodity]
            ) ** 2
    return beta * math.sqrt(gradient_numerator) / math.sqrt(gradient_denominator)


def iterate_localized_multicommodity_flow(
    graph: DiGraph,
    flow: dict[tuple[str, str], dict[str, float]],
    beta: float,
    mu: float,
    nu: float,
) -> tuple[dict[tuple[str, str], dict[str, float]], float]:
    """
    A single iteration of the localized multicommodity flow algorithm.

    Returns the new flow and the updated beta.
    """
    current_potential_difference = calculate_potential_difference(graph, flow)

    new_flow: dict[tuple[str, str], dict[str, float]] = {}
    for edge in graph.edges:
        edge = cast(tuple[str, str], edge)
        new_flow[edge] = {}
        for commodity in flow[edge]:
            new_flow[edge][commodity] = max(
                0,
                flow[edge][commodity]
                + beta * current_potential_difference[edge][commodity],
            )

    new_potential_difference = calculate_potential_difference(graph, new_flow)

    omega = compute_gradient(
        graph,
        beta,
        flow,
        current_potential_difference,
        new_flow,
        new_potential_difference,
    )

    while omega > nu:
        beta *= 0.8 / omega
        for edge in graph.edges:
            edge = cast(tuple[str, str], edge)
            new_flow[edge] = {}
            for commodity in flow[edge]:
                new_flow[edge][commodity] = max(
                    0,
                    flow[edge][commodity]
                    + beta * current_potential_difference[edge][commodity],
                )
        new_potential_difference = calculate_potential_difference(graph, new_flow)
        omega = compute_gradient(
            graph,
            beta,
            flow,
            current_potential_difference,
            new_flow,
            new_potential_difference,
        )

    if omega <= mu:
        beta *= 1.5

    return new_flow, beta


def rounded_flow(
    flow: dict[tuple[str, str], dict[str, float]]
) -> dict[tuple[str, str], dict[str, float]]:
    """Round the flow to two decimal places for display."""
    rounded_flow = {}
    for edge in flow:
        rounded_flow[edge] = {
            commodity: round(flow[edge][commodity], 2) for commodity in flow[edge]
        }
    return rounded_flow


def main() -> None:
    """Main function."""
    G = DiGraph()

    G.add_node("s_b", demand={"b": 3, "r": 0}, partition=0)
    G.add_node("s_r", demand={"b": 0, "r": 3}, partition=0)
    G.add_node("1", partition=1)
    G.add_node("3", partition=1)
    G.add_node("2", partition=2)
    G.add_node("4", partition=2)
    G.add_node("t_b", demand={"b": -3, "r": 0}, partition=3)
    G.add_node("t_r", demand={"b": 0, "r": -3}, partition=3)

    G.add_edge("s_b", "1", capacity=2)
    G.add_edge("s_b", "3", capacity=2)
    G.add_edge("s_r", "1", capacity=2)
    G.add_edge("s_r", "3", capacity=2)

    G.add_edge("1", "2", capacity=2)
    G.add_edge("1", "4", capacity=2)
    G.add_edge("3", "2", capacity=2)
    G.add_edge("3", "4", capacity=2)

    G.add_edge("2", "t_b", capacity=2)
    G.add_edge("2", "t_r", capacity=2)
    G.add_edge("4", "t_b", capacity=2)
    G.add_edge("4", "t_r", capacity=2)

    commodities = ["b", "r"]

    # Initialize flow to zero on all edges
    flow: dict[tuple[str, str], dict[str, float]] = {}
    for edge in G.edges:
        edge = cast(tuple[str, str], edge)
        flow[edge] = {commodity: 0 for commodity in commodities}

    layout = nx.multipartite_layout(G, subset_key="partition")

    fig, ax = plt.subplots()
    fig.set_figheight(10)
    fig.set_figwidth(20)

    beta = 1
    mu = 0.5
    nu = 0.9
    max_iterations = 10

    def init():
        nx.draw(
            G,
            with_labels=True,
            pos=layout,
            node_color=["blue", "red", "gray", "gray", "gray", "gray", "blue", "red"],
            edge_color="gray",
            font_weight="bold",
            node_size=2000,
            font_color="white",
        )
        nx.draw_networkx_edge_labels(
            G,
            pos=layout,
            label_pos=0.6,
            edge_labels=rounded_flow(flow),
            font_weight="bold",
        )

    def update(frame) -> None:
        ax.clear()
        ax.set_title(f"Iteration {frame + 1}")
        nonlocal flow, beta
        flow, beta = iterate_localized_multicommodity_flow(G, flow, beta, mu, nu)
        # Check for convergence, wich is having all potential differences close to zero
        potential_difference = calculate_potential_difference(G, flow)

        nx.draw(
            G,
            with_labels=True,
            pos=layout,
            node_color=["blue", "red", "gray", "gray", "gray", "gray", "blue", "red"],
            edge_color="gray",
            font_weight="bold",
            node_size=2000,
            font_color="white",
        )
        nx.draw_networkx_edge_labels(
            G,
            pos=layout,
            label_pos=0.6,
            edge_labels=rounded_flow(flow),
            font_weight="bold",
        )

    ani = FuncAnimation(
        fig=fig,
        init_func=init,  # type: ignore
        func=update,  # type: ignore
        frames=max_iterations,
        repeat_delay=2000,
        interval=1000,
    )

    ani.save("../images/localized_multicommodity_flow.gif")


if __name__ == "__main__":
    main()
