import random
from time import sleep
computer_choices = 'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z'.split(', ')
player_choices = []
word_length = -1
computer_score,computer_lives ,computer_guesses = 0,0,0
player_score,player_lives ,player_guesses = 0,0,0

mode = None        #difficulty



# reading words from file and removing new line chracter

def get_words():
    global word_length
    file = open("words.txt","r+")            
    words = file.readlines()
    words = set(words)
    word_list = []
    for word in words :
        if len(word) >= 4:
            word_list.append(word[0:-1]) 
    """words = list(filter(lambda x: x[2:len(x)-2], words))"""
    words = []
    #print(word_length)
    for word in word_list:
        if len(word) <= word_length[1] and len(word) >= word_length[0]:        
            words.append(word.upper())
    #words = [x for x in words if len(x) <= word_length]
    #print(word_list)
    #print(words)
    #print(len(words))
    return words

#setting difficulty

def set_difficulty(mode):
    global word_length,computer_lives,player_lives,computer_choices,player_choices
    computer_choices = 'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z'.split(', ')
    player_choices = []
    if mode == 1:
        """easy"""
        word_length =  (4,7)
        computer_lives = 5
        player_lives = 10
        return "Easy"
    

    elif mode == 2:
        """Med"""
        word_length =  (6,9)
        computer_lives = 10
        player_lives = 7
        return "Medium"

    else:
        """hard"""
        word_length = (8,12)
        computer_lives = 12
        player_lives = 5
        return "Hard"


#computer turn

