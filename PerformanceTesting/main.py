import numpy as np
import pandas as pd
import string

import os

import gc
import time
import tracemalloc

from utils import fl2_transition


def create_OOI_letters():
    letters = list(string.ascii_uppercase)
    double = string.ascii_uppercase

    double_lst = list()
    for d in double:
        double_lst.append(d + d)

    letters = letters + double_lst
    return letters


def generate_dataset(project_path, dataset_size, fps, n_OOI):
    # Create time dataframe
    list_cols = ['time']
    df = pd.DataFrame(np.arange(0, dataset_size * fps, 0.02), columns=list_cols)

    # Create OOI variable (for comparison reason choose OOIs to switch every timeframe)
    letters = create_OOI_letters()
    letters_n_OOI = letters[:n_OOI]
    lst = list()
    for l in letters_n_OOI:
        l10 = [l] * 10
        lst = lst + l10
    lst = lst * int(dataset_size / 10)
    #OOI_lst = lst[:n_OOI]
    OOI_var = lst[:dataset_size]# * int(dataset_size / len(OOI_lst))

    df['gaze_target'] = OOI_var

    fps_str = str(fps).replace('.', '')

    # Save dataframe
    df.to_csv(project_path + '/data/df_size-{}_fps-{}_nOOIS-{}.csv'.format(dataset_size, fps_str, n_OOI))


def load_dataframes(project_path, Npart, dataset_size, N_OOI):
    tracemalloc.start(10)
    dataloader_time = time.time()

    data_path = project_path + '/data/'
    dataframes = list()

    for i in range(Npart):
        df = pd.read_csv(data_path + 'df_size-{}_fps-002_nOOIS-{}.csv'.format(dataset_size, N_OOI), index_col=0)
        dataframes.append(df)

    dataloader_deltatime = time.time() - dataloader_time
    try:
        tracemalloc.run_reflector()
    except:
        snapshot = tracemalloc.take_snapshot()
        memory = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
    return dataframes, dataloader_deltatime, memory


if __name__ == '__main__':
    project_path = os.path.abspath(os.getcwd())

    # Performance tracking
    dataloader_file = open(project_path + "/results/Python/dataloader.txt", "w")
    dataloader_file.write("Participants, Dataset_size, NumberOfOOIS, runtime, memorycurrent, memorypeak \n")

    matrices_file = open(project_path + "/results/Python/matrices.txt", "w")
    matrices_file.write("Participants, Dataset_size, NumberOfOOIS, runtime, memorycurrent, memorypeak \n")

    # Enable steps in testing
    generate_data = False
    build_transition_matrices = True

    # Parameters
    N_participants = [25, 50, 100, 250, 500]
    dataset_sizes = [100, 1000, 10000, 100000]
    N_OOIs = [4, 10, 25, 50]
    fps = 0.02

    # Generate test datasets
    if generate_data:
        for dataset_size in dataset_sizes:
            for N_OOI in N_OOIs:
                generate_dataset(project_path, dataset_size, fps, N_OOI)

    #### Start testing ####

    # Build transition matrices
    if build_transition_matrices:
        for Npart in N_participants:
            ID_lst = np.arange(0, Npart)
            for dataset_size in dataset_sizes:
                for N_OOI in N_OOIs:
                    small_condition = np.logical_and(dataset_size == 100, np.logical_or(N_OOI == 25, N_OOI == 50))

                    if not small_condition:
                        parent_dir = project_path + '/data/Python/transition_matrix/'
                        directory = "df_part-{}_size-{}_nOOIS-{}".format(Npart, dataset_size, N_OOI)
                        save_path = os.path.join(parent_dir, directory)
                        try:
                            os.mkdir(save_path)
                        except:
                            print('Folder already exists')

                        dataframes, dataloader_deltatime, memory = load_dataframes(project_path, Npart, dataset_size,
                                                                                   N_OOI)
                        dataloader_file.write(
                            "{},{},{},{},{},{} \n".format(Npart, dataset_size, N_OOI, dataloader_deltatime,
                                                          memory[0], memory[1]))

                        matrices, matrices_deltatime, matrices_memory = fl2_transition.create_transition_datasets(
                            save_path,
                            ID_lst,
                            dataframes,
                            save=True)
                        matrices_file.write(
                            "{},{},{},{},{},{} \n".format(Npart, dataset_size, N_OOI, matrices_deltatime,
                                                          matrices_memory[0], matrices_memory[1]))
                        del dataframes
                        # del matrices
                        gc.collect()

        dataloader_file.close()
        matrices_file.close()


    print(' ')
