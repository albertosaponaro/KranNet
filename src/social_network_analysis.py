import env, utils, sql_utils
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from itertools import combinations
from collections import Counter

def add_edges_for_meeting(meeting_id, graph, dataframe):

    # Generate all possible combinations of pairs within a list
    combinations_list = list(combinations(dataframe[dataframe.meeting_id == meeting_id].speaker_name, 2))
    
    # Add Edges
    for s1, s2 in combinations_list:
        graph.add_edge(s1, s2)

def generate_graph(krannet_df, min_interventions):
    # Remove some people based on interventions
    krannet_df = krannet_df[krannet_df.interventions >= min_interventions]

    G = nx.Graph()

    # Create counters for nodes and edges
    node_counter, edge_counter = Counter(), Counter()

    for m in set(krannet_df.meeting_id):
        combinations_list = list(combinations(krannet_df[krannet_df.meeting_id == m].speaker_name, 2))
        
        # Add edges
        for s1, s2 in combinations_list:
            G.add_edge(s1, s2)
            node_counter[s1] += 1
            node_counter[s2] += 1
            edge_counter[(s1, s2)] += 1

    # Normalize node sizes for better visualization
    node_sizes = [node_counter[node] * 50 for node in G.nodes()]  # Adjust scaling factor as needed

    # Normalize edge widths for better visualization
    edge_widths = [edge_counter[edge] for edge in G.edges()]

    return G, node_sizes, edge_widths

def plot_network(G, node_sizes, edge_widths, show_plot=True, save_plot_as=None):
    # Set up the figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # Use a layout for the graph
    pos = nx.spring_layout(G, seed=42)  # spring layout with a fixed seed for reproducibility

    # Draw nodes and edges with attributes
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='skyblue', alpha=0.7)
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='darkslategray')

    # Title and display options
    plt.title('Network Graph of Speaker Interactions')
    plt.axis('off')  # Hide the axes
    if show_plot: plt.show();
    if save_plot_as: plt.savefig(save_plot_as)

def calc_deg_centrality(krannet_df, G, min_interventions):
    # Remove some people based on interventions
    krannet_df = krannet_df[krannet_df.interventions >= min_interventions]
    
    # calculate degree centrality and betweenness for nx
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    # define the node labels
    nodes = list(set(krannet_df.speaker_name))

    # retrieve degree centrality for each node
    dc_calculations = []
    bc_calculations = []

    for node in nodes:
        dc_calculations += [degree_centrality[node]]
        bc_calculations += [betweenness_centrality[node]]

    # create a centrality data df to store values
    centrality_data = pd.DataFrame()

    # populate the df with the nodes and their centrality values
    centrality_data["Node"] = nodes
    centrality_data["Degree-Centrality"] = dc_calculations
    centrality_data["Betweenness-Centrality"] = bc_calculations

    return centrality_data


def main():
    input_file, output_dir = utils.parse_arguments()

    krannet_df = pd.read_json(input_file)

    # Initialize new graph
    min_inter = 1
    G, node_sizes, edge_widths = generate_graph(krannet_df, min_interventions=min_inter)

    # Plot network
    plot_network(G, node_sizes, edge_widths, show_plot=False, save_plot_as=f'{output_dir}/sn_min-inter-{min_inter}.pdf')

    # Calculate degree of centrality
    centrality_df = calc_deg_centrality(krannet_df, G, min_inter)
    centrality_df.to_csv(f'{output_dir}/sn_centrality_min-inter-{min_inter}.csv', sep='\t')


    # ---------------------------------------------------------------------------------------------------------------------------------------------#


    # Initialize new graph
    min_inter = 3
    G, node_sizes, edge_widths = generate_graph(krannet_df, min_interventions=min_inter)

    # Plot network
    plot_network(G, node_sizes, edge_widths, show_plot=False, save_plot_as=f'{output_dir}/sn_min-inter-{min_inter}.pdf')

    # Calculate degree of centrality
    centrality_df = calc_deg_centrality(krannet_df, G, min_inter)
    centrality_df.to_csv(f'{output_dir}/sn_centrality_min-inter-{min_inter}.csv', sep='\t')
    



if __name__ == '__main__':
    main()