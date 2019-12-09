# Python3 Script
# Run to start program: python3 BoggleSolver.py

from collections import defaultdict
# Typing alias
from typing import List, Set, Tuple, NewType
TrieNode = NewType
# Toolkit to get valid words in the English Language
from nltk.corpus import words

class ValidWordsGenerator:
    def __init__(self, board : List[List[int]], wordDictionary: List):
        self.board = board
        self.wordTrie = Trie(wordDictionary)
        self.directions = [[-1,-1], [-1, 0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]] 
        self.rowLen = len(self.board)
        self.colLen = len(self.board[0])
        self.minimumValidWordLength = 3
        self.validWords = set()

    def getAdjCells(self, x : int , y : int ):
        '''
        Generator function to iterate over the adjacent cells of a given cell(x,y)
        '''
        adjCells = []

        # For every direction possible
        for move in self.directions:
            # Calculate the new coordinates after moving in a direction from the passed in cell (x,y)
            new_x = x + move[0]
            new_y = y + move[1]
            # If there exists a cell in the direction (not out of bounds)
            if(0 <= new_x < self.rowLen and 0 <= new_y < self.colLen):
                # Add it as an adjacent cell
                yield [new_x, new_y]

    def DFS(self, row : int , col : int, board , trie: TrieNode , incoming_word: str):
        '''
        Checks if a given cell's letter is present in the TrieNode's children.
        If so, and the child letter TrieNode is marked as valid (representing the end of a valid word) of the TrieNode, 
               we have found a valid word!
        Otherwise, the function performs the DFS on the cell's adjacent cells, while passing in the child letter's TrieNode.
        '''

        # If the cell has been visited already, stop the DFS in that direction
        if board[row][col] == '*':
            return

        # Reference to get the children of the TrieNode
        children = trie.children

        # Get the letter of the cell and convert it to uppercase
        letter = self.board[row][col].upper()

        # Mark cell as visited
        board[row][col] = '*'
        
        # If the letter is in the TrieNode's children
        if letter in children:
            # Append letter to the incoming word
            incoming_word += letter 
            # If the cell's letter represents the end of a valid word in the TrieNode
            if children[letter].valid and len(incoming_word) >= self.minimumValidWordLength:     
                # Hooray we have found a valid word ! 
                self.validWords.add(incoming_word)  
            # Perform DFS on this cell's adjacent cells 
            # to see if a valid word can be made if we add more letters
            for cell in self.getAdjCells(row, col):
                self.DFS(cell[0], cell[1], board , children[letter], incoming_word)

        # Allows for letter to be visited in different branches of the recursion
        board[row][col] = letter

    def findValidWords(self):
        '''
        Calls DFS on each cell in the board in order to generate all possible valid words.
        '''
        root = self.wordTrie.root
        for row in range(self.rowLen):
            for col in range(self.colLen):
                self.DFS(row, col, self.board , root, '')
    
    def getValidWords(self):
        '''
        Returns the set of valid words found in the board.
        '''
        self.findValidWords()
        return self.validWords

class TrieNode:
    def __init__(self):
        self.valid = False
        self.children = {}

class Trie:
    def __init__(self, wordDictionary: List):
        self.root = TrieNode()
        self.wordDictionary = wordDictionary
        self.minimumValidWordLength = 3
        self.buildRoot()
        
    def buildRoot(self):
        '''
        Builds the Trie using the words(uppercased) in the wordDictionary.
        '''
        for word in self.wordDictionary:
            if len(word) >= self.minimumValidWordLength:
                self.insert(word.upper(), self.root)

    def insert(self, word : str, node : TrieNode):
        ''' 
        Breaks down a word and inserts each letter of the word into the Trie recursively.
        '''
        if not word:
            return

        # Insert one letter at a time (make sure letters are uppercase)
        firstLetter = word[0]

        children = node.children
        # If the letter is not in the TrieNode's children
        if firstLetter not in children:
            # Then insert the letter into the TrieNode's children
            children[firstLetter] = TrieNode()
            # If we are at the end of a word
            if len(word) == 1:
                # Mark the letter as the end of a valid word
                children[firstLetter].valid = True
        
        # Recursively insert letters down the tree
        self.insert(word[1:], children[firstLetter])

