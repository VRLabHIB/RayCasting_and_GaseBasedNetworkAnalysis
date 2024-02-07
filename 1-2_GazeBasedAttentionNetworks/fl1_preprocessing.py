import glob
import numpy as np

import pandas as pd
import os


def load_and_preprocess_datasets(filepath, filetag, start_t, end_t):
    """
    Loads the dataset in a particular folder and preprocesses the data

    :param filepath: folder path where the data is located
    :param start_t: float for the start time of the experiment
    :param end_t: float for the end time of the experiment
    :param filetag: with the glob package we can scan the folder content and select files based on a filetag
    :return: list of filenames and a list of respective preprocessed datasets
    """
    os.chdir(filepath)

    name_lst = glob.glob(filetag)
    print("Number of found files: ", len(name_lst))
    dataframes = [pd.read_csv(f, sep=',', header=0) for f in name_lst]  # create list with all data frames loaded

    # Rename variables, determine start and end time, delete missing object rows
    for file in range(len(dataframes)):
        obj = dataframes[file]

        # Renaming of variable names
        obj = obj.rename(columns={'real_time': 'time'})  # We had to rename the time variable in our dataset
        obj = obj.rename(columns={'object': 'gaze_target'})  # We had to rename the gaze target variable

        # Cut the dataset by start and end time of the interval we want to analyze
        obj = obj[np.logical_and(obj['time'] >= start_t, obj['time'] <= end_t)]

        # Remove all rows with missings in the gaze_target variable
        cond = np.invert(obj['gaze_target'].isna())
        final = obj[cond]
        dataframes[file] = final

        ######
        # Additional prepocessing steps can be added here, e.g. checking for data quality or tracking ratio
        ######

    # Remove most unused variables to speed up the process and rename object variables
    for file in range(len(dataframes)):
        obj = dataframes[file]
        obj = obj.drop(['hmd.position.x', 'hmd.position.y', 'hmd.position.z',
                        'hmd.orientation.pitch', 'hmd.orientation.yaw', 'hmd.orientation.roll',
                        'gaze_x_interpol', 'gaze_y_interpol', 'gaze_z_interpol', 'gaze_speed', 'hmd_speed', 'label',
                        'event', 'nor_pupil_diameter'], axis=1)

        # Use proper naming for the gaze targets (this step is only for presentation purposes)
        replace = {'S11_C': 'S11', 'S11_R': 'S11', 'S12_C': 'S12', 'S12_R': 'S12',
                   'S13_C': 'S13', 'S13_R': 'S13', 'S14_C': 'S14', 'S14_R': 'S14',
                   'S15_C': 'S15', 'S15_R': 'S15', 'S16_C': 'S16', 'S16_R': 'S16',
                   'S17_C': 'S17', 'S17_R': 'S17', 'S22_C': 'S22', 'S22_R': 'S22',
                   'S23_C': 'S23', 'S23_R': 'S23', 'S24_C': 'S24', 'S24_R': 'S24',
                   'S27_C': 'S27', 'S27_R': 'S27', 'S28_C': 'S28', 'S28_R': 'S28',
                   'S32_C': 'S32', 'S32_R': 'S32', 'S33_C': 'S33', 'S33_R': 'S33',
                   'S34_C': 'S34', 'S34_R': 'S34', 'S35_C': 'S35', 'S35_R': 'S35',
                   'S36_C': 'S36', 'S36_R': 'S36', 'S37_C': 'S34', 'S37_R': 'S37',
                   'S38_C': 'S38', 'S38_R': 'S38', 'S42_C': 'S42', 'S42_R': 'S42',
                   'S43_C': 'S43', 'S43_R': 'S43', 'S44_C': 'S44', 'S44_R': 'S44',
                   'S47_C': 'S47', 'S47_R': 'S47', 'S48_C': 'S28', 'S48_R': 'S48',
                   'CartoonTeacher': 'teacher', 'RealTeacher_2': 'teacher',
                   'Screen_95': 'screen'}
        # Replace the gaze target names with the proper ones
        obj['object'] = obj['object'].replace(replace)
        dataframes[file] = obj

    return name_lst, dataframes
