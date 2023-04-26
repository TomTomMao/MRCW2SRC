from typing import Union
from datetime import datetime
from datetime import timedelta
import random
from energyCore import Energycore
from treasure import Treasure, VALID_TREASURE_TYPE
from quiz import Quiz
import json


def checkDigit(string: str):
    if len(string) == 0:
        return False
    for char in string:
        if char not in [str(i) for i in range(10)]:
            return False
    else:
        return True


def readQuiz(path="./quiz.csv"):
    """
        Return a list of dictionary like this: {"id":"1", "answer": "B", "mode": "shed"}
    """
    # reference for relative path https://stackoverflow.com/questions/40416072/reading-a-file-using-a-relative-path-in-a-python-project
    import csv
    from pathlib import Path
    basePath = Path(__file__).parent
    filePath = filePath = (basePath / path).resolve()
    print(filePath)
    data = []
    with open(filePath) as quizConfigFile:
        csvreader = csv.reader(quizConfigFile, delimiter='\t')
        for row in csvreader:
            data.append(row)
    config = [{data[0][0]: entry[0], data[0][1]: entry[1],
               data[0][2]: entry[2]} for entry in data[1:]]
    return config


HINTS_TEMPLATE = """
    <html>
        <head>
            <title>
            guideline for the human
            </title>
        </head>
        <body>
            <h1>Welcome to the game</h1>
            <p>Here is the instruction for the human</p>
        </body>
    </html>
"""
SNOW_MONSTER_INSTRUCTION_TEMPLATE = """
    <html>
        <head>
            <title>
            guideline for the snow monster
            </title>
        </head>
        <body>
            <h1>Welcome to the game</h1>
            <p>Here is the instruction for the monsters</p>
        </body>
    </html>
"""
SUCCESS_EXPAND_TIME_TEMPLATE = """
    <html>
        <head>
            <title>
            Time Expanded
            </title>
        </head>
        <body>
            <h1>Time Expanded</h1>
            <p>Time has been expanded for {timeExpand}</p>
            <p>The remaining time limit is: {timeLimit}</p>
        </body>
    </html>
"""
VALID_DIFFICULTY = ("easy", "mid", "hard")
VALID_FIXING_MODE = ("shed", "nonshed", "inactive")
VALID_ATTACK_STATE = ("attacked", "notAttacked")
VALID_WEATHER = ("rain", "notRain")


# GAME CONFIGURE
try:
    QUIZ_CONFIG = readQuiz("./quiz.csv")
except Exception as e:
    print(str(e))
    print("error: fail to read quiz file")
BOMB_TIME_INSECOND: int = 30
ENERGYCORE_COUNT = 7
ENERGYCORE_CONFIG = [{'id': str(i)} for i in range(1, ENERGYCORE_COUNT)]
GAME_CONFIG = {
    'easy': {
        'timeExpanderEffectInSeconds': 15,
        'quizCount': 20,
        'attackTime': 15,
        # for random.choices()
        'treasure': {'types': ['shield', 'timeExpander', 'fixer'], 'weights': [6, 2, 2], 'count': 20},
        'timeLimit': timedelta(minutes=10),
        'attackChanceCount': 15
    }, 'mid': {
        'timeExpanderEffectInSeconds': 10,
        'quizCount': 20,
        'attackTime': 20,
        # for random.choices()
        'treasure': {'types': ['shield', 'timeExpander',
                               'fixer'], 'weights': [7, 3, 1], 'count': 20},
        'timeLimit': timedelta(minutes=7.5),
        'attackChanceCount': 20
    }, 'hard': {
        'timeExpanderEffectInSeconds': 5,
        'quizCount': 20,
        'attackTime': 30,
        # for random.choices()
        'treasure': {'types': ['shield', 'timeExpander', 'fixer', 'timeExpanderBomb'], 'weights': [6, 2, 1, 1], 'count': 20},
        'timeLimit': timedelta(minutes=0.5),
        'attackChanceCount': 50
    }
}

