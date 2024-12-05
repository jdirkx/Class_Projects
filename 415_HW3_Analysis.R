"
LING 415 - HW3 Analysis Script
Jacob Dirkx
"

#set wd, get data from csv
setwd("C:/Users/jacob/OneDrive/Desktop/UOregon/Linguistics")
data <- read.csv("415_HW3_Data.csv")

#custom reference levels for interactivity, text_type
data$interactivity <- as.factor(data$interactivity)
data$interactivity <- relevel(data$interactivity, ref = "MX")
data$speaker_status <- as.factor(data$speaker_status)
data$speaker_status <- relevel(data$speaker_status, ref = "NNS")

  #get median text_type based on because/since percentages
  tt_data <- data.frame(
    text_type = c('ADV', 'COL', 'DEF', 'DIS', 'INT', 'LAB', 'LEL', 'LES', 'MTG', 'OFC', 'SEM', 'SGR', 'STP', 'SVC', 'TOU'),
    because = c(66.67, 95.74, 80.00, 88.14, 100.00, 88.24, 93.86, 96.77, 89.36, 93.62, 93.55, 92.42, 84.62, 100.00, 94.44),
    since = c(33.33, 4.26, 20.00, 11.86, 0.00, 11.76, 6.14, 3.23, 10.64, 6.38, 6.45, 7.58, 15.38, 0.00, 5.56)
  )
  tt_data$sort_key <- tt_data$because
  tt_data_sorted <- tt_data[order(-tt_data$sort_key), ]
  med_tt = tt_data_sorted[8, c("text_type")]
  
data$text_type <- as.factor(data$text_type)
data$text_type <- relevel(data$text_type, ref = med_tt)


#Run binomial regression
#change form column to 0/1 binary response variable
#because = 0, since = 1
data$form[data$form == "because"] <- 0
data$form[data$form == "since"] <- 1
data$form <- as.numeric(data$form)
model <- glm(form ~ speaker_status + text_type + interactivity, family = binomial, data=data)
#baseline categories per variable
#speaker_status = NS
#text_type = SEM
#interactivity = MX
summary(model) 


#model accounting for interaction
interaction_model <- glm(form ~ speaker_status * text_type * interactivity, family = binomial, data=data)
summary(interaction_model)

