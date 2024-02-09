project_path = dirname(rstudioapi::getSourceEditorContext()$path)

#### Start testing ####
library(pryr)
data_path <- paste0(project_path, '/data/')


# Load the original datafile and preprocess it
start_time <- Sys.time()
df <- read.csv(paste0(data_path, "final_A116.csv"))
# select subset
dfs <- df[c("real_time", "object", "left.pupil_diameter_mm", "right.pupil_diameter_mm")]
dfs <- dfs[!(dfs$left.pupil_diameter_mm==-1 | dfs$right.pupil_diameter_mm==-1),]
dfs <- dfs[complete.cases(dfs),]
colnames(dfs) <- c('time', 'gaze_target', 'left.pupil_diameter_mm', 'right.pupil_diameter_mm')
write.csv(dfs, paste0(data_path, "smaller_subset_R.csv"))
deltatime <- Sys.time() - start_time


# Create transition matrix
start_time <- Sys.time()

df <- read.csv(paste0(data_path, "smaller_subset_R.csv"))

ID <- "001"

ID_lst_new <- vector()
source_lst <- vector()
target_lst <- vector()
time_lst <- vector()
trans_time_lst <- vector()

source <- df$gaze_target[1]

for (i in 2:nrow(df)) {
  if (source != df$gaze_target[i]) {
    ID_lst_new <- c(ID_lst_new, ID)
    time_lst <- c(time_lst, df$time[i - 1])
    trans_time_lst <- c(trans_time_lst, df$time[i] - df$time[i - 1])
    source_lst <- c(source_lst, source)
    target_lst <- c(target_lst, df$gaze_target[i])
    
    source <- df$gaze_target[i]
  }
}


df_trans <- data.frame(participant = ID_lst_new, time_point = time_lst, trans_dur = trans_time_lst,
                       Source = source_lst, Target = target_lst)

write.csv(df_trans, paste0(data_path, "transition_R.csv"))

deltatime <- Sys.time() - start_time

library(igraph)
library(dplyr)

start_time <- Sys.time()
# Create adjacency dataset
dfs <- df_trans
dfs$participant <- NULL
dfs$time_point <- NULL
dfs$trans_dur <- NULL
dfs$Weight <- 1
adj <- dfs %>% group_by(Source, Target) %>% summarise(weight = sum(Weight))


# Create graph
n <- nrow(adj)
G <- graph_from_edgelist(as.matrix(adj[1:n,1:2]), directed=TRUE)
G <- set.edge.attribute(G, "weight", index=E(G), adj$weight)
deltatime <- Sys.time() - start_time

#### Create graph features ####

#Weighted degree centrality
start_time <- Sys.time()
# Extracting weights from the adjecency matrix
adj$weight_n <- adj$weight / sum(adj$weight)
weights <- adj[adj$Source=="CartoonTeacher",]$weight_n

# Sort weights
sorted_weights <- sort(weights)

# Calculate sum of outgoing weights
sumw <- sum(weights)

DC <- length(sorted_weights)
FCi <- numeric(DC - 1)

for (i in 1:(DC - 1)) {
  fj <- 0
  for (j in 1:i) {
    fj <- fj + sorted_weights[j] / sumw
  }
  FCi[i] <- fj
}

WDC <- 1 + 2 * sum(FCi)
deltatime <- Sys.time() - start_time


# Count the number of cliques containing only student OOIs larger than 1
start_time <- Sys.time()
stud <- c('S11_C', 'S12_C', 'S13_C', 'S14_C', 'S15_C', 'S16_C', 
          'S17_C', 'S22_C', 'S23_C', 'S24_C', 'S27_C', 'S28_C',
          'S32_C', 'S33_C', 'S34_C', 'S35_C', 'S36_C', 'S37_C',
          'S38_C', 'S42_C', 'S43_C', 'S44_C', 'S47_C', 'S48_C')

subv <- Reduce(intersect, list(colnames(mat), stud))
sg <- induced.subgraph(graph=G,vids=subv)

cl <- max_cliques(sg)

cl_count <- 0
for (l in cl){
  if (length(l)>1){
    cl_count <- cl_count +1
  }
}
print(paste0('Number of cliques: ', cl_count))

deltatime <- Sys.time() - start_time
