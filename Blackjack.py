# This is a program that plays a simple game of blackjack with the 
# user. This was made in 2021 by William Elegy.
import random


# These Tuples and dictionary are used for building cards.
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7,'Eight':8, 
          'Nine':9, 'Ten':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14}
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')


class Card:
# The Card class is used to track of suits and values of cards in the 
# deck.  It can also be used to display cards to the player.
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:
# The Deck class is used to build a deck by using the Card class, 
# shuffle the deck, and deal cards.
    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()


class Player:
# The Player class is used to keep track of the value of the player's 
# and dealer's hand.  It can draw cards and return a string with info 
# on the player's and dealer's hands.
    def __init__(self,name):
        self.name = name
        self.hand = 0

    def draw(self,new_card):
        if self.hand + new_card.value > 21 and new_card.rank == 'Ace':
            self.hand += 1
        else:
            self.hand += new_card.value

        print(f'{self.name} drew {new_card}')

    def __str__(self):
        return f"{self.name}'s current score is {self.hand}"


class Bank:
# The Bank class is used to keep track of the player's bank.  It is 
# also used to add or remove currency from the player's bank if they 
# win or lose, as well as prompt the player to bet before each hand.
    def __init__(self):
        self.balance = 100
        self.wager = 0

    def bet(self,amount):
        self.wager = int(amount)

        while self.balance - self.wager < 0 or self.wager < 1:
                self.wager = int(input('Please enter a valid bet amount '))

    def win(self):
        self.balance = self.balance + self.wager * 2

    def lose(self):
        self.balance = self.balance - self.wager

    def __str__(self):
        return f"Your current balance is {self.balance}"


def twentyone(score):
# The twentyone function is used to calculate if the player or dealer 
# has won with a perfect score.
    if score.hand == 21:
        return True

    else:
        return False


def win_check(player,dealer):
# The win_check function is used to check if the player or dealer has 
# won.
    if 21 - player.hand < 21 - dealer.hand and player.hand != dealer.hand:
        return True
        print('problem here')

    else:
        return False
        print('problem here')


def bust_check(score):
# The bust_check function is used to check if the player or dealer has 
# exceeded a score of 21.
    if score.hand > 21:
        return True

    else:
        return False


def again_check():
# The again_check function prompts the player to select whether they 
# would like to play another round.
    check = ''

    while check.upper() != 'Y' and check.upper() != 'N':
        check = input('Play Again? (Y or N) ')

    if check.upper() == 'Y':
        return True

    else:
        return False

def hit_or_stay():
# The hit_or_stay function prompts the player to select whether they 
# want to draw another card or stay.
    pinput = ''

    while pinput.upper() != 'H' and pinput.upper() != 'S':
        pinput = input('Hit or Stay? (H or S)')

    if pinput.upper() == 'H':
        return True

    elif pinput.upper() == 'S':
        return False

    else:
        print('hit_or_stay error')


def main():
# The functions previously defined will be put to use in the main 
# function.
    playagain = True
    # Display a welcome message, create the players bank and ask 
    # for the players name.
    while True:
        print('Welcome to Blackjack!')
        human_bank = Bank()
        human_name = input('What is your name? ')
        playagain = True
        # As long as it is the first round or the player has selected 
        # that they would like to play again, this loop will run.
        while playagain == True:
            # Create an empty hand for the player.
            human = Player(human_name)
            # Create an empty hand for the dealer.
            dealer = Player('Dealer')
            # Create a new deck.
            new_deck = Deck()
            # Shuffle the deck.
            new_deck.shuffle()
            # Print the players bank.
            print(human_bank)

            # Ask the player how much they would like to bet.  
            # Once the player has entered a valid number this 
            # loop will end.
            while True:

                try:
                    human_bank.bet(int(input('How much will you bet '
                                             'on this hand? ')))

                except:
                    print('You must enter a number amount')

                else:
                    break

            pchoice = False

            # Ask the player if they would like to draw cards 
            # until they reach a score of 21, bust, or select stay.
            while (bust_check(human) == False and
                   twentyone(human) == False and
                   pchoice == False):

                print(human)

                if hit_or_stay() == True:
                    human.draw(new_deck.deal_one())

                else:
                    pchoice = True
            # While neither the player nor dealer have reached a score 
            # of 21 or busted, the dealer will draw cards until they 
            # win or bust.
            while (bust_check(dealer) == False and
                   twentyone(dealer) == False and
                   bust_check(human) == False and
                   twentyone(human) == False and
                   human.hand >= dealer.hand):
                dealer.draw(new_deck.deal_one())
                print(dealer)

            # The following if/else statements are checks for all the 
            # the ways the player could have won or lost.  The program 
            # will output how the player won or lost and handle the 
            # players bank accordingly.
            if bust_check(human) == True or twentyone(dealer) == True:
                print('Sorry, you lost!')
                print(human)
                print(dealer)
                human_bank.lose()

            elif (win_check(dealer,human) == True and
                  twentyone(human) == False and
                  bust_check(human) == False and
                  bust_check(dealer) == False):
                print('Sorry, you lost!')
                print(human)
                print(dealer)
                human_bank.lose()

            elif twentyone(human) == True:
                print('You won with a perfect score!')
                print(human)
                print(dealer)
                human_bank.win()

            elif (win_check(human,dealer) == True and
                  twentyone(human) == False and
                  bust_check(human) == False):
                print('You won!')
                print(human)
                print(dealer)
                human_bank.win()

            elif bust_check(dealer) == True:
                print('You won!')
                print(human)
                print(dealer)
                human_bank.win()

            else:
                print('There is a tie!')

            print(human.hand)
            print(dealer.hand)

            # Restart the game if the player wants to play again.
            if again_check() == True:
                playagain = True
                # Exit the program if the player runs out of money.
                if human_bank.balance == 0:
                    print('You ran out of money!')
                    playagain = False
            # Exit the program if the player does not want to play 
            # again.
            else:
                playagain = False

        if playagain == False:
            print('Thanks for playing!')
            break


main()
