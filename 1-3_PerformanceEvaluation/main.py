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
    df = pd.DataFrame(np.arange(0, dataset_size * fps, 0.025), columns=list_cols)

    # Create OOI variable (for comparison reason choose OOIs to switch every timeframe)
    letters = create_OOI_letters()
    letters_n_OOI = letters[:n_OOI]
    lst = list()
    for l in letters_n_OOI:
        l10 = [l] * 8
        lst = lst + l10
    lst = lst * int(dataset_size / 8)
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
        df = pd.read_csv(data_path + 'df_size-{}_fps-0025_nOOIS-{}.csv'.format(dataset_size, N_OOI), index_col=0)
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
    #dataloader_file = open(project_path + "/results/Python/dataloader.txt", "w")
    #dataloader_file.write("Participants, Dataset_size, NumberOfOOIS, runtime, memorycurrent, memorypeak \n")
    #dataloader_file.close()

    #matrices_file = open(project_path + "/results/Python/matrices.txt", "w")
    #matrices_file.write("Participants, Dataset_size, NumberOfOOIS, runtime, memorycurrent, memorypeak \n")
    #matrices_file.close()

    # Enable steps in testing
    generate_data = False
    build_transition_matrices = True

    # Parameters
    N_participants = [50, 100, 300] # done
    dataset_sizes = [25000, 50000]
    N_OOIs = [10, 20, 40]
    fps = 0.025

    # Generate test datasets
    if generate_data:
        for dataset_size in dataset_sizes:
            for N_OOI in N_OOIs:
                generate_dataset(project_path, dataset_size, fps, N_OOI)

    #### Start testing ####

    # Build transition matrices
    if build_transition_matrices:
        for dataset_size in dataset_sizes:
            for Npart in N_participants[1:]:
                ID_lst = np.arange(0, Npart)
                N_OOI = 10

                parent_dir = project_path + '\\data\\Python\\transition_matrix\\'
                directory = "df_part-{}_size-{}_nOOIS-{}".format(Npart, dataset_size, N_OOI)
                save_path = os.path.join(parent_dir, directory)

                try:
                    os.mkdir(save_path)
                except:
                    print('Folder already exists')

                dataframes, dataloader_deltatime, memory = load_dataframes(project_path, Npart, dataset_size,
                                                                           N_OOI)
                dataloader_file = open(project_path + "/results/Python/dataloader.txt", "a")
                dataloader_file.write(
                    "{},{},{},{},{},{} \n".format(Npart, dataset_size, N_OOI, dataloader_deltatime,
                                                  memory[0], memory[1]))
                dataloader_file.close()

                matrices, matrices_deltatime, matrices_memory = fl2_transition.create_transition_datasets(
                    save_path,
                    ID_lst,
                    dataframes,
                    save=True)
                matrices_file = open(project_path + "/results/Python/matrices.txt", "a")
                matrices_file.write(
                    "{},{},{},{},{},{} \n".format(Npart, dataset_size, N_OOI, matrices_deltatime,
                                                  matrices_memory[0], matrices_memory[1]))
                matrices_file.close()
                del dataframes
                # del matrices
                gc.collect()





    print(' ')
