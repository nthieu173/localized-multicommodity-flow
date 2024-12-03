# Mathematical notations

Much like the single-commodity flow problem, the multi-commodity flow problem can be formulated as a linear program. The multi-commodity flow problem can be defined with the following constraints:
- The sum of the flow for all commodities on each edge must be less than or equal to the capacity of the edge:

    \\[
    \sum_{k \in \mathcal{K}} f_{ij,k} \leq u_{ij}, \quad \forall (i, j) \in E
    \\]

- The flow for all commodities at each node must be conserved, except for the source and sink nodes of each commodity.

    \\[
    \sum_{j \in \delta^+(i)} f_{ij,k} - \sum_{j \in \delta^-(i)} f_{ji,k} =
    \hat{\Delta}_{ik}, \quad \forall k \in \mathcal{K}, \; i \in V
    \\]

    where \\( \hat{\Delta}_{ik} \\) is defined as:

    \\[
    \hat{\Delta}_{ik} = 
    \begin{cases} 
    0, & \text{if } i \in V \setminus \{s_k, t_k\} \\\\
    d_k, & \text{if } i = s_k \\\\
    -d_k, & \text{if } i = t_k.
    \end{cases}
    \\]

- The flow for all commodities on each edge must be non-negative.

    \\[
    f_{ij,k} \geq 0, \quad \forall k \in \mathcal{K}, \quad (i, j) \in E
    \\]

Here, we have:
- \\(\mathcal{K}\\) is the set of all commodities.
- \\(V\\) is the set of all nodes.
- \\(E\\) is the set of all edges.
- \\(f_{ij,k}\\) is the flow on edge \\((i, j)\\) for commodity \\(k\\).
- \\(u_{ij}\\) is the capacity of edge \\((i, j)\\).
- \\(d_k\\) is the demand of commodity \\(k\\).
- \\( \hat{\Delta}_{ik} \\) is a correction term used to account for the added or removed flow at the source and sink nodes of each commodity.
- \\(\delta^+(i)\\) and \\(\delta^-(i)\\) are the sets of edges that are incident to node \\(i\\) in the forward and backward directions, respectively.
