# 📘 Community Detection in Social Networks

This project focuses on detecting communities in social networks using graph-based algorithms. It analyzes how nodes form clusters based on their connections and evaluates different approaches for identifying these communities.


## 🔍 Algorithms Implemented

### 1. Louvain Method
- Based on modularity optimization
- Efficient and scalable for large networks
- Produces high-quality community structures

### 2. Girvan–Newman Algorithm
- Based on edge betweenness centrality
- Removes important edges to split the graph
- Produces hierarchical community structures
- Computationally expensive for large datasets


## 📊 Datasets Used

- **Zachary Karate Club Dataset**
  - Small benchmark social network
  - 34 nodes and 78 edges

- **Facebook Social Network Dataset (SNAP)**
  - Real-world large-scale network
  - Sampled subgraph used for computation


## ⚙️ Features

- Load datasets (Karate / CSV / SNAP)
- Construct graph using NetworkX
- Perform community detection using:
  - Louvain Algorithm
  - Girvan–Newman Algorithm
- Compute graph statistics:
  - Number of nodes and edges
  - Graph density
  - Clustering coefficient
- Calculate modularity score
- Visualize communities
- Export results to CSV
- Compare execution time and performance


## 🛠️ Tech Stack

- Python
- NetworkX
- Pandas
- Matplotlib
- python-louvain
