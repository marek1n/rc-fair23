library(rcicr) 

# https://medium.com/@rondotsch/reverse-correlation-image-classification-using-r-a0701648fb0
# TODO generate hi-res stimuli (~/.../scioi_fair_demonstrator/rproject_rc_demonstrator/material)

setwd("/app/src") # TODO

# extract cmd line args
args <- commandArgs(trailingOnly = TRUE)
subject_id <- args[1]
condition <- args[2]

# load data
assets_dir <- '../static/assets'
data_dir <- '../data'
data_file <- sprintf('sub-%s_%s.csv', subject_id, condition)
seed_file <- 'rcic_seed_1_time_Sep_16_2023_15_28.Rdata'

# rcicr args
df_path <- file.path(data_dir, data_file)
df <- read.csv(df_path, header = TRUE)

baseimage <- 'base'
rdata <- file.path(assets_dir, seed_file)

stimuli <- df$X - 1
responses <- df$response

# generate cis
ci <- generateCI2IFC(stimuli, responses, baseimage, rdata, 
                    targetpath = '../static/cis', 
                    filename = sprintf("sub-%s_%s", subject_id, condition)
                    )