import string
import random

class HangmanGame():
    def __init__(self):
        self.wordList = dict()
        self.lives = 0

    def AddCategory(self, key, value):
        self.wordList[key] = value
        
    def printCategories(self, id=-1):
        if id == -1:
            temp = (f"""Select\tCategory Name\n{'-'*30}\n""")
            for idx, keys in enumerate(self.wordList):
                  temp += (f"""{idx}\t{keys}\n""")
            print(temp)
        else:
            for idx, keys in enumerate(self.wordList):
                if idx == id:
                    return keys
            
    def selectCategory(self, val):
        for idx, value in enumerate(self.wordList.values()):
            if idx == val:
                return value
        
    def getLives(self, val):
        self.lives = val
        
    def HangMan(self):
        alphabet = set(string.ascii_uppercase)
        obj.printCategories()
        xval = int(input('Select the Category for the Word !!'))
        xcat = obj.printCategories(xval)
        tempList = self.selectCategory(xval)
        if tempList == None:
            print("Invalid selection of Categories !!!!")
            return
        word = random.choice(tempList).upper()
        wordL = set(word)
        self.getLives(int(input("Enter the Lives you want !!!")))
        usedL = set()


        while len(wordL) > 0 and self.lives > 0:
            tList = [l if l in usedL else '_' for l in word]
            print()
            print("Current Word is : ",'  '.join(tList), "(Cateogyr Hint): ", (xcat))

            gLetter = input("Guess the Next Letter : ").upper()

            if gLetter in (alphabet - usedL):
                usedL.add(gLetter)
                if gLetter in wordL:
                    wordL.remove(gLetter)
                else:
                    self.lives -= 1
                    print('{} is not exists, you left {} live remain !!!'.format(gLetter, self.lives))
            elif gLetter in usedL:
                print('{} word is already Used !!!'.format(gLetter))
            else:
                print('Invalid Character !!!!')

        print()
        if self.lives ==0:
            print()
            print('You Lost the Game, the Word is {}'.format(word))
        else:
            print('Congratulation! You Guess the word {} !!!!'.format(word))