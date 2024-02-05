# Test code performance with Python against R

## Key Performance Indicator (KPI)

- Runtime
- Memory Storage
- Number of Operations
- Complexity (Big-O)

## Data Generation and Parameters

Generate different dataset to check for changes in performance. Tow separate steps are tested:
- Data preparation/ Generation of transition matrices
- Network creation and computation of structural variables

Parameters for the data are:

- Number of participants (loop over the same dataset, but load them as separate dataframes)

- Size (length) of the eye-tracking dataset (N=100, 1000, 10000, 100000)
  - A 10-minute VR experiments translates roughly into 30000 data points (with 50 fps (0.02))
  - Using high frequency eye tracker can increase the number of data points, therefore we added a dataset size of 100000
    - However, this number is not reached with the presented setup since it would result in an 33-minute VR session 

- Number of OOIs (result in the number of nodes in the network) (N nodes=4, 10, 25, 50)
  - X unique OOIs would mean that there existed X unique objects in the environment to be tracked

## General Tips
- Remove unnecessary variables (to generate transition matrices only 2 variables are necessary {time, object})
  - This leads to an average of 1.5 kilobytes per 100 time points (increases with an increasing number of OOIs)