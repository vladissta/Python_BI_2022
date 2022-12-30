import random
import itertools
import algorythm

suits = ['♦︎', '♥', '♠︎', '♣︎']
# ('spades', 'hearts', 'diamonds', 'clubs',
# ♣︎♠︎ )
vals = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')

cards = list(itertools.product(vals, suits))


def replace(player, deck):
    print('Would you like to change some cards?')
    num_of_cards = list(map(int, input('Print their numbers or if you do not want - press Enter: ').split()))

    # print(num_of_cards)

    if num_of_cards:
        player.money -= len(num_of_cards) * player.bet

        new_cards = random.sample(deck.cards, len(num_of_cards))

        for card in new_cards:
            deck.cards.remove(card)

        for i, num in enumerate(num_of_cards):
            player.cards[num - 1] = new_cards[i]

        print()
        player.show_cards()
        return True


def play_pass():
    play_pass = input('Play or pass (print pass / press Enter): ')
    if play_pass == 'pass':
        return False
    else:
        return True


def play_again():
    play = input('Do you want to play again (print no / press Enter): ')
    if play == 'no':
        return False
    else:
        return True


def win(player, player_combination):
    if player_combination == 1:
        coefficient = 2
    else:
        coefficient = player_combination[0]

    print(f'You won {player.bet * (coefficient - 1)}')
    player.money += player.bet * coefficient
    print(f'Your money: {player}')


def no_game(player):
    print(f'You won {player.bet}')
    player.money += player.bet * 2
    print(f'Your money: {player}')


def lose(player):
    print('You lose')
    print(f'Your money: {player}')


def draw(player):
    print('Draw! You take your bet')
    player.money += player.bet
    print(f'Your money: {player}')


class Deck:
    def __init__(self):
        self.cards = list(cards)[:]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        dealt_cards = random.sample(deck.cards, 5)
        for card in dealt_cards:
            self.cards.remove(card)
        return dealt_cards


class Cardhoder:

    def __init__(self):
        self.cards = None
        self.name = None

    def take_five_cards(self, deck):
        self.cards = deck.deal()

    def show_cards(self):
        print(f'Cards of {self.name}:')
        for n, card in enumerate(self.cards):
            print(f'{n + 1}) {card[0]} {card[1]}')


class Player(Cardhoder):

    def __init__(self, money, name):
        super().__init__()
        self.bet = None
        self.money = int(money)
        self.name = name

    def __str__(self):
        return f'{self.money}'

    def make_a_bet(self):
        self.bet = int(input('Enter your bet: '))
        self.money -= self.bet


class Croupier(Cardhoder):

    def __init__(self):
        super().__init__()
        self.name = 'Croupier'


if __name__ == '__main__':

    player = Player(int(input('Enter your money: ')), input('Enter your name: '))
    croupier = Croupier()
    print(f'Hello, {player.name}')

    while True:
        deck = Deck()
        deck.shuffle()

        player.make_a_bet()

        player.take_five_cards(deck)
        croupier.take_five_cards(deck)

        print()

        player.show_cards()

        print()

        if not play_pass():
            if play_again():
                continue
            else:
                break
        print()

        is_replaced = replace(player, deck)

        print()

        if is_replaced:
            player.show_cards()
            if not play_pass():
                if play_again():
                    continue
                else:
                    break
            print()

        croupier.show_cards()

        print()

        print('Croupier: ')
        croupier_combination = algorythm.combinations(croupier.cards)

        print()

        print('Player: ')
        player_combination = algorythm.combinations(player.cards)
        print()

        if croupier_combination[0] == 0:
            no_game(player)

        elif croupier_combination[0] < player_combination[0]:
            win(player, player_combination)

        elif croupier_combination[0] == player_combination[0]:

            if croupier_combination[1] < player_combination[1]:
                print(f'You have a higher card!')
                win(player, player_combination)

            elif croupier_combination[1] == player_combination[1]:
                draw(player)

            else:
                print(f'Croupier have a higher card!')
                lose(player)

        else:
            lose(player)
        print()

        if not play_again():
            break
        else:
            print()
            continue
