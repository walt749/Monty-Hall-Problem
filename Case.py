
import array as arr
import random as ran

class Case:
    _number = 0
    _value = 0.0
    _opened = None

    def __init__(self, number, value):
        self._number = number
        self._value = value
        self._opened = False

    def getNumber(self):
        return self._number

    def getValue(self):
        return self._value

    def getOpened(self):
        return self._opened

    def setOpened(self,opened):
        self._opened = opened

    def __str__(self):
        return "Case: "+str(self._number) +" Value: $" +str(self._value)



class DealOrNoDealGame:
    _gameNo = 0
    _ACTUAL_GAME_VALUES = arr.array('d',[0.01, 1.00,5.00,10.00,25.00,50.00,75.00,
                                         100.00,200.00,300.00,400.00,500.00,
                                         750.00, 1000.00, 5000.00, 10000.00, 25000.00, 50000.00,
                                         75000.00, 100000.00, 200000.00, 300000.00, 400000.00, 500000.00,
                                         750000.00, 1000000.00])

    _VALUES = arr.array('d',[0.01, 0.01,	0.01, 0.01, 0.01, 0.01,
                             0.01, 0.01,	0.01, 0.01,	0.01, 0.01,
                             0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
                             0.01, 0.01, 0.01, 0.01, 0.01, 0.01,0.01, 1000000.00])

    TOP_PRIZE = _VALUES[len(_VALUES)-1]

    DEFAULT_GAME_COUNT = 500

    _cases = [] #(Case, [])

    _playerChoice = Case
    _unopenedCase = Case

    def __init__(self):
        self.setUp()

    def setUp(self):
     for x in range(len(self._VALUES)):
        self._cases.append(Case(x+1,self._VALUES[x]))
        #print(self._cases[0].getValue())
     ran.shuffle(self._cases)

    def keep(self):
        return

    def trade(self):
     self._playerChoice = self._unopenedCase

    def pick(self, gameno):
        self._gameNo = gameno

        #print(len(self._VALUES))
        pick = ran.randint(1, len(self._VALUES))
        self._playerChoice = self._cases[pick - 1]

        for x in self._cases:

            if x.getValue() != self.TOP_PRIZE:
                x.setOpened(True)

            elif x.getValue() == self.TOP_PRIZE:
                self._unopenedCase = x

        if self._playerChoice.getValue() == self.TOP_PRIZE:
            a = self._cases[len(self._VALUES)-1]
            a.setOpened(False)
            self._unopenedCase = a

    def getPlayerChoice(self):
        return self._playerChoice

    def getUnopenedCase(self):
        return self._unopenedCase

    def __str__(self):
        return "Game: " +str(self._gameNo) +" [Player's Choice: " +str(self._playerChoice) +", Unopened Case: " +str(self._unopenedCase) +"]"

class Game:
    won = False
    Switched = False
    selectedCase = Case

    def __init__(self, case, switched, won):

        self.selectedCase = case
        self.Switched = switched
        self.won = won

    def getSwitched(self):
        return self.getSwitched()

    def getWon(self):
        return self.getWon()


class DealOrNoDealer:

    game = DealOrNoDealGame()
    DEFAULT_GAME_COUNT = 500
    _PRINT_LIMIT = 10
    _winCount = 0
    _gameCount = 0
    _History = (Game,[])

    def __init__(self, gamecount):
        self._gameCount = gamecount
       # print("gamecount" +str(gamecount))
        self.game = DealOrNoDealGame()
        self._History = (Game,[])

    def SaveToHistory(self):
        switched = self.game.getUnopenedCase() == self.game.getPlayerChoice()
        won = self.game.getPlayerChoice() == DealOrNoDealGame.TOP_PRIZE
        self._History = (*self._History, (Game(self.game.getPlayerChoice(), switched, won)))



    def reset(self):
        self._History = []
        self._winCount = 0

    def DisplaySummary(self):
        totalGames = int(len(self._History))
        gamesWon = 0
        gamesWonWhenSwitched = 0;
        gamesSwitched = 0;
        gamesWonWhenKept = 0;

        for g in self._History:
            if g.getWon():
               gamesWon = gamesWon + 1
               if g.getSwitched():
                gamesWonWhenSwitched = gamesWonWhenSwitched + 1

            if not g.getSwitched():
                 if g.getWon:
                     gamesWonWhenKept = gamesWonWhenKept + 1

            else: gamesSwitched = gamesSwitched + 1

        gamesLost = totalGames - gamesWon
        gamesKept = totalGames - gamesSwitched

        print("total " +str(totalGames))
        percentWonWhenKept = gamesWonWhenKept #/ gamesKept * 100
        percentWonWhenSwtiched = gamesWonWhenSwitched #/  gamesSwitched * 100
       # print("Player won "+str(gamesWonWhenKept) +" of %" +str(self._gameCount) +" ("+str(percentWonWhenKept) +"%) when case was kept.")
       # print("Player won " +str(gamesWonWhenSwitched) +" of %" +str(self._gameCount) +" (" +str(percentWonWhenSwtiched) +"%) when case was kept")


    def SimulateGames(self, tradeCase):

        #print("leng" +str((self._gameCount)))
        for a in range(int(self._gameCount)):


            self.game.pick(a+1)

            if tradeCase:
                self.game.trade()
            if not tradeCase:
                self.game.keep()

            self.SaveToHistory()
            if a < self._PRINT_LIMIT:
                print(self.game)

            self.reset()


    def Play(self):

     print("===========================================================================")
     print("GAMES WHERE THE PLAYER KEPT THE CASE ORIGINALLY SELECTED")
     self.SimulateGames(False)

     print("---------------------------------------------------------------------------")
     print("GAMES WHERE THE PLAYER TRADED THE CASE ORIGINALLY SELECTED")
     self.SimulateGames(True)

     print("---------------------------------------------------------------------------")
     self.DisplaySummary()
     print("============================================================================")

     self.reset()



games = input("How many games would you like to simulate for each keep/trade decision? ")
dealer = DealOrNoDealer(games)

dealer.Play()

