import random


def poker(hands):
    '''Return the best hand: poker([hand,...]) => [hand,...]'''
    return allmax(hands, key=hand_rank)

def deal(numhands, n=5, deck=[r+s for r in '23456789TJQKA' for s in 'SHDC']):
    '''Shuffle the deck and deal out numhands n-card hands.'''
    random.shuffle(deck)
    return [deck[n*i : n*(i+1)] for i in range(numhands)]

def allmax(iterable, key=None):
    '''Return a list of all items equal to the max of the iterable.'''
    key = key or (lambda x: x)
    result, maxval = [], max(iterable, key=key)
    return [i for i in iterable if key(i) == key(maxval)]

def hand_rank(hand):
    '''Return a value indicating the ranking of a hand.'''
    # counts is the count of each rank; ranks lists corresponding ranks
    # E.g. '7 T 7 9 7' => counts = (3, 1, 1); ranks = (7, 10, 9)
    groups = group(['--23456789TJQKA'.index(r) for r, s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    flush = len(set([s for r,s in hand])) == 1
    return (9 if (5,) == counts else
            8 if straight and flush else
            7 if (4, 1) == counts else
            6 if (3, 2) == counts else
            5 if flush else
            4 if straight else
            3 if (3, 1, 1) == counts else
            2 if (2, 2, 1) == counts else
            1 if (2, 1, 1, 1) == counts else
            0), ranks

def group(items):
    '''Return a list of [(count, x)...], highest count first, then highest x first.'''
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse=True)

def unzip(pairs): return zip(*pairs)


def test():
    '''Test cases for the functions in poker program.'''
    sf1 = '6C 7C 8C 9C TC'.split() # Straight Flush
    sf2 = '6D 7D 8D 9D TD'.split() # Straight Flush
    fk = '9D 9H 9S 9C 7D'.split() # Four of a Kind
    fh = 'TD TC TH 7C 7D'.split() # Full House
    tp = '5S 5D 9H 9C 6S'.split() # Two pairs
    al = 'AC 2D 4H 3D 5S'.split() # Ace-Low Straight

    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2] 
    assert poker([sf1, fk, fh]) == [sf1]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf1]) == [sf1]
    assert poker([sf1] + 99 * [fk]) == [sf1]
    
    assert hand_rank(sf1) == (8, (10, 9, 8, 7, 6))
    assert hand_rank(fk) == (7, (9, 7))
    assert hand_rank(fh) == (6, (10, 7))
    return 'tests pass'

test()
