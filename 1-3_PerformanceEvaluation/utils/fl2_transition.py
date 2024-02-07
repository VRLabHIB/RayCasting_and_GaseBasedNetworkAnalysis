import numpy as np
import pandas as pd

import gc
import time
import tracemalloc


def create_transition_datasets(save_path, ID_lst, dataframes, save=True):
    # Define a list of objects of interest (OOIs)
    tracemalloc.start(10)
    dataloader_time = time.time()

    df_transition_lst = list()

    for file in range(len(dataframes)):
        df = dataframes[file]
        # name = data_lst[file]

        # [Remove all rows from the dataset that do not contain our OOIs] exclude, selection of OOIs
        # bool_lst = df['gaze_target'].isin(ooi_lst)
        # df = df[bool_lst]
        # df = df.reset_index(drop=True)

        # In our case we get the participant ID out of the filename
        # Here you have to adjust the function eventually
        ID = ID_lst[file]

        ID_lst_new = list()
        source_lst = list()
        target_lst = list()
        time_lst = list()
        trans_time_lst = list()

        source = df['gaze_target'].iloc[0]

        for i in range(1, len(df)):
            if source != df['gaze_target'].iloc[i]:
                ID_lst_new.append(ID)
                time_lst.append(df['time'].iloc[i - 1])
                trans_time_lst.append(df['time'].iloc[i] - df['time'].iloc[i - 1])
                source_lst.append(source)
                target_lst.append(df['gaze_target'].iloc[i])

                source = df['gaze_target'].iloc[i]

        df_trans = pd.DataFrame({'participant': ID_lst_new, 'time_point': time_lst, 'trans_dur': trans_time_lst,
                                 'Source': source_lst, 'Target': target_lst})
        df_transition_lst.append(df_trans)

        if save:
            df_trans.to_csv(save_path +'/ID_' + str(ID) + '.csv', index=False)

    dataloader_deltatime = time.time() - dataloader_time

    try:
        tracemalloc.run_reflector()
    except:
        snapshot = tracemalloc.take_snapshot()
        memory = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()

    return df_transition_lst, dataloader_deltatime, memory


def build_adjacency_matrices_as_datasets(df_transition_lst, min_trans_dur=0, max_trans_dur=10,
                                         min_weight=1, normalize=True):
    df_mat_lst = list()

    for file in range(len(df_transition_lst)):
        df = df_transition_lst[file]

        # Not included in performance testing  (select thresholds)
        # df = df[np.logical_and(df['time_dur'] >= min_trans_dur, df['time_dur'] <= max_trans_dur)]

        df_mat = pd.DataFrame(df.groupby(['Source', 'Target'], as_index=False).size())
        df_mat.columns = ['Source', 'Target', 'Weight']

        # Not included in performance testing (select thresholds)
        # df_mat = df_mat[df_mat['Weight'] >= min_weight]

        if normalize:
            w_sum = np.sum(df_mat['Weight'].values)
            df_mat['Weight'] = df_mat['Weight'] / w_sum

        df_mat_lst.append(df_mat)

    return df_mat_lst
