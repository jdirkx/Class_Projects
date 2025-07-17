"
LING 493 Final Project Analysis - searching for target regional words
Jacob Dirkx, Eloy Vetto, Clay Worthington
"
library(data.table)
library(dplyr)

your_data_table <- fread("/Users/Jacob/Desktop/Corpus Ling/Final Corpus/CorpusSum")

# Target Words
Cougar <- "Cougar"
Sunbreak <- "Sunbreak"
Granola <- "Granola"
Spendy <- "Spendy"

#Paths
setwd("/Users/Jacob/Desktop/Corpus Ling/Final Corpus") #change directory for your own 
PNW <- "/Users/Jacob/Desktop/Corpus Ling/Final Corpus/PNW"
Other <- "/Users/Jacob/Desktop/Corpus Ling/Final Corpus/Other"

#Corpora based on region and word type
PNW_AF <- list.files(path = PNW, pattern = "*AF.csv", recursive = T, include.dirs= T)
Other_AF <- list.files(path = Other, pattern = "*AF.csv", recursive = T, include.dirs= T)
PNW_NF <- list.files(path = PNW, pattern = "*NF.csv", recursive = T, include.dirs= T)
Other_NF <- list.files(path = Other, pattern = "*NF.csv", recursive = T, include.dirs= T)

#Function to search CSVs for specific words
Search <- function(file_path, pattern) {
  data <- read.csv(file_path)
  
  # Filter rows based on the pattern in the "word" column
  result <- data %>%
    filter(grepl(pattern, word, ignore.case = TRUE))
  
  # Return the file name and matching rows
  return(list(file = file_path, matches = result))
}

#Call function for files
Cougar_PNW <- lapply(PNW_Nouns, function(file) Search(file, Cougar))
print(search_results)

for (i in PNW_AF){
  data <- read.csv(i)
  PNW_Adjs <- as.character(data$word)
}

Adj <- "AF"
Noun <- "NF"



data <- data.frame(
  region = c("PNW", "PNW", "Other", "Other"),
  fictionality = c("fiction", "nonfiction", "fiction", "nonfiction"),
  cougar = c(6, 53, 2, 0),
  mt_lion = c(4, 2, 0, 15),
  puma = c(6, 0, 0, 0)
)


glm_1 <- glm(cougar ~ region + fictionality, family = "gaussian", data)
glm_2<- glm(mt_lion ~ region + fictionality, family = "gaussian", data)
glm_3 <- glm(puma ~ region + fictionality, family = "gaussian", data)

glm_models <- list(glm_1, glm_2, glm_3)
summaries <- lapply(glm_models, summary)
print(summaries)

summary(glm_1)

install.packages("readxl")
install.packages("nnet")


library(readxl)
library('lme4')
library('MuMIn')
library(nnet)

setwd("/Users/Jacob/Desktop/Corpus Ling/Final Corpus")
data2 <- read.csv("AltCon.txt", sep = "\t")


realmodel <- multinom(Realization ~ Region + Fictionality, data = data2)

summary(realmodel)

data2$Realization <- as.factor(data2$Realization)

realization_levels <- levels(data2$Realization)
print(realization_levels)

Rmodel <- lm(number ~ fiction, data = Fictionality)
summary(Rmodel)

cont_table <- table(Fictionality$Fiction, Fictionality$Nonfiction)

FictChi <- chisq.test(cont_table)
print(FictChi)
summary(FictChi)