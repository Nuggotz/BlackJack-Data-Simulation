
import random
import time

class Strategy():

    h = "H" #Hit
    s = "S" #Stand

    def __init__(self):
        
        self.hitPrize = 0
        self.standPrize = 0
        self.doublePrize = 0
        self.splitPrize = 0

        self.numHit = 0
        self.numStand = 0
        self.numDouble = 0
        self.numSplit = 0

        self.end = False
        
    def getEnd(self):
        return self.end
    
    def changeEnd(self):
        self.end = False

    def endTurn(self):
        self.end = True

    def getStats(self):
        print(f"Hit: {self.numHit} Stand: {self.numStand} Double: {self.numDouble} Split: {self.numSplit} TotalHands: {self.hitPrize + self.standPrize + self.doublePrize + self.splitPrize}")
        print(f"HitPrize: {self.hitPrize} StandPrize: {self.standPrize} DoublePrize: {self.doublePrize} SplitPrize: {self.splitPrize} TotalPrize: {self.hitPrize + self.standPrize + self.doublePrize + self.splitPrize}")      


    def updateNum(self, type):
        if type == self.h:
            self.numHit += 1
        elif type == self.s:
            self.numStand += 1
        elif type == self.d:
            self.numDouble += 1
        elif type == self.p:
            self.numSplit += 1

    def win(self, type, mult):
        if self.end:
            if type == self.h:
                self.hitPrize -= 100
            elif type == self.s:
                self.standPrize -= 100
            elif type == self.d:
                self.doublePrize -= 200
            elif type == self.p:
                self.splitPrize -= 100

            if mult > 0:
                if type == self.h:
                    self.hitPrize += 100 * mult
                elif type == self.s:
                    self.standPrize += 100 * mult
                elif type == self.d:
                    self.doublePrize += 200 * mult
                elif type == self.p:
                    self.splitPrize += 100 * mult 

class Conservative(Strategy):

    def __init__(self):
        super().__init__()
    
    def turn(self, hand, obj):
        turn = -1
        while not self.getEnd():
            turn += 1
            if obj.handScore(hand) < 12:
                obj.hit(hand)
            elif turn == 0:
                self.updateNum(self.s)
                self.end = True
                obj.dealerTurn()
                return self.s
            else:
                self.end = True
                obj.dealerTurn()
                self.updateNum(self.h)
                return self.h
        
class Seventeen(Strategy):
    
    def __init__(self):
        super().__init__()
    
    def turn(self, hand, obj):
        turn = -1
        while not self.getEnd():
            turn += 1
            if obj.handScore(hand) < 17  and obj.handScore(hand) > 0:
                obj.hit(hand)
            elif turn == 0:
                self.updateNum(self.s)
                self.end = True
                obj.dealerTurn()
                return self.s
            else:
                self.end = True
                obj.dealerTurn()
                self.updateNum(self.h)
                return self.h
            
