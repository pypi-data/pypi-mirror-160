import string
import random

class HangmanGame():
    def __init__(self):
        self._wordList = dict()
        self._lives = 0
        self.AddCategory('Countries',['Pakistan','India','Turkey','Russia'])
        self.AddCategory('Cities',['Karachi','Lahore','Islamabad','Quetta','Peshawar'])
        self.AddCategory('Sports',['Cricket','Hockey','Football','Tennis'])


    def AddCategory(self, key, value):
        self._wordList[key] = value
        
    def printCategories(self, id=-1):
        if id == -1:
            temp = (f"""Select\tCategory Name\n{'-'*30}\n""")
            for idx, keys in enumerate(self._wordList):
                  temp += (f"""{idx}\t{keys}\n""")
            print(temp)
        else:
            for idx, keys in enumerate(self._wordList):
                if idx == id:
                    return keys
            
    def _selectCategory(self, val):
        for idx, value in enumerate(self._wordList.values()):
            if idx == val:
                return value
        
    def _getLives(self, val):
        self._lives = val
        
    def HangMan(self):
        alphabet = set(string.ascii_uppercase)
        self.printCategories()
        xval = int(input('Select the Category for the Word !!'))
        xcat = self.printCategories(xval)
        tempList = self._selectCategory(xval)
        if tempList == None:
            print("Invalid selection of Categories !!!!")
            return
        word = random.choice(tempList).upper()
        wordL = set(word)
        try:
            self._getLives(int(input("Enter the Lives you want !!! ")))
        except ValueError:  
            print("Please select 1 to 9, Invalid Selection!") 
            return
        usedL = set()


        while len(wordL) > 0 and self._lives > 0:
            tList = [l if l in usedL else '_' for l in word]
            print()
            print("Current Word is : ",'  '.join(tList), "(Cateogyr Hint): ", (xcat))

            gLetter = input("Guess the Next Letter : ").upper()

            if gLetter in (alphabet - usedL):
                usedL.add(gLetter)
                if gLetter in wordL:
                    wordL.remove(gLetter)
                else:
                    self._lives -= 1
                    print('{} is not exists, you left {} live(s) remain !!!'.format(gLetter, self._lives))
            elif gLetter in usedL:
                print('{} word is already Used !!!'.format(gLetter))
            else:
                print('Invalid Character !!!!')

        print()
        if self._lives ==0:
            print()
            print('You Lost the Game, the Word is {}'.format(word))
        else:
            print('Congratulation! You Guess the word {} !!!!'.format(word))