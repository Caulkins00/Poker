import math
from itertools import combinations

status = [False]*52

def parseInput(card):
    suit = card[-1]
    card = card[:-1]
    number = card
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
    if status[mult*13+num]:
        print("Error!")
    status[mult*13+num]=True
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

def higherThan(cards1, cards2):
    hand1 = getPlayableHand(cards1)
    hand2 = getPlayableHand(cards2)
    if hand1[0]>hand2[0]:
        return 1
    elif hand1[0]<hand2[0]:
        return 0
    else:
        counts1 = [0]*13
        counts2 = [0]*13
        rank1 = sorted(toRank(hand1[1]))
        rank2 = sorted(toRank(hand2[1]))
        for r in rank1:
            counts1[r] += 1
        for r in rank2:
            counts2[r] += 1
        counts1.append(counts1.pop(0))
        counts2.append(counts2.pop(0))
        max1 = 0
        second1 = 0
        max2 = 0
        second2 = 0
        for i in reversed(range(13)):
            if counts1[i]>counts1[max1]:
                second1 = max1
                max1 = i
            if counts2[i]>counts2[max2]:
                second2 = max2
                max2 = i
        if max1>max2:
            return 1
        elif max2>max1:
            return 0
        elif second1>second2:
            return 1
        elif second2>second1:
            return 0
    return -1

def getPossibleHands(cards):
    remaining = []
    for i in range(len(status)):
        if not status[i]:
            remaining.append(i)
    combos = list(combinations(remaining,7-len(cards)))
    possible = [0]*len(combos)
    for i in range(len(combos)):
        possible[i] = cards + list(combos[i])
    return possible

def getPlayableHand(cards):
    if len(cards)>=5:
        combos = list(combinations(cards, 5))
        max = 0
        maxHand = []
        playableHand = combos[0]
        for c in combos:
            hand = calcHand(c)
            if hand>max:
                max = hand
                maxHand = c
                playableHand = c
            if hand==max and rankHand(hand, c, maxHand):
                playableHand = c
    return max, playableHand

def rankHand(hand, cards, cards2):
    cards = sorted(toRank(cards))
    cards2 = sorted(toRank(cards2))
    if hand==8 or hand==4 or hand==0 or hand==5:
        high = cards[-1]
        high2 = cards[-1]
        if high>high2:
            return 1
        elif high<high2:
            return 0
        else:
            return -1
    counts1 = [0]*13
    counts2 = [0]*13
    for c in cards:
        counts1[c] +=1
    for c in cards2:
        counts2[c] +=1
    index1 = 1
    index2 = 1
    nextIndex1 = 1
    nextIndex2 = 1
    if hand==7:
        for i in range(len(counts1)):
            if counts1[i]==4:
                index1 = i
            if counts2[i]==4:
                index2 = i
        if index1==0:
            index1 = 13
        if index2==0:
            index2 = 13
        if index1>index2:
            return 1
        elif index1<index2:
            return 0
        else:
            high1 = cards[-1]
            high2 = cards[-1]
            if high1>high2:
                return 1
            if high2<high2:
                return 0
            else:
                return -1
    if hand==6:
        for i in range(len(counts1)):
            if counts1[i]==3:
                index1 = i
            if counts2[i]==3:
                index2 = i
            if counts1[i]==2:
                nextIndex1 = i
            if counts2[i]==2:
                nextIndex2 = i
            if index1==0:
                index1 = 13
            if index2==0:
                index2 = 13
            if nextIndex1==0:
                nextIndex1 = 13
            if nextIndex2==0:
                nextIndex2 = 13
            if index1>index2:
                return 1
            elif index1<index2:
                return 0
            else:
                if nextIndex1<nextIndex2:
                    return 1
                elif nextIndex1<nextIndex2:
                    return 0
                else:
                    return -1
    if hand==3:
        for i in range(len(counts1)):
            if counts1[i]==3:
                index1 = i
            if counts2[i]==3:
                index2 = i
        if index1==0:
            index1 = 13
        if index2==0:
            index2 = 13
        if index1>index2:
            return 1
        elif index1<index2:
            return 0
        else:
            high1 = cards[-1]
            high2 = cards2[-1]
            if high1>high2:
                return 1
            elif high1<high2:
                return 0
            else:
                return -1
    if hand==2 or hand==1:
        for i in range(len(counts1)):
            if counts1[i]==2:
                nextIndex1 = index1
                index1 = i
            if counts2[i]==2:
                nextIndex2 = index2
                index2 = i
            if index1==0:
                index1 = 13
            if index2==0:
                index2 = 13
            if nextIndex1==0:
                nextIndex1 = 13
            if nextIndex2==0:
                nextIndex2 = 13
            if index1>index2:
                return 1
            elif index1<index2:
                return 0
            else:
                if nextIndex1>nextIndex2:
                    return 1
                elif nextIndex1<nextIndex2:
                    return 0
                else:
                    return -1

