import numpy as np
import pandas as pd
import networkx as nx

from scipy.stats import chisquare

### Helper functions
def split(word):
    return [char for char in word]


def get_participant_id(name):
    s = split(name)
    ID = s[0] + s[1] + s[2]
    return ID

### Graph feature functions
def degree_centrality_for_groups(graph_lst, name_lst, group_name, names_of_group_members):
    '''

    :param graph_lst:
    :param name_lst:
    :param group_name:
    :param names_of_group_members:
    :return:
    '''

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


def weighted_degree_centrality_for_uniformity(graph_lst, name_lst, node):
    ID_lst = list()
    WDC_lst = list()

    for graph in range(len(graph_lst)):
        G = graph_lst[graph]
        s = split(name_lst[graph])
        ID = s[0] + s[1] + s[2]

        # Weighted degree centrality for specific node
        edges = G.out_edges(node, data=True)
        sumw = G.out_degree(node, weight='Weight')

        weight_lst = list()

        for e in edges:
            source, target, weight = e
            weight_lst.append(weight['Weight'])

        # Necessary to compare different graphs with different outgoing nodes.
        weight_lst.sort()

        DC = len(edges)
        FCi = np.zeros(DC - 1)

        for i in range(DC - 1):  # 0,1,2,3
            fj = 0
            for j in range(i + 1):
                fj += weight_lst[j] / sumw
            FCi[i] = fj
       
        WDC = 1+ 2*(np.sum(FCi))
        WDC_lst.append(WDC)
        
    df = pd.DataFrame({'ID':ID_lst, 'WDC':WDC_lst})
    return df

def uniformity(graph_lst, name_lst):
    ID_lst = list()
    chi_lst = list()

    for graph in range(len(graph_lst)):
        G = graph_lst[graph]
        s = split(name_lst[graph])
        ID = s[0] + s[1] + s[2]

        n_nodes = len(list(G.nodes))
        x = nx.get_edge_attributes(G, 'Weight')
        x = list(x.values())

        chi, _ = chisquare(x)

        ID_lst.append(ID)
        chi_lst.append(-chi)

    df = pd.DataFrame({'ID': ID_lst, 'ChiUniformity':chi_lst})
    return df
    
def cut_size(graph_lst, name_lst, stud_lst):
    cut_norm_lst = list()
    ID_lst = list()

    for graph in range(len(graph_lst)):
        G = graph_lst[graph]
        s = split(name_lst[graph])
        ID = s[0] + s[1] + s[2]

        # Devide nodes into students and teacher/screen
        S = list()
        for i in G.nodes:
            if i in stud_lst:
                S.append(i)
        T = ['teacher', 'screen']

        # calculate cut size between the two groups
        cut_norm = nx.normalized_cut_size(G, S, T, weight='Weight')

        ID_lst.append(ID)
        cut_norm_lst.append(cut_norm)

    return None
    
def clique_features(graph_lst, name_lst, group_name, names_of_group_members,
                    number_of_cliques=True, avg_clique_size=True):
    ID_lst = list()
    ratio_cl_boys_lst = list()
    avg_clique_size_stud_lst = list()
    n_cl_lst_not = list()

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
            None

    return None

if __name__ == '__main__':
    #Load a graph and test
    None