"
HW 2
Jacob Dirkx
(Worked with Eloy Vetto and Clay Worthington)
"

#1. Determine whether "some" and "of" are attracted to each other based on the chi square test, and the Fisher exact test in the Buckeye corpus
# Functions to use: rbind(c(),c()), fisher.test(), chisq.test()
library(stats)

setwd("/Users/Jacob/Desktop/Corpus Ling/Buckeye Corpus")

filenames <- list.files(pattern = "*.txt", recursive = T, include.dirs= T)
for (k in 1:length(filenames))
{
  if (k == 1) { 
    corpus <- scan(file=filenames[k], what="char", sep=" ", quote="") 
  }
  else {corpus <- c(corpus, scan(file=filenames[k], what="char", sep=" ", quote=""))}
  if (k %% 2 == 0) { print(k) }
}
some <- '\\bsome\\b'
of <- '\\bof\\b'
ctable <- table(corpus %in% of, corpus %in% some)


print("Chi-Square Test:")
print(chi_square_result)
#p-value is 0.0046, since it is under 0.05 they are attracted to each other and we can reject the null hypothesis
print("Fisher Exact Test:")
print(fisher_exact_result)
#p-value is 0.0002586, since it is under 0.05 they are attracted to each other and we can reject the null hypothesis

#class method
somefreq <- wd.freqs["some"]/(length(corpus))
offreq <- wd.freqs["of"]/(length(corpus))
#or
somes <- which(corpus=="some")
ofs <- which(corpus=="of")
some.of <- sum(corpus[somes+1]=="of")

A = some.of
B = length(somes) - some.of
C = length(ofs) - some.of
D = length(corpus) - B - C + A

contingencies <- rbind(c(A,B), c(C,D))
chisq.test(contingencies)
fisher.test(contingencies)

chi_square_result <- chisq.test(ctable)
fisher_exact_result <- fisher.test(ctable)

#2. Determine whether "of the" is favored by "some" more than by "all" or vice versa in utterances like "Some/all (of the) cats..." 
# in the Buckeye Corpus

freq_some <- grep(some,corpus)
freq_all <- grep('\\ball\\b',corpus)
freq_of <- grep(of,corpus)
freq_the <- grep('\\bthe\\b',corpus)
freq_allofthe = 0
freq_someofthe = 0

for (i in 1:length(freq_some)){
  if ((i+1 %in% freq_of == TRUE) && (i+2 %in% freq_the == TRUE)){
    freq_someofthe = freq_someofthe + 1
  }
}
for (i in 1:length(freq_all)){
  if ((i+1 %in% freq_of == TRUE) && (i+2 %in% freq_the == TRUE)){
    freq_allofthe = freq_allofthe + 1
  }
}
#this should work but does not for some reason? I do not know how to fix it

# Create a contingency table
contingency_table <- table(length(freq_all), length(freq_some), freq_allofthe, freq_someofthe)

# Print the contingency table
print(contingency_table)

#class method
post.somes <- somes + 1
post.some.ofs <- which(corpus[post.somes + 1]=="of")
post.some.ofs.thes <- which(corpus[post.some.ofs + 1]=="the")

alls <- which(corpus=="all")
post.all.ofs <- which(corpus[post.alls + 1]=="of")
post.all.of.thes <- which(corpus[post.all.ofs + 1]=="the")

A = post.some.ofs.thes
B = post.all.of.thes
C = length(somes) - post.some.ofs.thes
D = length(alls) - post.all.of.thes

#then same analysis method as question 1

#3. Is there a significant influence of the irrealis-realis construction (Irr_cj_real) on the choice of "da" vs. other 
# conjunctions if this variable is used to predict the choice by itself? What is the influence? Does the construction ("Y") favor or 
# disfavor "da"?
#Function to use: glm(, family="binomial")
#Note: you will have to recode the dependent variable so that "no" and "odnako" are treated as the same value, i.e., "not da"; recode() in the car package or fct_collapse() in the 
# forcats package could be used to do it. Or you could do it by hand.

conjdata <- read.table("C:/Users/Jacob/Desktop/Corpus Ling/conjunctions2013.txt", header = TRUE)

# Encode all instances of "no" and "odnako" to 0 and "da" to 1:
library(dplyr)
conjdata <- conjdata %>%
  mutate(conj = ifelse(conj %in% c("no","odnako"), 0, 1))

#make the model
model <- glm(conj ~ Irr_cj_real, family = "binomial", data = conjdata)
summary(model)
#p value is less than 2e^-16 so there is a significant effect that the construction has on the use of "da". 
#"Da" appears more with the IRR construction: est is high.

#4. Is there a significant influence of the irrealis-realis construction (Irr_cj_real) on the choice of "da" vs. other conjunctions if 
# genre and conj_type are also included in the model? Do not include interactions. Do these results agree with those in Kapatsinski (2009) or not?

#2nd model with all variables 
full_model <- glm(conj ~ Irr_cj_real + genre + conj_type, family = "binomial", data = conjdata)
summary(full_model)

#With the written genre and the verbal type conjugation, "da" is chosen much less (esp the latter). This agrees with Kapatsinski 2009, which 
#found that "da" was favored more with nominal conjugations and was less favored compared with "odanko" in written media.

#5. Start from the full model in #4, and eliminate each of the predictors from it in turn, so that you end up with models that have 
#all but one available predictors included. Do all predictors significantly contribute to the full model? Which one contributes the 
# most to the full model according to BIC?

# BIC of the full model
bic_full <- BIC(full_model)

# List of all the predictors
predictors_to_eliminate <- c("Irr_cj_real", "genre", "conj_type")

# Initialize a vector to store BIC values
bic_values <- numeric(length(predictors_to_eliminate))

# Perform the analysis for each predictor elimination
for (i in 1:length(predictors_to_eliminate)) {
  formula_reduced <- as.formula(paste("conj ~", paste(predictors_to_eliminate[-i], collapse = " + ")))
  reduced_model <- glm(formula_reduced, family = "binomial", data = conjdata)
  print(reduced_model)
  bic_values[i] <- BIC(reduced_model)
  print(bic_values)
}

most_contributing_predictor <- predictors_to_eliminate[which.min(bic_values)]

# Print the BIC values and the most contributing predictor
cat("BIC values for models with each predictor eliminated:\n")
for (i in 1:length(predictors_to_eliminate)) {
  cat(paste(predictors_to_eliminate[i], ": ", bic_values[i], "\n"))
}
cat("Most contributing predictor: ", most_contributing_predictor, "\n")

#the BIC found that genre is the most contributing factor (though the presence of IRR should be more?)

#6. Plot predictions of the full model in #4

install.packages("sjPlot")
library(sjPlot)

plot_model(full_model, type = "pred")

#7. Interpret the significant coefficients in the model in #4. What are the significant influences on the choice of "da" and what are 
# the directions of their effects? In other words, which values of the predictors favor "da" (relative to what other values) and which 
# values disfavor it?

summary(full_model)

"
In summary, the presence of the IRR construction stronly favors the use of 'da'. 
However, in both written works and when used with verbal conjugations 'da' is disfavored. 
The p value for 'da' with nominal conjugations was insignificant, but would have shown a disfavoring effect.
"