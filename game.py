# Import the random librabry
import random


# Initalize the values, ranks and suits in the deck
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}


# Crate a class
# must have card suit, rank and value initialized

class Card():

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        return self.rank + ' of ' + self.suit


# Deck Class

class Deck():

    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                # Create the card object
                created_card = Card(suit,rank)

                self.all_cards.append(created_card)
    
    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()


# Player Class
    # Must have some amount of money to start off

class Player():
    
    def __init__(self,name):
        self.name = name
        self.all_cards = []
        self.bank = 20

    def remove_one(self):
        return self.all_cards.pop(0)

    def add_cards(self, new_cards):
        if type(new_cards) == type([]):
            self.all_cards.extend(new_cards)
        else:
            self.all_cards.append(new_cards)
    
    def bet(self):
        self.bank -= 10
        return 10

    def __str__(self):
        return f'Player {self.name} has ${(self.bank)} in the bank.'


# Computer Dealer
dealer = Player("Dealer")


# Human Player
player = Player(input("What would you like to call yourself? "))


# Create a deck of cards
new_deck = Deck()
new_deck.shuffle()


# initialize the pot
pot = 0

# Start the game
game_on = True


# While game is on
while game_on:

    # Game is done when the player or the dealer loses all of their money in the bank
    if player.bank <= 0:
        print(f"{player} has run out of money. You have lost!")
        game_on = False
        break

    if dealer.bank <= 0:
        print("The dealer has lost all of its money. You have won!")
        game_on = False
        break


    # Human player places bets with his money
    pot = pot + dealer.bet()
    pot = pot + player.bet()
    print("    MONEY IN THE BANK!")
    print(dealer)
    print(player)
    print(pot)


    # Deal cards to both players
    for x in range(2):
        # Human player starts with two cards being dealt to them and placed face up
        player.add_cards(new_deck.deal_one())
        # Computer player start with two cards being dealt to them, one face down and one face up
        dealer.add_cards(new_deck.deal_one())
    print("    CARDS DEALT!")
    print(f"You have the {player.all_cards[0]} and {player.all_cards[1]}")
    print(f"The dealer has {dealer.all_cards[0]} and one face down card")


    #### Players Turn ####
    # In game the player goes first being asked to hit or stay with a maximum of five times
        # player tries and gets closer to a value of 21
        # if plaer goes over the hand is lost
    players_turn = True
    print("    Player's Turn!")

    while players_turn:

        # Initialize the total value and the ace count
        total_value = 0
        ace_count = 0

        # Checking how man aces aare there and the total value
        for card in player.all_cards:
            if card.rank == "Ace":
                ace_count += 1
            total_value += card.value

        # Changing value of ace to 1 if value is morethan 21
        while ace_count > 0:
            if total_value <= 21:
                ace_count = 0
            else:
                total_value -= 10
                ace_count -= 1

        # Bust check
        if total_value > 21:
            print("  ###  Uh OH! You bust!  ###")
            total_value = 0
            break

        # To many cards in the hand check
        if len(player.all_cards) > 4:
            print("  ###  You hae reached the maximum amount of cards you can be dealt!  ###")
            break

        # Hit or stay check
        choice = 'WRONG!'
        while choice not in ['Hit', 'Stay']:
            choice = input("Would you like to hit or stay? ").capitalize()

        if choice == 'Hit':
            player.add_cards(new_deck.deal_one())
            print("    YOU HIT!")
            print("You have:")
            for card in player.all_cards:
                print(card)
            continue
        else:
            break


    #### Dealers Turn ####
    # The Dealer then goes and hits until it beats the player or it busts
        # if the dealer beats the plyers cards then the dealer wins the players pot and the hand is over
        # if the dealer goes over 21 then the player wins the pot and the hand is over
    dealers_turn = True
    print("    Dealer's turn!")

    while dealers_turn:

        # Initialize total value and ace check
        dealer_value = 0
        dealer_ace_count = 0

        # Checking how man aces are there and the dealer value
        for card in dealer.all_cards:
            if card.rank == "Ace":
                dealer_ace_count += 1
            dealer_value += card.value

        # Changing value of ace to 1 if value is morethan 21
        while dealer_ace_count > 0:
            if dealer_value <= 21:
                dealer_ace_count = 0
            else:
                dealer_value -= 10
                dealer_ace_count -= 1

        # Bust check
        if dealer_value > 21:
            print("  ###  Uh OH! The dealer bust!  ###")
            dealer_value = 0
            break

        # To many cards in the hand check
        if len(dealer.all_cards) > 4:
            break

        # Telling the dealer to stay
        if total_value == 0 or dealer_value >= 17:
            print("The dealer stays with this hand:")
            for card in dealer.all_cards:
                print(card)
            break
        if dealer_value < 17:
            dealer.add_cards(new_deck.deal_one())
            print("The dealer gets another card!")
            continue


    # Create an if, elif and an else statement
    # If the the player won, then the player gets the pot
    if total_value > dealer_value:
        pot = 0
        player.bank += 20
        print("  ***  You won the hand and the pot!!!  ***")
    # If the dealer has won, then the dealer gets the pot
    elif total_value < dealer_value:
        pot = 0
        dealer.bank += 20
        print("  ***  The dealer won the hand and the pot!!!  ***")
    # If the game ends in a draw, then the money gets distributed evenly between both players
    if total_value == dealer_value:
        pot = 0
        player.bank += 10
        dealer.bank += 10
        print("  ***  No one won!!!  ***")

    for card in range(len(player.all_cards)):
        player.all_cards.pop()

    for card in range(len(dealer.all_cards)):
        dealer.all_cards.pop()