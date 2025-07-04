import random

def getWords(filename):
    try:
        with open(filename, 'r') as file:
            words = []
            
            for line in file:
                word = line.strip().upper()
                if word:
                    words.append(word)
            
            return tuple(words)
            
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
        print("Please make sure the file exists in the same directory.")
        return tuple()

def loadVocabulary():
    print("Loading files...")
    
    articles = getWords("articles.txt")
    nouns = getWords("nouns.txt") 
    verbs = getWords("verbs.txt")
    prepositions = getWords("prepositions.txt")
    
    if not all([articles, nouns, verbs, prepositions]):
        print("Warning: Some files are missing or empty!")
        print("Using default vocabulary instead.")
        articles = ("A", "THE")
        nouns = ("BOY", "GIRL", "BAT", "BALL")
        verbs = ("HIT", "SAW", "LIKED")
        prepositions = ("WITH", "BY")
    
    return articles, nouns, verbs, prepositions

def sentence():
    return nounPhrase() + " " + verbPhrase()

def nounPhrase():
    return random.choice(articles) + " " + random.choice(nouns)

def verbPhrase():
    return random.choice(verbs) + " " + nounPhrase() + " " + \
           prepositionalPhrase()

def prepositionalPhrase():
    return random.choice(prepositions) + " " + nounPhrase()

def main():
    global articles, nouns, verbs, prepositions
    
    articles, nouns, verbs, prepositions = loadVocabulary()
    
    print(f"Vocabulary loaded:")
    print(f"  Articles: {len(articles)} words")
    print(f"  Nouns: {len(nouns)} words") 
    print(f"  Verbs: {len(verbs)} words")
    print(f"  Prepositions: {len(prepositions)} words")
    print()
    
    try:
        number = int(input("Enter the number of sentences: "))
        print()
        
        for count in range(number):
            print(f"{count + 1}. {sentence()}")
            
    except ValueError:
        print("Error: Please enter a valid number.")

if __name__ == "__main__":
    main()