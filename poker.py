# mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC'] 
import random

def poker(hands):
    '''Return the best hand: poker([hand,...]) => [hand,...]'''
    return allmax(hands, key=hand_rank)

def deal(numhands, n=5, deck=[r+s for r in '23456789TJQKA' for s in 'SHDC']):
    '''Shuffle the deck and deal out numhands n-card hands.'''
    random.shuffle(deck)
    return [deck[n*i : n*(i+1)] for i in range(numhands)]

# My solution
# def deal(numhands, n=5, deck=mydeck):
#     deck = deck[:]
#     hands = []
#     for i in range(numhands):
#         random_hand = random.sample(deck, n)
#         hands.append(random_hand)
#         for card in random_hand:
#             deck.remove(card)
#     return hands

def allmax(iterable, key=None):
    '''Return a list of all items equal to the max of the iterable.'''
    key = key or (lambda x: x)
    result, maxval = [], max(iterable, key=key)
    return [i for i in iterable if key(i) == key(maxval)]

def hand_rank(hand):
    '''Return a value indicating the ranking of a hand.'''
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight
        return (4, max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):                          # 2 pair
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):                           # kind
        return (1, kind(2, ranks), ranks)
    else:                                          # high card
        return (0, ranks)

def card_ranks(hand):
    '''Return a list of the ranks, sorted with higher first.'''
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if ranks == [14, 5, 4, 3, 2] else ranks
    # My solution
    # ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    # ranks.sort(reverse = True)
    # if ranks == [14, 5, 4, 3, 2]:
    #     ranks[0] = 1
    #     ranks.sort(reverse = True)
    # return ranks

def straight(ranks):
    '''Return True if the ordered ranks form a 5-card straight.'''
    return (max(ranks) - min(ranks) == 4) and len(set(ranks)) == 5
    # My solution
    #
    # for i,r in enumerate(ranks):
    #     if ranks[0] != r + i:
    #         return False
    # return True

def flush(hand):
    "Return True if all the cards have the same suit."
    return len(set([s for r,s in hand])) == 1

def kind(n, ranks):
    '''Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand.'''
    for r in ranks:
        if ranks.count(r) == n: return r
    # My solution
    # for i in range(14, 0, -1):
    #     if ranks.count(i) == n:
    #         return i

def two_pair(ranks):
    '''If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None.'''
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair: return (pair, lowpair)
    # My solution
    # pairs = [r for r in ranks if ranks.count(r) == 2]
    # pairs = list(set(pairs))
    # if len(pairs) != 2:
    #     return None
    # pairs.sort(reverse=True)
    # return tuple(pairs)


def test():
    '''Test cases for the functions in poker program.'''
    sf1 = '6C 7C 8C 9C TC'.split() # Straight Flush
    sf2 = '6D 7D 8D 9D TD'.split() # Straight Flush
    fk = '9D 9H 9S 9C 7D'.split() # Four of a Kind
    fh = 'TD TC TH 7C 7D'.split() # Full House
    tp = '5S 5D 9H 9C 6S'.split() # Two pairs
    al = 'AC 2D 4H 3D 5S'.split() # Ace-Low Straight
    
    assert straight(card_ranks(al)) == True 

    assert two_pair(card_ranks(tp)) == (9, 5)
    assert two_pair([7, 4, 4, 2, 1]) == None

    fkranks = card_ranks(fk)
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7

    assert straight([9, 8, 7, 6, 5]) == True
    assert straight([9, 8, 8, 6, 5]) == False

    assert flush(sf1) == True
    assert flush(fk) == False

    assert card_ranks(sf1) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]

    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2] 
    assert poker([sf1, fk, fh]) == [sf1]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf1]) == [sf1]
    assert poker([sf1] + 99 * [fk]) == [sf1]

    assert hand_rank(sf1) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)
    return 'tests pass'

test()
