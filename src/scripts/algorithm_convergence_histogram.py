import random
from typing import cast
from networkx import DiGraph
from matplotlib import pyplot as plt
import networkx as nx
import math


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


def stopping_criteria(
    graph: DiGraph, flow: dict[tuple[str, str], dict[str, float]], tolerance: float
) -> bool:
    """
    Check if the stopping criteria is met, which is when
    the potential difference is close to zero.
    """
    potential_difference = calculate_potential_difference(graph, flow)
    for edge in graph.edges:
        edge = cast(tuple[str, str], edge)
        for commodity in flow[edge]:
            if potential_difference[edge][commodity] > tolerance:
                return False
    return True


def localized_multicommodity_flow(
    graph: DiGraph,
    flow: dict[tuple[str, str], dict[str, float]],
    beta: float,
    mu: float,
    nu: float,
    max_iterations: int,
) -> tuple[dict[tuple[str, str], dict[str, float]], int]:
    """
    The localized multicommodity flow algorithm.

    Returns the final flow, and the number of iterations it took to converge.
    """
    for i in range(max_iterations):
        if stopping_criteria(graph, flow, 0.01):
            return flow, i
        new_flow, beta = iterate_localized_multicommodity_flow(
            graph, flow, beta, mu, nu
        )
        flow = new_flow

    return flow, max_iterations


def generate_example(num_nodes: int, edge_probability: float, num_commodities: int):
    G: DiGraph = nx.gnp_random_graph(num_nodes, edge_probability, directed=True)

    commodities = [f"c{i}" for i in range(num_commodities)]

    # Pick random nodes as sources and sinks for each commodity
    for commodity in commodities:
        source = nx.utils.arbitrary_element(G.nodes)
        sink = nx.utils.arbitrary_element(G.nodes - {source})
        G.nodes[source]["demand"] = {commodity: 3}
        G.nodes[sink]["demand"] = {commodity: -3}

    # Pick random capacities for each edge
    for edge in G.edges:
        G.edges[edge]["capacity"] = random.randint(1, 5)

    # Initialize flow to zero on all edges
    flow: dict[tuple[str, str], dict[str, float]] = {}
    for edge in G.edges:
        edge = cast(tuple[str, str], edge)
        flow[edge] = {commodity: 0 for commodity in commodities}

    return G, flow


def generate_histogram(
    num_examples: int, num_nodes: int, edge_probability: float, max_iterations: int
):
    beta = 1
    mu = 0.5
    nu = 0.9

    iteration_to_convergence: list[int] = []
    for _ in range(num_examples):
        print(_)
        G, flow = generate_example(num_nodes, edge_probability, 3)
        _, iterations = localized_multicommodity_flow(
            G, flow, beta, mu, nu, max_iterations
        )
        iteration_to_convergence.append(iterations)
    plt.clf()
    plt.hist(iteration_to_convergence, bins=range(1, max_iterations + 1))
    plt.xlabel("Iterations")
    plt.ylabel("Frequency")
    plt.title(f"Histogram of Iterations to Convergence for {num_nodes} Nodes")
    plt.savefig(f"../images/algorithm_convergence_histogram_{num_nodes}.png")

    return iteration_to_convergence


def main():
    ten_iterations = generate_histogram(100, 10, 0.3, 100)
    hundred_iterations = generate_histogram(100, 100, 0.03, 200)
    five_hundreds_iterations = generate_histogram(100, 500, 0.006, 200)

    mean_ten_iterations = sorted(ten_iterations)[len(ten_iterations) // 2]
    mean_hundred_iterations = sorted(hundred_iterations)[len(hundred_iterations) // 2]
    mean_five_hundreds_iterations = sorted(five_hundreds_iterations)[
        len(five_hundreds_iterations) // 2
    ]

    plt.clf()
    plt.plot(
        [10, 100, 500],
        [
            mean_ten_iterations,
            mean_hundred_iterations,
            mean_five_hundreds_iterations,
        ],
    )
    plt.plot(
        [10, 100, 500],
        [
            sum(ten_iterations) / len(ten_iterations),
            sum(hundred_iterations) / len(hundred_iterations),
            sum(five_hundreds_iterations) / len(five_hundreds_iterations),
        ],
    )
    plt.xscale("log")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Iterations to Convergence")
    plt.title("Iterations to Convergence vs Number of Nodes")
    plt.legend(["Median", "Mean"])

    plt.savefig("../images/algorithm_convergence_histogram_mean.png")


if __name__ == "__main__":
    main()
