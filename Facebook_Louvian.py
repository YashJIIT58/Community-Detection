"""
Louvain Community Detection in social media
Author: Vishant

"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import community as community_louvain
import time
import os
import csv
from collections import defaultdict

class DatasetLoader:
    """
    Handles loading of different types of datasets.
    """

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
        print("-----------------------------------")

        return G

class GraphAnalyzer:
    """
    Provides basic graph statistics.
    """

    def __init__(self, graph):
        self.graph = graph

    def print_basic_stats(self):
        print("\n--- Graph Statistics ---")
        print("Nodes:", self.graph.number_of_nodes())
        print("Edges:", self.graph.number_of_edges())
        print("Density:", nx.density(self.graph))
        print("Average Clustering:", nx.average_clustering(self.graph))

    def degree_distribution(self):
        degrees = [deg for node, deg in self.graph.degree()]
        return degrees

class LouvainCommunityDetector:
    """
    Performs Louvain Community Detection.
    """

    def __init__(self, graph):
        self.graph = graph
        self.partition = None
        self.execution_time = None
        self.modularity_score = None

    def detect_communities(self):
        print("\nRunning Louvain Algorithm...")
        start = time.time()

        self.partition = community_louvain.best_partition(self.graph)

        end = time.time()
        self.execution_time = end - start
        print("Louvain execution time:", self.execution_time)

        return self.partition

    def calculate_modularity(self):
        if self.partition is None:
            raise ValueError("Run detection first.")

        self.modularity_score = community_louvain.modularity(
            self.partition, self.graph
        )
        print("Modularity Score:", self.modularity_score)
        return self.modularity_score

    def get_communities(self):
        communities = defaultdict(list)
        for node, comm_id in self.partition.items():
            communities[comm_id].append(node)
        return communities

    def export_results(self, filename="louvain_results.csv"):
        print("Exporting community results...")
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Node", "Community"])
            for node, comm in self.partition.items():
                writer.writerow([node, comm])
        print("Results saved to", filename)

    def visualize(self):
        print("Visualizing communities...")
        pos = nx.spring_layout(self.graph)
        values = [self.partition[node] for node in self.graph.nodes()]

        nx.draw(
            self.graph,
            pos,
            node_color=values,
            cmap=plt.cm.Set3,
            with_labels=True,
            node_size=400,
        )
        plt.title("Louvain Community Detection")
        plt.show()

    def print_summary(self):
        communities = self.get_communities()
        print("\n--- Community Summary ---")
        print("Total Communities:", len(communities))
        for comm_id, members in communities.items():
            print(f"Community {comm_id}: {members}")
        print("Execution Time:", self.execution_time)
        print("Modularity:", self.modularity_score)

def main():

    #Changes dataset_type to "csv" and provide file_path if needed
    
    loader = DatasetLoader(
    dataset_type="snap",
    file_path="datasets/facebook_combined.txt"
)
    G = loader.load()

    analyzer = GraphAnalyzer(G)
    analyzer.print_basic_stats()

    detector = LouvainCommunityDetector(G)
    detector.detect_communities()
    detector.calculate_modularity()
    detector.print_summary()
    detector.export_results()
    detector.visualize()

if __name__ == "__main__":
    main()
