import sorting

def promptInput(numCards):
    cards = []
    print("Hello! Welcome to the Poker Odds Calculator.")
    for x in range(numCards):
        card = parseInput(input("Enter a card: "))
        while any(i == card for i in cards):
            card = parseInput(input("Card is already in play. Please try again: "))
        cards.append(card)
    return cards

def parseInput(card):
    number = card[0]
    suit = card[1]
    num = 0
    mult = 0
    match suit: # suits are Clubs, Spades, Hearts, or Diamonds
        case 'c':
            mult = 0
        case 's':
            mult = 1
        case 'h':
            mult = 2
        case 'd':
            mult = 3
        case other:
            parseInput(input("Invalid entry. Please try again: "))
    try:
        num = int(number)-1
    except:
        match number:
            case 'a':
                num = 0
            case 'j':
                num = 10
            case 'q':
                num = 11
            case 'k':
                num = 12
            case other:
                parseInput(input("Invalid entry. Please try again: "))
                
    return mult * 13 + num

def toRank(cards):
    rank = []
    for i in range(len(cards)):
        rank.append(cards[i]%13)
    return rank

def toSuit(cards):
    suit = []
    for i in range(len(cards)):
        suit.append(int(cards[i]/13))
    return suit

def parseStatus(statuses, status):
    print(statuses, status)
    if status>=64:
        statuses[6] = True # four of a kind
        status = status-64
        parseStatus(statuses, status)
    elif status>=16:
        statuses[4] = True # flush
        status = status-16
        parseStatus(statuses, status)
    elif status>=8:
        statuses[3] = True # straight
        status = status-8
        if statuses[4]:
            statuses[7] = True # straight flush
        parseStatus(statuses, status)
    elif status>=4:
        statuses[2] = True # three of a kind
        status = status-4
        parseStatus(statuses, status)
    elif status>=2:
        statuses[1] = True # two pair
        status = status-2
        parseStatus(statuses, status)
    elif status>=1:
        statuses[0] = True # pair
        status = status-1
        if statuses[2] and statuses[1]:
            statuses[5] = True # full house
        parseStatus(statuses, status)
    else:
        print('Status: ', statuses)
        return checkHighest(statuses)
    
def checkHighest(statuses):
    print(statuses)
    highest = 0
    for i in range(len(statuses)):
        if statuses[i]:
            highest = i
    print(highest)
    return highest

def handRank(hand):
    probabilities = [] # this should return a list of the number of hands that are automatically lower than the current hand
    """^ example, there are no hands higher than a straight flush so the 7th index would read (max number of hands). 
    There are 40 ways to make a straight flush so the 6th index would read (max number of hands) - 40.

    From here we need to determine how many hands rank exactly the same as the current hand. Ex. a straight flush is unique except for the suit.
    There are therefore 3 effectively identical hands (these other 3 are impossible to have in play at the same time, but
    I'll address that at a later date)
    """
    return None

"""
High card: 0
Pair: 1
Two Pair: 2
Three of a Kind: 4
Straigh: 8
Flush: 16
Full House: 32
Four of a Kind: 64
Straight Flush: 128
"""
def initStatus():
    statuses = []
    for x in range(8):
        statuses.append(False)
    return statuses

def checkStatus(cards, status):
    #check pair
    flag = False
    rank = toRank(cards)
    for c1 in range(len(rank)):
        if status<2:
            for c2 in range(c1+1,len(rank)):
                if rank[c1]==rank[c2]:
                    #single pair exists
                    status = status + 1
                    if flag:
                        # two pair exists
                        status = status + 2
                        print(2,[c1,c2])
                        break
                    print(1,[c1,c2])
                    for c3 in range(c2+1,len(rank)):
                        if rank[c3]==rank[c1]:
                            #three of a kind exists
                            status = status + 4
                            print(4,[c1,c2,c3])
                            for c4 in range(c3+1,len(rank)):
                                if rank[c4]==rank[c1]:
                                    #four of a kind exists
                                    status = status + 64
                                    print(64,[c1,c2,c3,c4])
                                    break
                            break
                    flag = True
                    break

    rank = sorting.bubble(rank)
    consecCount = 0
    print(rank)
    for r in range(len(rank)-1):
        if rank[r+1]-rank[r]==1:
            consecCount = consecCount + 1
            print(consecCount)
            if consecCount>=4:
                break
        else:
            consecCount = 0
    if consecCount>=4:
        # straight exists
        status = status + 8
        print(8)
    #need to sort the rank and check if there is ever 5 cards in a row that increment by 1 (determines striaght)

    suit = toSuit(cards)
    suitCount = [0,0,0,0]
    for card in suit:
        suitCount[card] = suitCount[card] + 1
    for card in suitCount:
        if card>4:
            #flush exists
            status = status + 16
            print(16)

    return status

cards = []
status = 0

numCards = 5 #number of cards in the draw

cards = promptInput(numCards)
status = checkStatus(cards, status)
print(status)
statuses = initStatus()
print(parseStatus(statuses, status))