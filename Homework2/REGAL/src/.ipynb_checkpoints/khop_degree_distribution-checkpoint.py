"""Get k-hop degree distributions from graph."""

import argparse
import numpy as np
import sys
from time import perf_counter

import networkx as nx


def get_khop_degree_distribution(graph, k):
    degree_stats = []
    for node in graph.nodes:
        subgraph = nx.generators.ego.ego_graph(graph, node, radius = k)
        degrees = np.array([graph.degree[nbr] for nbr in subgraph.nodes])
        node_degree_stats = np.array(
            [degrees.min(), np.median(degrees), np.mean(degrees), degrees.max()]
        )
        degree_stats.append(node_degree_stats)
    return(np.array(degree_stats))


def main():
    descrip = "Get k-hop degree distributions from graph."
    parser = argparse.ArgumentParser(description = descrip)
    parser.add_argument('input', type = str, 
                       help = "Edgelist file containing input graph.")
    parser.add_argument('output', type = str,
                       help = "Path to save output array.")
    parser.add_argument('-k', '--kmin', type = int, default = 1, 
                       help = "Number of hops.")
    parser.add_argument('--kmax', type = int, default = None, 
                       help = "Range of k-hops to compute.")
    parser.add_argument('--delimiter', type = str, default = ',',
                       help = "Delimiter for input edgelist file.")
    args = parser.parse_args()
    
    graph = nx.read_edgelist(args.input, create_using = nx.Graph(), 
                             delimiter = args.delimiter)
    
    
    if args.kmax is None:
        args.kmax = args.kmin
    
    degree_distributions = []
    for k in range(args.kmin, args.kmax + 1):
        print(f"Searching for {k}-hop degree distributions...")
        start = perf_counter()
        distribution_k = get_khop_degree_distribution(graph, k)
        stop = perf_counter()
        print(f"Found {k}-hop degree distributions in {stop-start:.2f} s.")
        degree_distributions.append(distribution_k)
    
    combined_distributions = np.hstack(tuple(degree_distributions))
    np.savetxt(args.output, combined_distributions, delimiter = ",")
    
    return


if __name__ == "__main__":
    sys.exit(main())