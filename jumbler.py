"""jumbler:  List dictionary words that match an anagram.
2023-10-02 by Jacob Dirkx

Credits: 
Myself
"""

DICT = "dict.txt"    
  
dict_file = open(DICT, "r")
def find(anagram: str):
    for line in dict_file:
        word = line.strip()
        SortWord = normalize(word)
        if SortWord == anagram:
            print(word)
def normalize(word):
    word = word.lower()
    word = sorted(word)
    return(word)
def main(): 
    anagram = input("Anagram to find> ")
    anagram = anagram.lower()
    anagram = sorted(anagram)
    find(anagram)

main()

