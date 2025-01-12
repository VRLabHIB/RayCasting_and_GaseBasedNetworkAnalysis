# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 09:10:51 2021

@author: Stark
"""


def create_and_save_graphs(df_mat_lst, name_lst, save_path, save=True):
    import networkx as nx
    import pickle
    import os

    os.chdir(save_path)

    graph_lst = list()
    for file in range(len(df_mat_lst)):
        df_mat = df_mat_lst[file]
        G = nx.from_pandas_edgelist(df_mat, source='Source', target='Target', edge_attr=['Weight'],
                                    create_using=nx.MultiDiGraph())
        graph_lst.append(G)

        if save:
            name = name_lst[file]
            with open("{}.p".format(name), 'wb') as f:
                pickle.dump(G, f)

    return graph_lst


if __name__ == '__main__':
    # file function libraries
    import fl1_preprocessing as fl1
    import fl2_transition as fl2
    import fl3_calculate_graph_features as fl3

    # Load and preprocess the datasets
    # Renaming of the dataset variables and additional prepocessing steps must be implemented directly in the script
    filepath = "/your_file_path/"
    name_lst, dataframes = fl1.load_and_preprocess_datasets(filepath=filepath, save_path=None, start_t=0, end_t=850,
                                                            filetag="object*.csv")

    # Create a transition dataset, that contains all transitions between our OOIs as well as the transition starting
    # point and the duration of the transition. Define your list of objects of interest that should be considered when
    # creating the transition datasets
    # Define a list of objects of interest (OOIs)
    ooi_lst = ['S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S22', 'S23', 'S24', 'S27', 'S28', 'S32', 'S33',
               'S34', 'S35', 'S36', 'S37', 'S38', 'S42', 'S43', 'S44', 'S47', 'S48', 'screen', 'teacher']

    # Customization of the get_participant_id function is necessary depending on the datasets
    filepath = "/file_path_of_preprocessed_data/"
    savepath = "/your_file_save_path"
    df_transition_lst = fl2.create_transition_datasets(dataframes=dataframes, name_lst=name_lst, filepath=filepath,
                                                       savepath=savepath, ooi_lst=ooi_lst)

    # with the transition dataframes we can now compute the adjacency matrices. Note that we also store them in a
    # pandas dataframe format for further graph building
    filepath = "/file_path_of_transition_data/"
    savepath = "/your_file_save_path"
    df_mat_lst = fl2.build_adjacency_matrices_as_datasets(dataframes=df_transition_lst, name_lst=name_lst,
                                                          min_trans_dur=0, max_trans_dur=10, min_weight=1,
                                                          normalize=True)

    savepath = "/your_graph_save_path/"
    graph_lst = create_and_save_graphs(df_mat_lst, name_lst, savepath)

    # ###### Calculate graph structural variables for individual graphs for each participant ######
    # Depending of the datasets investigated the OOIs and the foci could be very different.
    # Therefore, we just try to give an example of our VR classroom study.

    stud_lst = ['S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S22', 'S23', 'S24', 'S27', 'S28', 'S32', 'S33',
                'S34', 'S35', 'S36', 'S37', 'S38', 'S42', 'S43', 'S44', 'S47', 'S48']
    teacher_lst = ['teacher']
    screen_lst = ['screen']

    # All dataset can be merged later on using the pandas merge function on ID
    centr_student = fl3.degree_centrality_for_groups(graph_lst, name_lst, 'students', stud_lst)
    centr_teacher = fl3.degree_centrality_for_groups(graph_lst, name_lst, 'teacher', teacher_lst)
    cenrt_screen = fl3.degree_centrality_for_groups(graph_lst, name_lst, 'screen', screen_lst)