def generateValidWords(board: List[List[int]], wordDictionary : List):
    '''
    Main function to call to outputs set of valid words for a 4x4 board. 
    If no valid words exist, an empty set is returned.
    '''
    validBoardSize = 4

    if len(board) != validBoardSize or len(board[0]) != validBoardSize:
        return "Invalid board size. Please use a 4x4 board."

    generator = ValidWordsGenerator(board, wordDictionary)
    validWords = generator.getValidWords()
    return validWords

# Driver Code
def main():
    # If no valid words dictionary is provided by the user, I will use this wordDictionary I created
    # using nltk library which has a dictionary of all valid words in the English Language
    wordDictionary = words.words()

    board = [['R','A','E','L'],
             ['M','O','F','S'],
             ['T','E','O','K'],
             ['N','A','T','I']]
    ans = generateValidWords(board, wordDictionary)
    print(ans)

    '''
    Outputs...

    {'MEN', 'AFOOT', 'RAMENT', 'MENTOR', 'ORA', 'ROTA', 'TEAT', 'ITA', 'EAN', 'RAMET', 'TOATOA', 'OFO', 'FOOT', 
    'SELF', 'SKI', 'TOM', 'TOME', 'MAO', 'OMEN', 'ETA', 'TENT', 'SFOOT', 'SEA', 'SKIT', 'MOOT', 'TOOK', 'AMT', 
    'FEAR', 'NETI', 'KOAE','TOETOE', 'ATOM', 'NAOS', 'EAT', 'ATEF', 'ELF', 'FOO', 'AMEN', 'LEORA', 'IOTA', 'MAFOO', 
    'FLEAM', 'MEANT', 'FOR', 'FEN', 'NATE', 'ITO', 'ROOK', 'NEO', 'ANTE', 'TAOS', 'ROME', 'TOA', 'FAM', 'ROOT', 
    'TAT', 'SKITE', 'MOE', 'ETNA', 'KITE', 'SOT', 'SOFAR', 'FLEA', 'EOAN', 'ARM', 'ROTATE', 'FENT', 'TEN', 'NET', 
    'FORA', 'TOOM', 'FEAT', 'LEA', 'FORME', 'ITEN', 'OKI', 'NAT', 'ITEA', 'LEAR', 'NEA', 'ROTAN', 'AMOR', 'MOOSE', 
    'RAMEAN', 'MARO', 'FOAM', 'RAFE', 'FOMENT', 'ARMET', 'MAE', 'MEAN', 'TEMA', 'RAME', 'ATI', 'MEO', 'ROTE', 'TOE', 
    'NEAT', 'LES', 'ARO', 'AME', 'TOAT', 'TANE', 'FARM', 'ROT', 'ANT', 'FORM', 'MOTET', 'AOTEA', 'LEO', 'OES', 'SEAR', 
    'KOA', 'FOT', 'MAR', 'TOMA', 'FAR', 'OAM', 'OATEN', 'TEAN', 'TAEN', 'TOI', 'KIT', 'FET', 'AMENT', 'ATMO', 'TOO', 
    'SOFA', 'LEAFEN', 'MOTE', 'FAME', 'OSE', 'SOOT', 'MOT', 'ELS', 'TATE', 'MOR', 'NEMA', 'SOE', 'ROMEO', 'OMAR', 'MOO',
    'OAT', 'KOI', 'ROE', 'SOTIK', 'TORA', 'TOSK', 'MEAT', 'MENT', 'LEAM', 'MET', 'META', 'OAR', 'OAF', 'SOK', 'TAO', 
    'OTATE', 'TAN', 'KITAN', 'ATMA', 'EAR', 'NAE', 'LEAF', 'TEA', 'FOE', 'TOOT', 'ATEN', 'FARO', 'FAE', 'SEAM', 'KOS', 
    'NEF', 'ATIK', 'ROOF', 'FETOR', 'FELS', 'TOR', 'KIOEA', 'FEMORA', 'TORMA', 'ATE', 'TAE', 'RAM', 'AES', 'TORMEN', 'SKOO', 
    'MORA', 'ITEM', 'ROAM', 'KOTA', 'FORAMEN'}
    '''
main()
