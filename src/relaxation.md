# Relaxation

The main idea of the algorithm devised by [Liu et al](https://doi.org/10.48550/arXiv.2108.07549) is to relax both the conservation of flow constraint on the vertices and the capacity constraint on the edges. This relaxation is done by introducing a **pseudo-flow**.

The **pseudo-flow**, defined as \\( \mathcal{f}: K \times E \to \mathbb{R}^+ \\), is a function that maps each commodity \\( k \in \mathcal{K} \\) and edge \\( (i, j) \in E \\) to a non-negative real number, which is just the same as that of a *real* flow. The main difference is that the pseudo-flow does not need to satisfy the constraints noted above.

Going forward, all \\( f_{ij,k} \\) will refer to the pseudo-flow unless otherwise noted.

## Height

Relaxing the conservation of flow constraint on the vertices, we keep track of the amount by which the flow going into a vertex exceeds the flow going out of it:

\\[
\Delta_{ik} = \sum_{j \in \delta^-(i)} f_{ji,k} - \sum_{j \in \delta^+(i)} f_{ij,k} + \hat{\Delta}_{ik}, \quad \forall i \in V, \; k \in \mathcal{K}
\\]

We now refer to this as the **height** of the vertex \\( i \\) for commodity \\( k \\).

\\[
    h_{ik} = \Delta_{ik}
\\]

We can see that the conservation of flow constraint will hold when the height of all vertices is zero.

## Congestion

Relaxing the capacity constraint on the edges, we keep track of the amount by which the flow on an edge exceeds its capacity:

\\[
\psi_{ij} = \begin{cases}
    f_{ij} - u_{ij}, & \text{if } f_{ij} > u_{ij} \\\\
    0, & \text{if } f_{ij} \leq u_{ij}
\end{cases}
\\]

where \\(f_{ij}\\) is just the sum of the pseudo-flows for all commodities on edge \\((i, j)\\):

\\[
    f_{ij} = \sum_{k \in \mathcal{K}} f_{ij,k}
\\]

We can see that the capacity constraint will hold when the congestion of all edges is zero.

## Potential difference

Now that we have defined the height and congestion, we can define the **potential difference** for each commodity \\( k \in \mathcal{K} \\) between two vertices \\( i \\) and \\( j \\):

\\[
    \phi_{ij,k} = h_{ik} - h_{jk} - \psi_{ij}
\\]

Intuitively, if the potential difference is positive, it means that the flow from \\( i \\) to \\( j \\) for commodity \\( k \\) is too low because of broken conservation of flow.

Conversely, if the potential difference is negative, it means that the flow from \\( i \\) to \\( j \\) for commodity \\( k \\) is too high because of broken conservation of flow *or* capacity constraint.

As noted, for both the flow conservation and capacity constraints to hold, all heights and congestions must be zero, which implies that the potential difference must be zero for all commodities on all edges in a feasible solution.

However, the converse is not necessarily true. A zero potential difference does not imply that the flow is feasible. This is because we could have a positive \\( h_{ik} - h_{jk} \\) (more flow going into \\( i \\) than going out of \\( j \\)) and a positive \\( \psi_{ij} \\) (flow on edge \\( (i, j) \\) exceeds its capacity) that cancel each other out. This implies that the flow is infeasible.

The above observations are indeed formalized in the following section.

## Stable pseudo-flow

In the paper, a **psuedo-flow** is a **stable psuedo-flow** if it satisfies the following conditions:
- For any used edge of commodity \\( k \\), the height difference between vertex \\( i \\) and vertex \\( j \\) for commodity \\( k \\) is equal to the congestion of edge \\((i, j)\\), i.e., the potential difference \\( \phi_{ij,k} \\) is zero.
- For any unused edge of commodity \\( k \\), the height difference between vertex \\( i \\) and vertex \\( j \\) is less than or equal to the congestion of edge \\((i, j)\\), i.e., the potential difference \\( \phi_{ij,k} \\) is less than or equal to zero.

where an edge \((i, j)\) is used by commodity \(k\) if \(f_{ij,k} > 0\).

### Zero stable pseudo-flow

A **stable pseudo-flow** is a **zero stable pseudo-flow** if it satisfies the following additional condition:
\\[
    \psi_{ij} = 0, h_{ik} = 0, \forall (i, j) \in E, i \in V, k \in \mathcal{K}
\\]

otherwise, it is a **non-zero stable pseudo-flow**.

From the above definitions, the author then proves the following theorem.

## Theorem

> There exists a feasible flow for the multi-commodity flow problem if and only if there exists zero-stable pseudo-flow.

In fact, if a non-zero stable pseudo-flow exists, then there is no feasible flow for the multi-commodity flow problem.