class Hard(Strategy):

    h = "H" #hit
    s = "S" #stand
    d = "D" #double
    p = "P" #split
    dH = "Dh" #Double, else hit

    hardTable = [
#Dealer  2   3   4   5   6   7   8   9   10  A   Player:
        [h,  h,  h,  h,  h,  h,  h,  h,  h,  h], #4-8
        [h,  dH, dH, dH, dH, h,  h,  h,  h,  h], #9
        [dH, dH, dH, dH, dH, dH, dH, dH, h,  h], #10
        [dH, dH, dH, dH, dH, dH, dH, dH, dH, h], #11
        [h,  h,  s,  s,  s,  h,  h,  h,  h,  h], #12
        [s,  s,  s,  s,  s,  h,  h,  h,  h,  h], #13
        [s,  s,  s,  s,  s,  h,  h,  h,  h,  h], #14
        [s,  s,  s,  s,  s,  h,  h,  h,  h,  h], #15
        [s,  s,  s,  s,  s,  h,  h,  h,  h,  h], #16
        [s,  s,  s,  s,  s,  s,  s,  s,  s,  s]  #17+
    ]

    splitTable = [
#Dealer  2  3  4  5  6  7  8  9  10 A  Player:
        [p, p, p, p, p, p, h, h, h, h], #2
        [p, p, p, p, p, p, h, h, h, h], #3
        [h, h, h, p, p, h, h, h, h, h], #4
        [p, p, p, p, p, h, h, h, h, h], #5
        [p, p, p, p, p, p, h, h, h, h], #6
        [p, p, p, p, p, p, p, p, p, p], #7
        [p, p, p, p, p, s, p, p, s, s], #8
        [p, p, p, p, p, p, p, p, p, p], #9
        [s, s, s, s, s, s, s, s, s, s], #10
        [p, p, p, p, p, p, p, p, p, p]  #A
    ]

   
    def __init__(self):
        super().__init__()

    def turn(self, hand, obj, dealer, index):
        turn = -1
        outcome = ''
        while not self.getEnd():
            turn += 1
            value = self.handScore(hand)
            if hand[0] == hand[1] and len(obj.getHands()) < 4 and hand[0] != 10 and value > 0:
                if hand[0] == 'A':
                    hand[0] = 11
                outcome = self.splitTurn(hand, obj, dealer, index)     
                hand[0] == 'A'
            elif value < 8 and value > 0:
                obj.hit(hand)
            elif value >= 17 or value == 0:
                self.end = True
            elif value > 0:
                outcome = self.hardTurn(hand, obj, dealer, value - 8 )

        obj.dealerTurn()

        if turn == 0 and outcome == self.s:
            self.updateNum(self.s)
            return self.s
        elif outcome == self.d:
            self.updateNum(self.d)
            return self.d 
        elif outcome == self.p:
            self.updateNum(self.p)
            return (self.p)
        else:
            self.updateNum(self.h)
            return self.h

    def splitTurn(self, hand, obj, dealer, index):
        if Hard.splitTable[hand[0]-2][dealer-2] == Hard.p:
            obj.split(index)
            return self.p
        elif Hard.splitTable[hand[0]-2][dealer-2] == Hard.h:
            obj.hit(hand)
            return self.h
        else:
            self.end = True
            return self.s
                    
    def hardTurn(self, hand, obj, dealer, value):
        if (Hard.hardTable[value][dealer-2]) == Hard.dH and len(hand) == 2:
            self.endTurn()
            self.updateNum(self.d)
            obj.hit(hand)
            return self.d
        elif (Hard.hardTable[value][dealer-2]) == Hard.h:
            obj.hit(hand)
            return self.h
        else:
            self.endTurn()
            return self.s

    def handScore(self, hand):
        sum = 0
        for card in hand:
            if type(card) == int:
                sum += card
            elif hand[1] == 10 and len(hand) == 2:
                sum = 21
            else:
                sum += 1
        if sum > 21:
            sum = 0
        return sum

class Soft(Hard):
    
    h = "H" #Hit
    s = "S" #Stand
    dH = "Dh" #Double, else hit
    dS = "Ds" #Double, else stand

    softTable = [
#Dealer  2  3   4   5   6   7  8  9  10 A  Player:
        [h, h,  h,  dH, dH, h, h, h, h, h], #13
        [h, h,  h,  dH, dH, h, h, h, h, h], #14
        [h, h,  dH, dH, dH, h, h, h, h, h], #15
        [h, h,  dH, dH, dH, h, h, h, h, h], #16
        [h, dH, dH, dH, dH, h, h, h, h, h], #17
        [s, dS, dS, dS, dS, s, s, h, h, h], #18
        [s, s,  s,  s,  s,  s, s, s, s, s]  #19+
    ]

    def __init__(self):
        super().__init__()

    def turn(self, hand, obj, dealer, index):
        turn = -1
        outcome = ''
        while not self.getEnd():
            turn += 1
            value = obj.handScore(hand)
            if value >= 19 or value < 0:
                self.end = True
                outcome = self.s
            elif not ((hand[0] == 'A' and hand[1] == 'A')):
                Hard.turn(self, hand, obj, dealer, index)
            else:
                outcome = self.softTurn(hand, obj, dealer, value - 13)

        if turn == 0 and outcome == self.s:
            self.updateNum(self.s)
            return self.s 
        elif outcome == self.d:
            self.updateNum(self.d)
            return self.h
        else:
            self.updateNum(self.h)
            return self.h

    def softTurn(self, hand, obj, dealer, value):
        if (self.softTable[value][dealer-2] == self.dH or self.softTable[value][dealer-2] == self.dS) and len(hand) == 2:
            self.end = True
            obj.hit(hand)
            return self.d
        elif self.softTable[value][dealer-2] == self.h or self.softTable[value][dealer-2] == self.dH == self.dH:
            obj.hit(hand)
            return self.h
        else:
            self.end = True
            return self.s
            

