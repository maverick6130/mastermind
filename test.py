import mastermind
import random
import time

n= 12
k= 7

play_self = True
code = []

# pick a code in autoplay
if play_self:
    for i in range(k):
        code.append( random.randint(0, n-1) )

# calculate response in auto play
def get_auto_response( move ):
    assert( len(move) == k )
    rd = random.randint(1,10)
    if rd > 2:
        reds = 0
        for i in range(k):
            if move[i] == code[i]:
                reds += 1
        matched_idxs = []
        whites_and_reds = 0
        for i in range(k):
            c = move[i]
            for j in range(k):
                if j in matched_idxs:
                    continue
                if c == code[j]:
                    whites_and_reds += 1
                    matched_idxs.append(j)
                    break
    else:
        reds = random.randint(0,k-1)
        whites_and_reds = random.randint(reds,k-1)
    print("found a move:")
    print( move )
    print( "Enter red count: "  +str(reds) )
    print( "Enter white count: "+str(whites_and_reds-reds) )
    return reds, whites_and_reds-reds

def get_human_response():
    red = int(input("Enter red count: "))
    white = int(input("Enter white count: "))
    if white+red > k:
        raise Exception("bad input!")
    return red,white

def play_game():
    if play_self:
        print("Chosen code:")
        print(code)
    # ~~~~ API CALL: We tell your code our choice of n and k
    #      n is the number of colors
    #      k is the size of the sequence
    #
    mastermind.initialize(n,k)
    guess_list = []
    response_list = []
    red = 0
    while red < k:
        # ~~~~ API CALL: we collect your move
        # Your response should be of a list of k numbers. Ex. [ 2, 4, 4, 5]
        #  The numbers indicate the colors
        #
        move = mastermind.get_second_player_move()
        guess_list.append(move)
        if play_self:
            red, white = get_auto_response( move )
        else:
            print("found a move:")
            print( move )
            red, white = get_human_response()
        # ~~~~ API CALL: we collect your guesses
        # We send you reds and white responses
        #  red  : number of correct colors in correct positions 
        #  white: number of correct colors in wrong positions
        # 
        mastermind.put_first_player_response( red, white )
    print("Game solved in " + str(len(guess_list)) +" moves for n = " + str (n)+ " and k = " + str(k)+ "!")

t0 = time.time()
play_game()
t1 = time.time()
print("Code took {} seconds".format(t1-t0))
