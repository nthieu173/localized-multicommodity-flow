# Conclusion

In this report, we've examined the multi-commodity flow problem and a localized solution method proposed by [Liu et al](https://doi.org/10.48550/arXiv.2108.07549). The method is intuitive and seems to produce good results in practice, scaling well with the number of edges in the graph, as long as the graph is sparse.

Furthermore, because of the parallelizable nature of the algorithm, it is possible to entirely offset the increase in computation time due to the increase in the number of edges by using more computational resources, calculating the height, congestion, and potential difference for each edge and node in parallel.

Further research could be done implement the algorithm in a more performant language such as C++ or Rust, and compare its performance with more standard mixed-integer programming solvers. This would give a better idea of the algorithm's performance in practice.