class BlackJack(Conservative, Seventeen, Soft, Hard):    

    def __init__(self, deck): 
        super().__init__()

        self.player = [[]]
        self.dealer = []
        self.deck = list(deck)

        for i in range(4):
            if i % 2 == 0:
                self.player[0].append(self.deck[0])
            else:
                self.dealer.append(self.deck[0])
            del self.deck[0]
    
    def getHand(self, index):
        return self.player[index]
    
    def getHands(self):
        return self.player

    def getDealer(self):
        return self.dealer[0]

    def showHand(self):
        print(f"Player hand: {self.player}, Dealer hand: {self.dealer}")

    def handScore(self, hand):
        sum = 0
        for card in hand:
            if type(card) == int:
                sum += card
            else:
                if sum + 11 > 21:
                    sum += 1
                else:
                    sum += 11
        if sum > 21:
            return 0
        return sum
    
    def hit(self, hand):
        hand.append(self.deck[0])
        del self.deck[0]
    
    def split(self, index):
        self.player.append([])
        self.player[len(self.player)-1].append(self.player[index][1])
        del self.player[index][1]
        self.hit(self.player[index])
        self.hit(self.player[len(self.player)-1] )

    def dealerTurn(self):
        while self.handScore(self.dealer) < 17 and self.handScore(self.dealer) > 0:
            self.dealer.append(self.deck[0])
            del self.deck[0]

    def outcome(self, hand):
        if self.handScore(hand) == 21 and len(hand) == 2 and self.handScore(self.dealer) != 21:
            return 2.5
        elif self.handScore(hand) > self.handScore(self.dealer):
            return 2
        elif self.handScore(hand) == self.handScore(self.dealer):
            return 1
        return 0

cStrat = Conservative()
tStrat = Seventeen()
hStrat = Hard()
sStrat = Soft()

start_time = time.time()
for _ in range(100000):
    deck = [ 2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A'
            ,2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A'
            ,2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A'
            ,2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A'
            ,2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A'
            ,2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A'
            ,2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A'
            ,2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',2,3,4,5,6,7,8,9,10,10,10,10,'A',]
    random.shuffle(deck)
    del deck[0]

    cHand = BlackJack(deck)
    tHand = BlackJack(deck)
    hHand = BlackJack(deck)
    sHand = BlackJack(deck)

    cStrat.win(cStrat.turn(cHand.getHand(0), cHand), cHand.outcome(cHand.getHand(0)))
    cStrat.changeEnd()

    tStrat.win(tStrat.turn(tHand.getHand(0), tHand), tHand.outcome(tHand.getHand(0)))
    tStrat.changeEnd()

    for i in range(len(hHand.getHands())):
        hStrat.win(hStrat.turn(hHand.getHand(i), hHand, 11 if hHand.getDealer() == 'A' else hHand.getDealer(), i), hHand.outcome(hHand.getHand(i)))
    hStrat.changeEnd()

    for i in range(len(sHand.getHands())):
        sStrat.win(sStrat.turn(sHand.getHand(i), sHand, 11 if sHand.getDealer() == 'A' else sHand.getDealer(), i), sHand.outcome(sHand.getHand(i)))
    sStrat.changeEnd()

end_time = time.time()
total_time = end_time - start_time
print(f"Runtime: {int(total_time / 3600)}:{int((total_time % 3600) / 60)}.{total_time % 60}")
cStrat.getStats()
tStrat.getStats()
hStrat.getStats()
sStrat.getStats()