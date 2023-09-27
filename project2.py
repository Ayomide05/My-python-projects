#import random that will be us eto shuffle
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
playing = True

#Create a class card that has a suit and rank
class card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit

#Create a deck class that holds all 52 objects and can then be shuffled around 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(card(suit,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card                    

#Create a hand class this represent what cards is in someones hand, they may be used to calculate the value of those cards using the values that are defined above   
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):

        while self.value > 21 and self.aces > 0:
            # if total value is greater than 21 and i still have an Ace
            # then change my ace to be a 1 instead of an 11 by deducting 10 from self.value and deducting 1 from self.aces which indicate we dont have ace again   
            self.value -= 10
            self.aces -= 1 

class chips: 
    def __init__(self,total=100):
        self.total = total #This can be set to a default value or supplied by user input 
        self.bet = 0


    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet    

#functions for taking bet
def take_bet(chips):

    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet"))
        except: 
            print("Sorry please provide an integer")
        else:
            if chips.bet > chips.total:
                print('Sorry, you do not have enough chips! you have: {}'.format(chips.total))         
            else:
                break

#function for taking hits. either player can take hits until they bust and hits means to take new cards# 
def hit(deck,hand):

    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

#function that prompt the player to hit or stand such that it accept the players deck and hand as arguements and assign playing as a global variable. if the player Hits, it employ the hit function above and if the player it stand it set the playing variable to false.
    
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop

    while True:
        x = input('Hit or Stand? Enter h or s ') 

        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print("Player Stands Dealer's Turn")  
            playing = False
        else:
            print("Sorry, I did not understand that, Please enter h or s only!")
            continue  
        break     

#Functions to display cards: after each time player takes a card, the dealers first card is hidden and all of the players card are visible and at the end of the hand all cards are shown.  
def show_some(player,dealer):
    # show only one of the dealers cards
    print("\n Dealer's Hand: ")
    print("First card hidden! ")
    print(dealer.cards[1])
    

    # show all (2 cards) of the player's hand/cards 
    print("\n Player's hand: ")
    for card in player.cards:
        print(card) 

def show_all(player,dealer):
    # show all the dealer's cards
    print("\n Dealer's hand: ")
    for card in dealer.cards:
        print(card) 
    #print("\n Dealer's hand: ", dealers.card,sep='\n')    
    #calculate and displays total value
    print(f"Value of Dealer's hand is : {dealer.value}")
    #show all the players card
    print("\n Player's hand: ")
    for card in player.cards:
        print(card) 

#function to hnadle end of game scenarios
def player_busts(player,dealer,chips):
    print("BUST PLAYER!")
    chips.lose_bet()
def player_wins(player,dealer,chips):
    print('PLAYER WINS!')
    chips.win_bet()
def dealer_busts(player,dealer,chips):
    print('PLAYER WINS! DEALER BUSTED!')
    chips.win_bet()        
def dealer_wins(player, dealer, chips):
    print("DEALER WINS!")
    chips.lose_bet()
def push(player,dealer):
    print('Dealer and player tie! PUSH')    

while True:
    #opening statement
    print("WELCOME TO BLACKHJACK")
    #create and shuffle the deck 
    deck = Deck()
    deck.shuffle()
    #deal two cards to each player
    player_hand = Hand()  
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    #set up the players chips
    player_chips = chips()
    #prompt the player for their bet
    take_bet(player_chips)
    #show cards but keep one dealer card hidden
    show_some(player_hand,dealer_hand)

    while playing:
        #Prompt player for hit or stand
        hit_or_stand(deck,player_hand)
        #show cards but keep one dealer card hidden
        show_some(player_hand,dealer_hand)
        #if player's hand exceed 21, ran player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)  

            break
    #if player hasn't busted, play dealer's hand until dealer's reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value  < 17:
            hit(deck,dealer_hand)         
        # show all cards
        show_all(player_hand,dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)  
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips) 
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips) 
        else:
            push(player_hand,dealer_hand)
    # inform player of their chips total
    print('\n Player total chips are at: {}'.format(player_chips.total))
    #Ask to play again
    new_game = input(" Would you like to play another hand? y/n")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing!' ) 
        break                   
