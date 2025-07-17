"
HW3 
Jacob Dirkx
Worked with Clay Worthington and Eloy Vetto
"

#Use the dative dataset in the languageR package. Select only the spoken data, d <- dative[dative$modality=="spoken",].

library('languageR')
library('lme4')
library('MuMIn')
d <- dative[dative$Modality=="spoken",]

#1. Determine whether speakers differ in their preference for the prepositional dative vs. the double-object dative (RealizationOfRecipient), by comparing a glm() model with only an intercept to a glmer() model with an intercept and random effect of speaker using BIC. Models should look like this:
#glm(y ~ 1) glmer(y ~ 1 + (1|Speaker))

int_only <- glm(RealizationOfRecipient ~ 1, family="binomial", d)
summary(int_only)

#int is -1.31119
#BIC is 2447.88

rand_speak <- glmer(RealizationOfRecipient ~ 1 + (1|Speaker), family="binomial", d)
summary(rand_speak)

#int is -1.33143
#BIC is 2454.9

#Because the the BIC value for the speaker model is higher than the model for just the intercept for dative constructions, 
#the intercept only model is favored. Thus speakers differ in their preference for the dative constructions.

#2. Determine whether verbs influence the choice of the prepositional dative vs. the double-object dative (RealizationOfRecipient) above and beyond speakers, by comparing a glmer() model with by-speaker random intercepts to one with by-speaker and by-verb random intercepts using BIC.

speak_verb <- glmer(RealizationOfRecipient ~ 1 + (1|Speaker) + (1|Verb), family="binomial", d)
summary(speak_verb)

#intercept is -1.4801
#BIC is 2024.6
#Because the BIC value for this model is lower than the one just with the random effect of speakers, it indicates that the goodness 
#of fit is better than the model with just the effect of speakers and thus verbs influence the choice of the dative construction
#above and beyond speakers

#3. Determine whether there are effects of LengthOfTheme and AccessOfRec on the choice of construction using glm(). Now do the same using glmer() with Verb and Speaker random effects. Do the results differ? In what way?

Length_Model <- glm(RealizationOfRecipient ~ LengthOfTheme, family="binomial", d)
summary(Length_Model)

#AIC is 2312.8

Access_Model <- glm(RealizationOfRecipient ~ AccessOfRec, family="binomial", d)
summary(Access_Model)

#AIC is 1994.2

Length_Rand_Model <- glmer(RealizationOfRecipient ~ LengthOfTheme + (1|Speaker) + (1|Verb), family="binomial", d)
summary(Length_Rand_Model)

#AIC is 1918.1

Access_Rand_Model <- glmer(RealizationOfRecipient ~ AccessOfRec + (1|Speaker) + (1|Verb), family="binomial", d)
summary(Access_Rand_Model)

#AIC is 1716.4

#In these models, the AIC gets is lower for models with the Access of Theme, and more so with the random effects of speakers and verbs
#taken into account. The differences between these is significantly greater than 2, so we can assume that the effects of 
#both Access of Recipient and Length of Theme (along with the speaker and verb in each case) are significant. 

#4. Report the results of the glmer model for AccessOfRec: "there is a significant effect of X on Y; compared to X = ... (the reference level of X), X = ... significantly favors the {PP;NP} realization of the recipient"; b(se) = ...(...), z = ..., p = ... 

#There is a significant effect of access of recipient on the realization of the recipient; 
#compared to X = accessible, given X = new significantly favors the PP realization of the recipient";
#b(se) = 0.58875(0.27027); z = 2.178; p = 0.0294

#5. Try to determine whether the effects of LengthOfTheme and AccessOfRec differ by speaker by fitting by-speaker random slopes for the two predictors. Report if the models converge, and if each of the random slopes improves the model according to BIC.

Length_BySP_Model <- glmer(RealizationOfRecipient ~ LengthOfTheme + (LengthOfTheme|Speaker) + (1|Verb) + (1|Speaker), family="binomial", d)
summary(Length_BySP_Model)
Length_BySP_Converge <- (attr(Length_BySP_Model, "converged") == 1)
cat("Length_BySP Converged:", Length_BySP_Converge, "\n")

#BIC is 1914.1, slight but significant improvement

Access_BySP_Model <- glmer(RealizationOfRecipient ~ AccessOfRec + (AccessOfRec|Speaker) + (1|Speaker) + (1|Verb), family="binomial", d)
summary(Access_BySP_Model)
Access_BySP_Converge <- (attr(Access_BySP_Model, "converged") == 1)
cat("Access_BySP Converged:", Access_BySP_Converge, "\n")

#BIC is 1783.2, not an improvement over non-random slope model

#6. Use model averaging to determine which of the Recipient (...Rec) variables are important to include in the model in addition to LengthOfTheme and the random intercepts. Can you tell which one is the best predictor of this bunch?

Model1 <- glm(RealizationOfRecipient ~ LengthOfRecipient, family="binomial", data = d)
Model2 <- glm(RealizationOfRecipient ~ AnimacyOfRec, family="binomial", data = d)
Model3 <- glm(RealizationOfRecipient ~ DefinOfRec, family="binomial", data = d)
Model4 <- glm(RealizationOfRecipient ~ PronomOfRec, family="binomial", data = d)

Av_Model_Set <- model.avg(Model1, Model2, Model3, Model4)
summary(Av_Model_Set)

#AIC of PronomOfRec Model: 1995.24
#AIC of LengthOfRecipient Model: 2065.81
#AIC of DefinOfRec Model: 2245.90
#AIC of AnimacyOfRec Model: 2380.47
#The best predictor of this group is whether the recipient is referred to pronominally or not as the AIC is lowest for that model
#Pronominality of Recipient is the only significant variables in the model, as it are the only one with a P value less than 0.05 

#7. Report the 'full model average' results for AccessOfRec as in Question 4.
#I'm assuming this is a typo and you mean to say report the results for the averaged model

#There is a significant effect of pronominalization of the recipient on the realization of the recipient; 
#compared to X = pronominal, given X = nonpronominal significantly favors the PP realization of the recipient";
#b(se) = -2.422(1.180e^-01); z = 20.513; p = 2e^-16

