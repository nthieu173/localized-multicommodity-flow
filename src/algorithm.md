# Algorithm

In its simplest form, the algorith is presented below.

## The potential difference reduction algorithm

1. Set up step size \\(\beta\\).

2. For \\(l = 0, 1, \dots\\), do

    1. Calculate the height \\(h^l_{ik}, \forall i \in V, k \in \mathcal{K}\\):

        \\[
        h^l_{ik} = \sum_{j \in \delta^-(i)} f^l_{ji,k} - \sum_{j \in \delta^+(i)} f^l_{ij,k} + \Delta_{ik}.
        \\]

    2. Calculate the congestion \\(\psi^l_{ij}, \forall (i, j) \in E\\):

        \\[
        \psi^l_{ij} = \sum_{k \in \mathcal{K}} f^l_{ij,k} + r^l_{ij} - u_{ij}.
        \\]

    3. Calculate the potential difference \\(\phi^l_{ij,k}, \forall (i, j) \in E, k \in \mathcal{K}\\):

        \\[
        \phi^l_{ij,k} = h^l_{ik} - h^l_{jk} - \psi^l_{ij}.
        \\]

    4. Update \\(f_{ij,k}^{l+1}, r_{ij}^{l+1}, \forall (i, j) \in E, k \in \mathcal{K}\\):
        \\[
        f_{ij,k}^{l+1} = \max\\{f^l_{ij,k} + \beta \phi^l_{ij,k}, 0\\},
        \\]
        \\[
        r_{ij}^{l+1} = \max\\{r^l_{ij} - \beta \psi^l_{ij}, 0\\}.
        \\]

3. End For

### Explanation

Most of the variables are the same as in the relaxation section, with some differences:
- \\(f^l_{ij,k}\\) is the flow on edge \\((i, j)\\) for commodity \\(k\\) at iteration \\(l\\).
- \\(r^l_{ij}\\) is the unused capacity on edge \\((i, j)\\) at iteration \\(l\\).

We now direct our attention toward \\(\beta\\), which is the step size. The paper has proven that to guarantee convergence, it must be constrained to the following:
\\[
    \beta \leq \frac{2\sigma}{\lambda_{\max}}
\\]

where \\(\sigma \in (0, 1)\\) is a constant and \\(\lambda_{\max}\\) is the largest eigenvalue of the matrix \\(Q^TQ\\), where \\(Q\\) is the directed incidence matrix of the graph.

However, for for graphs with very large \\(\lambda_{\max}\\), the step size \\(\beta\\) then can be constrained to be very small, which would lead to slow convergence.

Thus, in practice we would want to use a larger step size initially and then decrease it as the algorithm progresses. The author hence suggests an inexact line search method which will have an adaptive step size, presented below. 

## The inexact line search method

1. Set \\(\beta_0 = 1, \mu = 0.5, \nu = 0.9\\), given \\(f^0\\).
2. For \\(l = 0, 1, \dots\\), if the stopping criterion is not satisfied, do:
    1. Calculate \\(\phi(f^l)\\) by **Potential Difference Algorithm**.
    2. Update:
        \\[
        \hat{f}^l = \max\\{f^l + \beta^l \phi(f^l), 0\\};
        \\]
    3. Calculate \\(\phi(\hat{f}^l)\\) by **Potential Difference Algorithm**.
    4. Compute:
        \\[
        \omega^l = \beta^l \frac{\|\phi(f^l) - \phi(\hat{f}^l)\|_2}{\|f^l - \hat{f}^l\|_2}.
        \\]
    5. While \\(\omega^l > \nu\\), do:
        1. Update:
            \\[
            \beta^l := \beta^l \cdot \frac{0.8}{\omega^l};
            \\]
        2. Update:
            \\[
            \hat{f}^l = \max\\{f^l + \beta^l \phi(f^l), 0\\};
            \\]
        3. Calculate \\(\phi(\hat{f}^l)\\) by **Potential Difference Algorithm**.
        4. Recompute:
            \\[
            \omega^l = \beta^l \frac{\|\phi(f^l) - \phi(\hat{f}^l)\|_2}{\|f^l - \hat{f}^l\|_2}.
            \\]
    6. End while.
    7. Set:
        \\[
        f^{l+1} = \hat{f}^l;
        \\]
    8. Update:
        \\[
        \phi(f^{l+1}) = \phi(\hat{f}^l).
        \\]
    9. If \\(\omega^l \leq \mu\\), then:
        1. Update:
            \\[
            \beta^l := \beta^l \cdot 1.5.
            \\]
    10. End if.
3. End for.

### Potential Difference Algorithm


1. **Calculate the height** \\(h_{ik}, \forall i \in V, k \in \mathcal{K}\\):
    \\[
    h_{ik} = \sum_{j \in \delta^-(i)} f_{ji,k} - \sum_{j \in \delta^+(i)} f_{ij,k} + \Delta_{ik}.
    \\]

2. **Calculate the congestion function** \\(\psi_{ij}, \forall (i, j) \in E\\):
    \\[
    \psi_{ij} =
    \begin{cases}
    f_{ij} - u_{ij}, & \text{if } f_{ij} > u_{ij}, \\\\
    0, & \text{if } f_{ij} \leq u_{ij}.
    \end{cases}
    \\]

3. **Calculate the potential difference** \\(\phi_{ij,k}, \forall (i, j) \in E, k \in \mathcal{K}\\):
    \\[
    \phi_{ij,k} = h_{ik} - h_{jk} - \psi_{ij}.
    \\]
