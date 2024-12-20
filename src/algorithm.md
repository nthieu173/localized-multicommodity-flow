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

This algorithm follows much of the analysis on our previous section. After calculating the potential difference, we update the flow on each edge by some fraction of the potential difference, governed by the step size.

We now direct our attention toward \\(\beta\\), which is the step size. To guarantee convergence, it must be constrained by the following condition:
\\[
    \beta \leq \frac{2\sigma}{\lambda_{\max}}
\\]

where \\(\sigma \in (0, 1)\\) is a constant and \\(\lambda_{\max}\\) is the largest eigenvalue of the matrix \\(Q^TQ\\), where \\(Q\\) is the directed incidence matrix of the graph.

However, for for graphs with very large \\(\lambda_{\max}\\), the step size \\(\beta\\) then can be constrained to be very small, which would lead to slow convergence.

Thus, in practice we would want to use a larger step size when the potential difference is high and then decrease it as the algorithm progresses and the potential difference of each edge approaches zero. The author hence suggests an inexact line search method which will have an adaptive step size, presented below. 

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

### Remarks

Looking at step 2.4, we can see that \\(\omega^l\\) is created by multiplying the step size \\(\beta^l\\) by the gradient of the potential difference. This makes it a gradient projection method and is known to converge to a local minimum.

We note four hyperparameters in the inexact line search method:
- \\(\mu = 0.5\\) is the lower bound for \\(\omega^l\\). When \\(\omega^l\\) is below this value, the step size is increased.
- \\(\nu = 0.9\\) is the upper bound for \\(\omega^l\\). When \\(\omega^l\\) is above this value, the step size is decreased.
- 0.8 is the factor by which the step size is decreased when \\(\omega^l\\) is above \\(\nu\\).
- 1.5 is the factor by which the step size is increased when \\(\omega^l\\) is below \\(\mu\\).

These factors were chosen according to this paper: [Improvements of Some Projection Methods for Monotone Nonlinear Variational Inequalities](https://doi.org/10.1023/A:1013096613105) by He, B.S., Liao, L.Z.. The author seems to have made two slight changes compared to the original paper:
- \\(\mu\\) was increased from 0.4 to 0.5.
- The decrease factor was changed from 2/3 to 0.8.

It is unclear why these changes were made, but they might have been made according to empirical results from the author's experiments.

There is also the inclusion of the stopping criterion, which is not detailed in the paper. However, from the relaxation, we can devise a reasonable stopping criteria: when the **stable pseudo-flow** is reached, or in other word when \\(\psi_{ij}\\) is close to zero for all \\((i, j) \in E\\).

## Implementation

The algorithm is implemented in Python and can be found in the [scripts folder of the repository](https://github.com/nthieu173/localized-multicommodity-flow/blob/main/src/scripts/localized_multicommodity_flow.py).

![Algorithm implementation example](./images/localized_multicommodity_flow.gif)
