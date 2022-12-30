import itertools
import random

rank_dict = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6,
             '8': 7, '9': 8, '10': 9, 'Jack': 10, 'Queen': 11,
             'King': 12, 'Ace': 13}


def player_ranks_suits(player_cards):
    player_ranks = []
    player_suits = []
    for card in player_cards:
        player_ranks.append(rank_dict[card[0]])
        player_suits.append(card[1])
    return player_ranks, player_suits


def count_ranks_suits(player_suits, player_ranks):
    count_ranks = []
    count_suits = []
    for suit in set(player_suits):
        count_suits.append((suit, player_suits.count(suit)))
    for rank in set(player_ranks):
        count_ranks.append((rank, player_ranks.count(rank)))
    return count_suits, count_ranks


def highest_rank(count_ranks, combination_type):
    if combination_type == 0:
        return max(filter(lambda x: x[1] == (max(count_ranks, key=lambda x: x[1])[1]), count_ranks),
                   key=lambda x: x[1])[0]
    elif combination_type == 1:
        return max(count_ranks, key=lambda x: x[0])[0]


def count_order(player_ranks):
    count = 0
    ranks = sorted(player_ranks)

    if ranks == [1,2,3,4,13]:
        return True

    for i in range(1, len(player_ranks)):
        if ranks[i] == ranks[i - 1] + 1:
            count += 1
    if count == 4:
        return True


def combinations(cards):
    player_ranks, player_suits = player_ranks_suits(cards)

    count_suits, count_ranks = count_ranks_suits(player_suits, player_ranks)

    list_of_rank_count = sorted([n[1] for n in count_ranks])
    list_of_suit_count = sorted([n[1] for n in count_suits])

    count_straight = count_order(player_ranks)

    if count_straight and 5 in list_of_suit_count:
        print('Straight Flush!')
        return 51, highest_rank(count_ranks, 1)
    elif 4 in list_of_rank_count:
        print('Four of a kind!')
        return 21, highest_rank(count_ranks, 0)
    elif list_of_rank_count == [2, 3]:
        print('Full House')
        return 8, highest_rank(count_ranks, 1)
    elif 5 in list_of_suit_count:
        print('Flush!')
        return 6, highest_rank(count_ranks, 1)
    elif count_straight:
        print('Straight')
        return 5, highest_rank(count_ranks, 1)
    elif list_of_rank_count == [1, 1, 3]:
        print('Three of a kind!')
        return 4, highest_rank(count_ranks, 0)
    elif list_of_rank_count == [1, 2, 2]:
        print('Two pairs!')
        return 3, highest_rank(count_ranks, 0)
    elif list_of_rank_count == [1, 1, 1, 2]:
        print('Pair!')
        return 2, highest_rank(count_ranks, 0)
    elif {12, 13}.issubset(set(player_ranks)):
        print('Ace and King!')
        ranks = list(filter(lambda x: x[0] < 12, count_ranks))
        return 1, highest_rank(ranks, 1)
    else:
        print('No Game!')
        return 0, 0


if __name__ == '__main__':
    suits = ('spades', 'hearts', 'diamonds', 'clubs')
    vals = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')

    all_cards = list(itertools.product(vals, suits))

    # player_cards = random.sample(all_cards, 5)
    # player_cards = [('2', 'hearts'), ('4', 'hearts'), ('Ace', 'hearts'), ('3', 'clubs'), ('5', 'spades')]
    # player_cards = [('2', 'hearts'), ('4', 'hearts'), ('6', 'hearts'), ('3', 'hearts'), ('5', 'hearts')]
    # player_cards = [('King', 'hearts'), ('Ace', 'diamonds'), ('2', 'spades'), ('8', 'hearts'), ('7', 'spades')]

    # print(combinations(player_cards))

    print(player_cards)
    print(combinations(player_cards))
