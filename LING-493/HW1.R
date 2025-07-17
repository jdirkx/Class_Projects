"
Jacob Dirkx
HW 1
10/18/23
Worked with Eloy Vetto and Clay Worthington
"

setwd("/Users/Jacob/Desktop/Corpus Ling/Buckeye Corpus")
zipfiles <- list.files(pattern="*.zip",recursive=T,include.dirs=T)
for (i in zipfiles) { unzip(zipfile = i)}

#1. Read in the .txt corpus files from the Buckeye corpus (uploaded on canvas), split into words based on whitespace (spaces, tabs, new lines). 
filenames <- list.files(pattern = "*.txt", recursive = T, include.dirs= T)
k=0
for (i in filenames)
{
  k = k+1
  if (k == 1) {
    corpus <- scan(file=i, what="char", sep=" ", quote="") 
  }
  else { corpus <- c(corpus, scan(file=i, what="char", sep=" ", quote=""))}
  if (k %% 2 == 0) { print(k) }
}
corpus <- corpus[!grepl("\\b<.+?>\\b",corpus)]
corpus <- corpus[!is.na(corpus)]

#2. Create a list of word frequencies based on these files, using table(). 
freq <- table(corpus)
sort(freq,de=T)

#3. Remove strings that are not words (and their frequencies) from the table of word frequencies. Justify these removals with an operational definition of 'word'.

#I've moved the removal of nonwords(tags) to part 1 in line 18. 

#4. Find all instances of the lemma 'cat' in the corpus. Provide an operational definition of 'lemma'.
freqcat <- freq[grep('\\bcat\\b',names(freq),perl=TRUE,value=TRUE)]
print(freqcat)
#Lemmas are 'dictionary forms' or 'citation forms' of words that can be indexed in corpus linguistics.
#The lemma 'cat' occurs 6x in the corpus.

#5. Create a table of collocates for the word 'cat' occurring in the pre-cat and post-cat positions. Report the frequency of each collocate.
catposition <- grep('\\bcat\\b',corpus)
for (i in length(catposition)){
  catposition=catposition-1
  pre.cat <- corpus[catposition]
  print(pre.cat)
}
catposition <- grep('\\bcat\\b',corpus)
for (i in length(catposition)){
  catposition=catposition+1
  post.cat <- corpus[catposition]
  print(post.cat)
}
freqpre.cat <- table(pre.cat)
sort(freqpre.cat,de=T)
#pre-cat collocations: "a" occurs 4x, "the" occurs 1x, "copy" occurs 1x
freqpost.cat <- table(post.cat)
sort(freqpost.cat,de=T)
#post cat collocations: "something", "and", "i'd", "that", "you're", "yknow" each occur 1x

#6. Create a table of collocates for the word 'dog' occurring in the pre-dog and post-dog positions. Report the frequency of each collocate. Do the collocates of 'dog' seem systematically different from the cat collocates? How?
dogposition <- grep('\\bdog\\b',corpus)
print(dogposition)
for (i in length(dogposition)){
  dogposition=dogposition-1
  pre.dog <- corpus[dogposition]
  print(pre.dog)
}
dogposition <- grep('\\bdog\\b',corpus)
for (i in length(dogposition)){
  dogposition=dogposition+1
  post.dog <- corpus[dogposition]
  print(post.dog)
}
freqpre.dog <- table(pre.dog)
sort(freqpre.dog,de=T)
#pre-dog collocations: "a" occurs 14x, "my" occurs 6x, "the" occurs 3x, "had", "hot", "looking", "nice", "our", "that", "yard", "your" each occur 1x
freqpost.dog <- table(post.dog)
sort(freqpost.dog,de=T)
#post dog collocations: "and" occurs 4x, "but" occurs 2x, "to" occurs 2x, "yknow" occurs 2x, "a", "about", "at", "behaves", "can", "could", "for", "go", "has", "he's", hind", "my", "named", "on", "stands", "takes", "they", "tripping", "trying", "why", "yeah occur 1x
#Dog collocates seem to be similar to cats - possessives, articles etc being most common - but with a much greater variety of words exponentially related to how much more it appears in the corpus.

#7. Formulate a search query to find all single-word repetition disfluencies in the corpus. What difficulties do you face in this endeavour? Are there any unclear cases where you don't know if something is a repetition disfluency?
repwords <- character(0)
for (i in 1:(length(corpus))) {
    if (!any(is.na(corpus[i:(i+1)])) && corpus[i] == corpus[i+1]) {
      word <- corpus[i]
      repwords <- c(repwords, word)
    }
}
#sorting based on individual word frequency
repwords_kinds <- unique(repwords)
print(repwords_kinds)
#With the removal of the tags in the corpus, I can only tabulate single word repetition difluencies that were notated as distince strings by the corpus authors. Additionally, it is hard to garner other information on the difluencies, such as location of occurance etc.

#8. Search for the string 'cat' followed by any number of letter characters, including zero characters. Tabulate the resulting words (and their frequencies). What is the precision of this search query in retrieving lemmas of 'cat'?
freq_catstrings <- freq[grep('\\bcat',names(freq),perl=TRUE,value=TRUE)]
freq_catstrings <- freq_catstrings[order(freq_catstrings, decreasing = TRUE)]
print(freq_catstrings)
# catholic x64, catch x18, cats x10, catalog x8, cat x6, catholics x6, category x3, catching x2, catalog's x1, cataract x1, catastrophe x1, catches x1, cater x1, caterer x1, catfish x1
# I would say this is of pretty high precision as it searches for strings beginning with the characters 'cats'. However, on a linguistic level, this isn't really accurate as many of these words are unrelated to cats or feline things.

#9. Replace every 'dog' with 'cat'. 
corpus <- gsub("dog", "cat", corpus)

#10. Save the de-dogged corpus into a file.
write.csv(corpus, "de-dogged_corpus.csv", row.names = FALSE)