def calcHand(cards):
    if isRoyalFlush(cards):
        return 9
    if isStraightFlush(cards):
        return 8
    if isFourOfKind(cards):
        return 7
    if isFullHouse(cards):
        return 6
    if isFlush(cards):
        return 5
    if isStraight(cards):
        return 4
    if isThreeOfKind(cards):
        return 3
    if isTwoPair(cards):
        return 2
    if isPair(cards):
        return 1
    else:
        return 0

def isRoyalFlush(cards):
    rank = sorted(toRank(cards))
    if isStraightFlush(cards) and rank[0]==0:
        return True
    else:
        return False

def isStraightFlush(cards):
    if isStraight(cards) and isFlush(cards):
        return True
    else:
        return False

def isFourOfKind(cards):
    counts = [0]*13
    flag = False
    rank = toRank(cards)
    for i in range(len(rank)):
        for j in range(i):
            if rank[i]==rank[j]:
                counts[rank[i]]=counts[rank[i]]+1
    for count in counts:
        if count>3:
            return True
    return False

def isFullHouse(cards):
    if isThreeOfKind(cards) and isTwoPair(cards):
        return True
    else:
        return False

def isFlush(cards):
    suit = toSuit(cards)
    if all(ele==suit[0] for ele in suit):
        return True
    else:
        return False

def isStraight(cards):
    rank = sorted(toRank(cards))
    for i in range(len(rank)-1):
        if not (rank[i+1]-rank[i]==1):
            if rank[i]==0 and rank[i+1]==9:
                continue
            else:
                return False
    return True

def isThreeOfKind(cards):
    counts = [0]*13
    flag = False
    rank = toRank(cards)
    for i in range(len(rank)):
        for j in range(i):
            if rank[i]==rank[j]:
                counts[rank[i]]=counts[rank[i]]+1
    for count in counts:
        if count>=2:
            return True
    return False
    
def isTwoPair(cards):
    counts = [0]*13
    flag = False
    rank = toRank(cards)
    for i in range(len(rank)):
        for j in range(i):
            if rank[i]==rank[j]:
                counts[rank[i]]=counts[rank[i]]+1
    for count in counts:
        if count>=1:
            if flag:
                return True
            flag = True
    return False

def isPair(cards):
    rank = toRank(cards)
    for i in range(len(rank)):
        for j in range(i):
            if rank[i]==rank[j]:
                return True
    return False

dealtCards = ["2d","3h","4s","5c","6h"]
myCards = ["7s","9d"]
for i in range(len(myCards)):
    myCards[i] = parseInput(myCards[i])
for i in range(len(dealtCards)):
    dealtCards[i] = parseInput(dealtCards[i])
myPlayableHand = dealtCards + myCards
possibleOpponentHands = getPossibleHands(dealtCards)
winCount = 0
drawCount = 0
for hand in possibleOpponentHands:
    match = higherThan(myPlayableHand, hand)
    if match==-1:
        print(match, hand)
    elif match==0:
        print(match, hand)
    if match==1:
        winCount = winCount+1
    elif match==-1:
        drawCount = drawCount + 1

winProb = winCount/len(possibleOpponentHands)
drawProb = drawCount/len(possibleOpponentHands)
print("Win Probabilitiy: ",winProb)
print("Draw Probability: ", drawProb)