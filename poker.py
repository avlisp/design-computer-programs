def poker(hands):
    '''Return the best hand: poker([hand,...]) => hand'''
    return max(hands, key=hand_rank)

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

def card_ranks(cards):
    '''Return a list of the ranks, sorted with higher first.'''
    ranks = ['--23456789TJQKA'.index(r) for r,s in cards]

    # My solution
    # 
    # ranks = [r for r,s in cards]
    # higher_ranks = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    # for r in ranks:
    #     if not r.isdigit():
    #         ranks[ranks.index(r)] = higher_ranks.get(r)
    #     else:
    #         ranks[ranks.index(r)] = int(r)
    ranks.sort(reverse=True)
    return ranks


def test():
    '''Test cases for the functions in poker program.'''
    sf = '6C 7C 8C 9C TC'.split()
    fk = '9D 9H 9S 9C 7D'.split()
    fh = 'TD TC TH 7C 7D'.split()

    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]

    assert poker([sf, fk, fh]) == sf
    assert poker([fk, fh]) == fk
    assert poker([fh, fh]) == fh
    assert poker([sf]) == sf
    assert poker([sf] + 99 * [fk]) == sf

    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)
    return 'tests pass'

test()
