"""
Girvan-Newman Community Detection in social media
Author: Vishant

"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import time
import csv
import os
from collections import defaultdict
from networkx.algorithms.community.quality import modularity

class DatasetLoader:
    """
    Handles loading of different types of datasets.
    """

    def __init__(self, dataset_type="karate", file_path=None):
        self.dataset_type = dataset_type
        self.file_path = file_path

    def load(self):

        if self.dataset_type == "karate":
            print("Loading Zachary Karate Club dataset...")
            G = nx.karate_club_graph()

        elif self.dataset_type == "csv":
            if not self.file_path:
                raise ValueError("CSV file path required.")

            print(f"Loading CSV dataset from {self.file_path}...")
            df = pd.read_csv(self.file_path)
            G = nx.from_pandas_edgelist(df, "source", "target")

        elif self.dataset_type == "snap":
            if not self.file_path:
                raise ValueError("File path required for SNAP dataset.")

            print(f"Loading SNAP dataset from {self.file_path}...")

            G = nx.read_edgelist(
                self.file_path,
                nodetype=int,
                create_using=nx.Graph()
            )

        else:
            raise ValueError("Unsupported dataset type.")

        print("Dataset loaded successfully.")
        print("Total Nodes:", G.number_of_nodes())
        print("Total Edges:", G.number_of_edges())
        print("-----------------------------------\n")

        return G

class GraphAnalyzer:
    """
    Provides basic graph statistics.
    """
    def __init__(self, graph):
        self.graph = graph

    def print_basic_stats(self):
        print("----- Graph Statistics -----")
        print("Nodes:", self.graph.number_of_nodes())
        print("Edges:", self.graph.number_of_edges())
        print("Density:", nx.density(self.graph))
        print("Average Clustering:", nx.average_clustering(self.graph))
        print("----------------------------\n")

class GirvanNewmanDetector:
    """
    Performs Girvan-Newman Community Detection.
    """

    def __init__(self, graph):
        self.original_graph = graph
        self.graph = graph.copy()
        self.communities = []
        self.execution_time = None
        self.best_modularity = -1
        self.best_partition = None
        self.modularity_progress = []

    def _remove_highest_betweenness_edge(self):
        edge_betweenness = nx.edge_betweenness_centrality(self.graph)
        max_edge = max(edge_betweenness, key=edge_betweenness.get)
        self.graph.remove_edge(*max_edge)
        print(f"Removed edge: {max_edge}")

    def detect_communities(self):
        print("Running Girvan-Newman Algorithm...")
        start = time.time()

        while self.graph.number_of_edges() > 0:
            components = list(nx.connected_components(self.graph))

            if len(components) > len(self.communities):
                self.communities = components
                current_modularity = modularity(
                    self.original_graph, components
                )
                self.modularity_progress.append(current_modularity)

                print("Number of Communities:", len(components))
                print("Current Modularity:", current_modularity)

                if current_modularity > self.best_modularity:
                    self.best_modularity = current_modularity
                    self.best_partition = components

            self._remove_highest_betweenness_edge()

        end = time.time()
        self.execution_time = end - start

        print("\nGirvan-Newman execution time:", self.execution_time)
        return self.best_partition

    def export_results(self, filename="girvan_newman_results.csv"):
        print("Exporting best partition to CSV...")
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Node", "Community"])

            for i, community in enumerate(self.best_partition):
                for node in community:
                    writer.writerow([node, i])

        print("Results saved to", filename)

    def visualize(self):
        print("Visualizing best partition...")
        pos = nx.spring_layout(self.original_graph)

        node_colors = []
        for node in self.original_graph.nodes():
            for i, community in enumerate(self.best_partition):
                if node in community:
                    node_colors.append(i)

        nx.draw(
            self.original_graph,
            pos,
            node_color=node_colors,
            cmap=plt.cm.Set3,
            with_labels=True,
            node_size=400,
        )

        plt.title("Girvan-Newman Community Detection")
        plt.show()

    def print_summary(self):
        print("\n----- Final Summary -----")
        print("Total Communities:", len(self.best_partition))
        print("Best Modularity:", self.best_modularity)
        print("Execution Time:", self.execution_time)

        for i, community in enumerate(self.best_partition):
            print(f"Community {i}: {list(community)}")

        print("--------------------------\n")


def main():

    loader = DatasetLoader(
        dataset_type="snap",
        file_path="datasets/facebook_combined.txt"
    )

    G = loader.load()

    # ***Sampling for Girvan*** 
    sample_size = 300
    nodes = list(G.nodes())[:sample_size]
    G = G.subgraph(nodes).copy()

    print(f"Running Girvan on sampled subgraph ({sample_size} nodes)\n")

    analyzer = GraphAnalyzer(G)
    analyzer.print_basic_stats()

    detector = GirvanNewmanDetector(G)
    detector.detect_communities()
    detector.print_summary()
    detector.export_results()
    detector.visualize()

if __name__ == "__main__":
    main()
