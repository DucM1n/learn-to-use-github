import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
playing = True

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit
    
class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'The deck has: ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card
    
class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # keep track of aces

    def add_card(self, card):

        # card passed in 
        # from Deck.deal() --> single_card(suit, rank)
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):

        # if total value > 21 and there are aces
        # then change my ace to be a 1 instead of an 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

test_deck = Deck()
test_deck.shuffle()

class Chips:
    def __init__(self, total = 100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Enter your bet: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
        else:
            if chips.bet > chips.total:
                print("Insufficient chips. You have: {}".format(chips.total))
            else:
                break

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        x = input('Hit or stand? Enter h or s: ')

        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            playing = False
        else:
            print("Invalid input. Please enter 'h' or 's'.")
            continue
        break

def show_some(player, dealer):

    # dealer.cards[1]

    # Show only one of the dealer's cards
    print("\nDealer's Hand:")
    print("First card hidden!")
    print(dealer.cards[1])

    # Show all of the player's cards
    print("\nPlayer's Hand: ")
    for card in player.cards:
        print(card)

def show_all(player, dealer):

    # show all the dealer's cards
    print("Dealer's Hand: ")

    for card in dealer.cards:
        print(card)

    # calculate and display value (J + K == 20)
    print("Dealer's Hand Value: {}".format(dealer.value))

    # Show all of the player's cards
    print("\nPlayer's Hand: ")
    for card in player.cards:
        print(card)
    print("Player's Hand Value: {}".format(player.value))

def player_busts(player, dealer, chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()

def push(player, dealer):
    print("It's a push!")

while True:
    # print an opening statement
    print("Welcome to Blackjack!")

    # create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()

    for _ in range(2):
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

    # set up the player
    player_chips = Chips()  # remember the default value is 100

    # prompt the player for their bet
    take_bet(player_chips)

    # Show the hands
    show_some(player_hand, dealer_hand)

    while playing: # recall this variable from our hit_or_stand function

        # prompt the player to hit or stand
        hit_or_stand(deck, player_hand)

        # show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # if player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    if player_hand.value <= 21:

        while dealer_hand.value < player_hand.value:
            hit(deck, dealer_hand)

        # Show all hands
        show_all(player_hand, dealer_hand)

        # Check who wins
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        elif player_hand.value < dealer_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    print("Player's Chips: {}".format(player_chips.total))

    # Ask to play again
    new_game = input("Would you like to play again? (y/n): ")
    if new_game.lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for playing!")
        break