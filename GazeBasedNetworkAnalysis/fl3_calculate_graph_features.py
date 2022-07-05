import numpy as np
import pandas as pd
import networkx as nx

### Helper functions
def split(word):
    return [char for char in word]


def get_participant_id(name):
    s = split(name)
    ID = s[0] + s[1] + s[2]
    return ID


### Graph feature functions
def degree_centrality_for_groups(graph_lst, name_lst, group_name, names_of_group_members):
    """
    Calculates the degree centrality for each individual group member
    and sums up all centrality values for all members of the group.

    :param graph_lst: list that contains the graph objects
    :param name_lst: list of strings with the names of the graphs (might contain the participant ID)
    :param group_name: string of the name of the group
    :param names_of_group_members: list of strings of all nodes which the degree centrality should be summed up
    :return: pandas dataframe which consists of an ID variable and the Degree Centrality values for each participant
    """

    deg_centrality_lst = list()

    ID_lst = list()

    for graph in range(len(graph_lst)):
        G = graph_lst[graph]
        name = name_lst[graph]

        ID = get_participant_id(name)

        centr = G.degree(weight='Weight')
        centr = np.matrix(list(centr))

        deg_centrality = 0

        for i in range(len(centr)):
            if centr[i, 0] in names_of_group_members:
                deg_centrality += float(centr[i, 1])

        ID_lst.append(ID)
        deg_centrality_lst.append(deg_centrality)

    df = pd.DataFrame({'ID': ID_lst, 'DegreeCentrality_{}'.format(group_name): deg_centrality_lst})
    return df


def weighted_degree_centrality_for_uniformity():
    return None


def clique_features(graph_lst, name_lst, group_name, names_of_group_members, number_of_cliques=True, avg_clique_size=True):
    for graph in range(len(graph_lst)):
        G = graph_lst[graph]
        name = name_lst[graph]

        ID = get_participant_id(name)

        # Transform G into weighted undirected graph
        UG = G.to_undirected()
        for node in G:
            for ngbr in nx.neighbors(G, node):
                if node in nx.neighbors(G, ngbr):
                    UG.edges[node, ngbr, 0]['Weight'] = (G.edges[node, ngbr, 0]['Weight'] + G.edges[ngbr, node, 0][
                        'Weight']) / 2

        # Find maximal cliques
        cl = nx.find_cliques(UG)

        # count number of cliques larger than two nodes with only peers
        n_cl_not = 0

        # count number of nodes per clique for ones with only students in it
        n_nodes_in_c_stud = 0
        len_cl_stud = 0

        ratio_boys = 0
        ratio_girls = 0

        for c in cl:
            if 'teacher' not in c and 'screen' not in c:
                len_cl_stud += 1
                n_nodes_in_c_stud += len(c)

                H = nx.subgraph(UG, c)
                x = nx.get_edge_attributes(H, 'Weight')
                x = x.values()

                if len(c) > 2:
                    H = nx.subgraph(UG, c)
                    x = nx.get_edge_attributes(H, 'Weight')
                    x = x.values()
                    n_cl_not += 1


        if len_cl_stud == 0:
            n_nodes_in_c_stud = 0
            avg_ratio_boys = 0
            avg_ratio_girls = 0
        if len_cl_stud > 0:
            n_nodes_in_c_stud = n_nodes_in_c_stud / len_cl_stud
            avg_ratio_boys = ratio_boys / len_cl_stud
            avg_ratio_girls = ratio_girls / len_cl_stud

        ID_lst.append(ID)
        ratio_cl_boys_lst.append(avg_ratio_boys)
        avg_clique_size_stud_lst.append(n_nodes_in_c_stud)
        n_cl_lst_not.append(n_cl_not)
        if number_of_cliques:

    return None


def cut_size():
    return None


def uniformity():
    return None