class Game:
    def __init__(self) -> None:
        self.treasures: list[Treasure]
        self.quizzes: list[Quiz]
        self.energycores: list[Energycore]
        self.isGameStarted: bool = False
        self.startTime: datetime
        self.endTime: datetime
        self.timeLimit: int  # seconds
        self.shieldCount: int
        self.fixingMode: str
        self.gameDifficulty: str
        self.attackChanceCount: int
        self.connectedCore: Union[Energycore, None]
        self.attackState: str
        pass

    def initialise(self, difficulty: str):
        """
            Assume difficulty is in VALID_DIFFICULTY
            Initialize the game:
                Initialize the difficulty
                Initialize treasures list, there will be a list of treasures
                            quizzes list, there will be a list of quizzes
                            energycores list, there will be a list of energycores
                Initialize the startTime, endTime, and the timeLimit
                Initialize the shieldCount, fixingMode, attackChanceCount, connectedCore
                Set isGameStarted to be True
        """

        assert difficulty in VALID_DIFFICULTY, f"invalid difficulty: {difficulty}, it should be on of {VALID_DIFFICULTY}"

        # initialise the difficulty
        self.gameDifficulty = difficulty

        # initialise the treasure list
        treasureTypeList = [random.choices(
            GAME_CONFIG[self.gameDifficulty]['treasure']['types'], weights=GAME_CONFIG[self.gameDifficulty]['treasure']['weights'], k=GAME_CONFIG[self.gameDifficulty]['treasure']['count'])][0]
        self.treasures = [Treasure(id=str(index), treasureType=_treasureType)
                          for index, _treasureType in enumerate(treasureTypeList)]

        # initialise the quizzes list
        self.quizzes = [Quiz(id=quizConfig['id'], answer=quizConfig['answer'],
                             mode=quizConfig['mode']) for quizConfig in QUIZ_CONFIG]

        # initialise the energycores list
        self.energycores = [Energycore(id=energycoreConfig['id'])
                            for energycoreConfig in ENERGYCORE_CONFIG]

        # initialize the startTime, endTime, and the timeLimit
        self.startTime:datetime = datetime.now()
        self.timeLimit:int = GAME_CONFIG[self.gameDifficulty]['timeLimit'].seconds
        self.endTime:datetime = self.startTime + timedelta(seconds=self.timeLimit)

        # Initialize the shieldCount, fixingMode, attackChanceCount, connectedCore, attackState
        self.shieldCount = 0
        self.fixingMode = "inactive"
        self.attackChanceCount = GAME_CONFIG[self.gameDifficulty]['attackChanceCount']
        self.connectedCore = None
        self.attackState = "notAttacked"

        # set game state
        self.isGameStarted = True

    def getTreasures(self) -> list[Treasure]:
        """
            Assume game is started.
            Return a list of treasure object.
        """
        assert self.isStart(), "game must be started"
        return self.treasures

    def getConnectedEnergycore(self) -> Union[Energycore, None]:
        """
            Assume game is started.
            Return the energy core that is connected to the fixing tool if exists
            Return None if there is no energy core connecting to the fixing tool
        """
        assert self.isStart(), "game must be started"
        if self.connectedCore == None:
            return None
        else:
            return self.connectedCore

    def getEnergycores(self) -> list[Energycore]:
        """
            Assume game is started
            Return a list of energycores of the game
        """
        assert self.isStart(), "game must be started"
        return self.energycores

    def getTreasureById(self, treasureId: str) -> Union[Treasure, None]:
        """
            Assume game is started.
            treasureId: should be a string only contain number
            Return False if there is no treasure whose id is treasureId.
            Return a treasure object whose id is the same as treasureId.
        """
        # check pre condition
        assert self.isStart(), "game must be started"
        if (checkDigit(treasureId) == False):
            raise ValueError('treasureId must only contain numbers "0" to "9"')

        for treasure in self.treasures:
            if treasure.getId() == treasureId:
                return treasure
        else:
            return None

    def getEnergycoreById(self, energycoreId) -> Union[Energycore, None]:
        """
            Assume game is started.
            energycoreId: should be a string only contain number
            Return an energy core object if exist. 
            Otherwise return None
        """
        assert self.isStart(), "game must be started"
        if (checkDigit(energycoreId) == False):
            raise ValueError(
                'energycoreId must only contain numbers "0" to "9"')

        for energycore in self.energycores:
            if energycore.getId() == energycoreId:
                return energycore
        else:
            return None

    def getQuizById(self, quizId: str) -> Union[Quiz, None]:
        """
            Assume game is started.
            quizId: should be a string only contain number
            Return a quiz Object whose id = quizId if there exists such a quiz.
            Otherwise, return None
        """
        assert self.isStart(), "game must be started"
        if (checkDigit(quizId) == False):
            raise ValueError('quizId must only contain numbers "0" to "9"')

        for quiz in self.quizzes:
            if quiz.getId() == quizId:
                return quiz
        else:
            return None

    def getFixingMode(self) -> Union[str, None]:
        """
            Assume game is started.
            Return "shed" if the human is answering the questions under the shed
            Return "nonshed" if the human is not answering the questions under the shed
            Return None if there is no connected energycore
        """
        assert self.isStart(), "game must be started"
        if self.fixingMode == "shed":
            return "shed"
        elif self.fixingMode == "nonshed":
            return "nonshed"
        else:
            return None

    def getAttackState(self) -> str:
        """
            Assume game is started.
            Return "attacked" if the snow monster has successfully attacked the human
            Otherwise return "notAttacked"
        """
        assert self.isStart(), "game must be started"
        assert self.attackState in VALID_ATTACK_STATE, "invalid attribute value of game object"
        return self.attackState

    def setAttackState(self, attackState: str) -> str:
        """
            Assume game is started.
            Assume the attackState in VALID_ATTACK_STATE
            Set the attack state to be attackState, if it is a valid state. and return True
            Return False otherwise.
        """
        assert self.isStart(), "game must be started"
        assert attackState in VALID_ATTACK_STATE, "invalid parameter value"
        self.attackState = attackState
        return self.attackState

    def getAttackChanceCount(self) -> int:
        """
            Assume the game is started
            Assume the attack chance count is non negative
            Return the number of attack chance for the snow monster
        """
        assert self.isStart(), "game must be started"
        assert self.attackChanceCount >= 0, "invalid attribute value of game object"
        return self.attackChanceCount

    def setAttackChanceCount(self, newAttackChanceCount: int) -> int:
        """
            Assume the game is started
            newAttackChanceCount: a non negative integer
            Set the attackchance
            Return the new value
        """
        assert self.isStart(), "game must be started"
        if newAttackChanceCount < 0:
            raise ValueError(
                'newAttackChanceCount must be an positive integer')
        else:
            self.attackChanceCount = newAttackChanceCount
            return self.attackChanceCount

    def getShieldCount(self) -> int:
        """
            Assume the game is started
            Assume the shield count is non negative
            Return the number of shield count
        """
        assert self.isStart(), "game must be started"
        assert self.shieldCount >= 0, "invalid attribute value of game object"
        return self.shieldCount

    def setShieldCount(self, newShieldCount: int) -> int:
        """
            Assume the game is started
            newShieldCount: non negative integer
            Set the shieldCount
            return the number of shield
        """
        assert self.isStart(), "game must be started"
        if newShieldCount < 0:
            raise ValueError("newShieldCount must be an positive integer")
        else:
            self.shieldCount = newShieldCount
            return self.shieldCount

    def setFixingMode(self, mode:str) :
        """
            mode: nonshed, shed, inactive. 
        """
        if mode not in VALID_FIXING_MODE:
            raise ValueError(f"Invalid mode: {mode}, it must in {VALID_FIXING_MODE}")
        else:
            self.fixingMode = mode

    def getInfoJSON(self) -> str:
        """
            Return a json used by dashboard.html
            If game starts, return a detailed data
            If game not starts, return a data showing that.
        """
        
        if self.isStart() == False:
            print(json.dumps({"isGameStarted": "False"}))
            return json.dumps({"isGameStarted": "False"})

        treasureObjects = self.getTreasures()
        treasuresDict = [treasure.toDictionary() for treasure in treasureObjects] #  a list of dictionary
        connectedCore: Union[Energycore, None] = self.getConnectedEnergycore()
        if connectedCore != None: 
            connectedCoreDict: Union[dict, None] = connectedCore.toDictionary()
        else:
            connectedCoreDict = None
        data = {
            "treasures": treasuresDict,
            "energycores": [energycore.toDictionary() for energycore in self.energycores],
            "quizzes": [quiz.toDictionary() for quiz in self.quizzes],
            "isGameStarted": self.isGameStarted,
            "startTime": self.startTime.strftime("%m/%d/%Y, %H:%M:%S"), # reference : https://www.programiz.com/python-programming/datetime/strftime
            "endTime": self.endTime.strftime("%m/%d/%Y, %H:%M:%S"),
            "remainingTime": self.getRemainingTimeLimit(),
            "shieldCount": self.getShieldCount(),
            "fixingMode": self.getFixingMode(),
            "gameDifficulty": self.gameDifficulty,
            "attackChanceCount": self.getAttackChanceCount(),
            "connectedCore": connectedCoreDict,
            "attackState": self.getAttackState()
            }
        # print(data)
        # print(json.dumps(data, indent = 4))
        return json.dumps(data, indent = 4)


    def getRemainingTimeLimit(self) -> int:
        """
            Assume the game is started
            return the number of seconds of the remaining time of the game
        """
        assert self.isStart(), "game must be started"

        if self.endTime >= datetime.now():
            delta: timedelta = self.endTime - datetime.now()
            return delta.seconds
        else:
            delta: timedelta = datetime.now() - self.endTime
            return -delta.seconds

    def reduceTime(self, timeToReduceInSecond: int = -1) -> int:
        """
            If timeToReduceInSecond = -1, use GAME_CONFIG[self.gameDifficulty]['attackTime']
            Assume the game is started
            timeToReduceInsecond: must be an positive integer
            Reduce the remaining time limit by timeToReduceInSecond
            Return the remaining time in seconds
        """
        assert self.isStart(), "game must be started"
        if timeToReduceInSecond == -1:
            timeToReduceInSecond = GAME_CONFIG[self.gameDifficulty]['attackTime']
        if timeToReduceInSecond <= 0:
            raise ValueError(
                "timeToReduceInSecond must be an postivie integer")
        self.timeLimit = self.timeLimit - timeToReduceInSecond
        self.endTime = self.endTime - timedelta(seconds=timeToReduceInSecond)
        return self.getRemainingTimeLimit()

    def expandTimeLimit(self, timeToExpandInSecond: int) -> int:
        """
            Assume the game is started
            timeToExpandInSecond: an positive integer
            Expand the time limit
            return the remaining time in seconds
        """
        assert self.isStart(), "game must be started"
        if timeToExpandInSecond <= 0:
            raise ValueError(
                "timeToExpandInSecond must be an postivie integer")
        # print("self.timeLimit: ", type(self.timeLimit))
        # print("timeToExpandInSecond: ", type(timeToExpandInSecond))
        self.timeLimit = self.timeLimit + timeToExpandInSecond
        self.endTime = self.endTime + timedelta(seconds=timeToExpandInSecond)
        return self.getRemainingTimeLimit()

    def reduceTimeLimit(self, timeToReduceInSecond: int) -> int:
        """
            Assume the game is started
            timeToReduceInSecond: an positive integer
            Reduce the time limit
            return the remaining time in seconds
        """
        assert self.isStart(), "game must be started"
        if timeToReduceInSecond <= 0:
            raise ValueError(
                "timeToReduceInSecond must be an postivie integer")
        self.timeLimit = self.timeLimit - timeToReduceInSecond
        self.endTime = self.endTime - timedelta(seconds=timeToReduceInSecond)
        return self.getRemainingTimeLimit()

    def connectEnergycore(self, energycore: Energycore) -> Energycore:
        """
            Assume the game is started
            energycore: the energycore to connect.
            connect the energy core to the fixer
        """
        assert self.isStart(), "game must be started"
        self.connectedCore = energycore
        return self.connectedCore

    def disconnectedEnergycore(self) -> bool:
        """
            Assume the game is started
            If there is an connected Energy core, disconnected it and return True
            If there is no enercy core that is connected to the fixing tool, return False
        """
        assert self.isStart(), "game must be started"
        if self.getConnectedEnergycore() != None:
            self.connectedCore = None
            return True
        else:
            return False