def comp_turn(comp_word,comp_chars):
    global computer_choices
    choice = random.randint(0,len(computer_choices))
    choice = computer_choices.pop(choice).upper() if choice < len(computer_choices) else computer_choices.pop(len(computer_choices)//2).upper()
    hit = 0

    for index,ele in enumerate(comp_word):

        if ele == choice :
            hit = hit + 1
            comp_chars.pop(index)
            comp_chars.insert(index,ele)
    return (hit,comp_chars)


#player turn

def pla_turn(pla_word,pla_chars):
    global player_choices
    print("****PLAYER TURN****")
    print("Letters previously used: ",player_choices if len(player_choices) > 0 else "NONE")
    choice = input("Enter your Guess :  ")
    #choice = choice[0].upper() if choice != None else None
    #print("choice",choice)
    while len(choice) <= 0:
        print("Input cannot be empty") 
        choice = input("Enter your Guess :  ")
    choice = choice[0].upper()
    while not choice.isalpha() :
        print("Input cannot be number or special character")
        choice = input("Enter your Guess :  ")
    choice = choice[0].upper()
    while choice in player_choices:
        print("Choice already used....Select different alphabet")
        choice = input("Enter your Guess :  ")[0].upper()
    player_choices.append(choice)
    hit = 0
    
    for index,ele in enumerate(pla_word):

        if ele == choice :
            hit += 1
            pla_chars.pop(index)
            pla_chars.insert(index,ele)
    return (hit,pla_chars)


#main function for game

def play():
    global computer_score,computer_lives ,computer_guesses,player_score,player_lives ,player_guesses,player_choices,mode 
    #print(type(computer_choices))
    #print("Play")
    mode = int(input("Select Difficulty Level:\n1. Easy\n2. Medium\n3. Hard\n\n"))
    diff = set_difficulty(mode)
    print("Difficulty Set to " + diff )
    words = get_words()
    com_index = random.randint(0,len(words))
    pla_index = random.randint(0,len(words)) 
    comp_word = words[com_index]
    pla_word = words[pla_index] if com_index != pla_index else words[pla_index - 1]
    comp_word_len = len(comp_word)
    pla_word_len = len(pla_word)
    computer_guesses = 0
    player_guesses  = 0
    comp_chars = ['_']* comp_word_len
    pla_chars = ['_']* pla_word_len

   # print("run")
    # playing loop 

    while not game_over(computer_lives,computer_guesses,comp_word_len,player_lives,player_guesses,pla_word_len):

        print("Computer lives: ",computer_lives)
        print("Player lives: ",player_lives)
        comp_hit,comp_chars = comp_turn(comp_word,comp_chars)
        
        if comp_hit > 0:
            print("Computer guessed correctly!")
            print("computer word : ",end = "")
            for c in comp_chars:
                print(c,end = " ")
            print()
            computer_guesses += comp_hit
        else:
            print("Computer guessed wrong!")
            print("computer word : ",end = "")

            for c in comp_chars:
                print(c,end = " ")
            print()
            computer_lives -= 1
        print("#"*20)
        sleep(3)
       # print("DEBUG     player_word",pla_word)
        print("Your word : ",end = "")
        for c in pla_chars:
            print(c,end = " ")
        print()
        pla_hit,pla_chars = pla_turn(pla_word,pla_chars)
        
       
       
        if pla_hit > 0:
            print("You guessed correctly!")
            player_guesses += pla_hit
        else:
            print("You guessed wrong!")
           
            player_lives -= 1
        print("#"*20)
        
    if player_wins(player_guesses,pla_word_len,computer_lives):
        print("You won")
        if computer_lives <= 0:
            print("Computer lost all Lives")  
        else :
            print("Hurray!!,You Guessed the word correctly.")      #print player score

    elif comp_wins(computer_guesses,comp_word_len,player_lives):
        print("Computer won")
        
        if player_lives <= 0:
            print("You lost all Lives")  
        else :
            print("Alas!!,Computer Guessed the word correctly.")
    print("Computer word is : ",comp_word)
    print("Your word was : ",pla_word)
    print("Your score was : ",player_lives*pla_word_len)
    print("Computer score : ",comp_word_len*computer_lives)
    c = input("Do you want to save score? Y/N")
    if c == 'Y' or c == 'y':
        name = input("Enter your Name: ")
        save_score(name,player_lives*pla_word_len)
        print("Thank You")

#checking for game over
def game_over(computer_lives,computer_guesses,comp_word_len,player_lives,player_guesses,pla_word_len):
    return computer_lives <= 0 or player_lives <= 0 or player_guesses == pla_word_len or computer_guesses == comp_word_len

#player winning condition
def player_wins(player_guesses,pla_word_len,computer_lives):
    return  player_guesses == pla_word_len or computer_lives <= 0
    

#comp winning condition
def comp_wins(computer_guesses,comp_word_len,player_lives):
    return computer_guesses == comp_word_len or player_lives <= 0

#to store score and player name in a file

def save_score(player_name,score):
    global mode
    file = open("high_score.txt","a")
    file.write(player_name+"*"+str(score)+"*"+str(mode)+f"\r")
    file.close()

#to fetch the score
def fetch_scores():
    file = open("high_score.txt","r")
    scores = {
        "Easy" : [],
        "Medium" : [],
        "Hard" : []
    }
    for line in file :
        name = line.split("*")
        if len(name) < 2 : 
            continue
        pla_name = name[0]
        score = name[1]
        mode = int(name[2])
        #print(mode,type(mode))
        if mode == 1:
            scores["Easy"].append({"Name" : pla_name,"Score" : score})
        elif mode == 2:
            scores["Medium"].append({"Name" : pla_name,"Score" : score})
        else:
            scores["Hard"].append({"Name" : pla_name,"Score" : score})
    file.close()
    return scores

    print(scores)
#function to display high score

def highScore():
    scores = fetch_scores()
    for i in range(0,len(scores)):
        if i == 0 :
            print("Easy : ")
            for x in scores["Easy"]:
                print(" "*8 + x["Name"]+ " " + x["Score"])
        if i == 1 :
            print("Medium: ")
            for x in scores["Medium"]:
                print(" "*8+x["Name"]+ " " + x["Score"])
        if i == 2 :
            print("Hard : ")
            for x in scores["Hard"]:
                print(" "*8 + x["Name"]+ " " + x["Score"])



#main

if __name__=="__main__":
    
    option = None
    while option != 3:
        
        print("1. Play\n2. High Score\n3. Exit\n")
        option = input("select option        ")

        if option == '1':
            play()
        elif option == '2':
            highScore()
        elif option == '3':
            print("Thank You For Playing")
            break
        else:
            print("Incorrect option entered")


    