# keep working on this method.
    def isAvailableTreasure(self, treasure: Treasure) -> bool:
        """
            Assume the treasure object is part of self.
            Assume the treasure state is collected
            Assume the treusure is in VALID_TREASURE_TYPE
            If the game is suitable to apply the treasure, return True
            If the game is not suitable to apply the treasure, return False.
        """
        assert treasure in self.getTreasures(), "treasure must be part of the game"
        print(treasure.toDictionary())
        assert treasure.getState() == "collected", "treasure must be collected"
        assert treasure.getType() in VALID_TREASURE_TYPE, f"treasure has a wrong type:{treasure.getType()}"
        if treasure.getType() == "timeExpander":
            return True
        if treasure.getType() == "shield":
            return True
        if treasure.getType() == "fixer":
            # if there is unfixed energy core
            # return true
            # other wise false
            for energycore in self.energycores:
                if energycore.getState() == "unfixed":
                    return True
            return False
        if treasure.getType() == "timeExpanderBomb":
            return True
        else:
            raise AssertionError(f"treasure type is invalid:{treasure.getType()}")

    def isStart(self) -> bool:
        """
            If the game is started, return True
            If the game is not started, return False
        """
        return self.isGameStarted

    def isEnded(self) -> bool:
        """
            If the game is ended, return True
            If the game is not ended, return False
        """
        return self.getRemainingTimeLimit() <= 0

    def applyTreasure(self, treasure: Treasure) -> bool:
        """
            Assume the treasure can be applied
            Assume the treusure is in VALID_TREASURE_TYPE
            Apply the treasure effect. The state of treasure won't be changed in this method.
            Return True if success to apply
        """
        assert self.isAvailableTreasure(
            treasure), "treasure should be suitable to be applied"
        assert treasure.getType() in VALID_TREASURE_TYPE, f"treasure has a wrong type:{treasure.getType()}"
        if treasure.getType() == "timeExpander":
            timeToExpandInSeconds = GAME_CONFIG[self.gameDifficulty]['timeExpanderEffectInSeconds']
            self.expandTimeLimit(timeToExpandInSeconds)
            return True
        elif treasure.getType() == "shield":
            self.setShieldCount(self.getShieldCount()+1)
            return True
        elif treasure.getType() == "fixer":
            connectedEnergycore: Union[None, Energycore] = self.getConnectedEnergycore()
            if connectedEnergycore == None:
                for energycore in self.getEnergycores():
                    if energycore.getState() == "unfixed":
                        energycore.setState("fixed")
                        self.disconnectedEnergycore()
                        return True
            else:
                connectedEnergycore.setState("fixed")
                self.disconnectedEnergycore() 
            return True
        elif treasure.getType() == "timeExpanderBomb":
            self.reduceTimeLimit(BOMB_TIME_INSECOND)
            return True
        else:
            return False