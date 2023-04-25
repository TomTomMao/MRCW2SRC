from typing import Union
from datetime import datetime
from datetime import timedelta
import random
from energyCore import Energycore
from treasure import Treasure
from quiz import Quiz

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
    import csv
    data = []
    with open(path) as quizConfigFile:
        csvreader = csv.reader(quizConfigFile, delimiter='\t')
        for row in csvreader:
            data.append(row)
    config = [{data[0][0]: entry[0], data[0][1]: entry[1], data[0][2]: entry[2]} for entry in data[1:]]
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
except:
    print("error: fail to read quiz file")
ENERGYCORE_COUNT = 7
ENERGYCORE_CONFIG=[{'id':str(i)} for i in range(1,ENERGYCORE_COUNT)]

GAME_CONFIG = {
    'easy': {
        'quizCount': 20,
        'attackTime': 15,
        # for random.choices()
        'treasure': {'types': ['shield', 'timeExpander', 'fixer'], 'weights': [6, 2, 2], 'count': 20},
        'timeLimit': timedelta(minutes=10),
        'attackChance': 15,
        'quiz': []
    }, 'mid': {
        'quizCount': 20,
        'attackTime': 20,
        # for random.choices()
        'treasure': {'types': ['shield', 'timeExpander',
                               'fixer'], 'weights': [7, 3, 1], 'count': 20},
        'timeLimit': timedelta(minutes=7.5),
        'attackChance': 20
    }, 'hard': {
        'quizCount': 20,
        'attackTime': 30,
        # for random.choices()
        'treasure': {'types': ['shield', 'timeExpander', 'fixer', 'timeExpanderBomb'], 'weights': [6, 2, 1, 1], 'count': 20},
        'timeLimit': timedelta(minutes=5),
        'attackChance': 50
    }
}


class Game:
    def __init__(self) -> None:
        self.treasures: list[Treasure]
        self.quizzes: list[Quiz]
        self.energycores: list[Energycore]
        self.isGameStarted: bool
        self.isGameEnded: bool
        self.startTime: bool
        self.endTime: bool
        self.timeLimit: int  # seconds
        self.shieldCount: int
        self.fixingMode: str
        self.gameDifficulty: str
        self.attackChance: int
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
                Initialize the shieldCount, fixingMode, attackChance, connectedCore
                Set isGameStarted to be True
        """

        assert difficulty in VALID_DIFFICULTY, f"invalid difficulty: {difficulty}, it should be on of {VALID_DIFFICULTY}"

        # initialise the difficulty
        self.gameDifficulty = difficulty

        # initialise the treasure list
        treasureTypeList = [random.choices(
            GAME_CONFIG[self.gameDifficulty]['treasure']['types'], weights=GAME_CONFIG[self.gameDifficulty]['treasure']['weights'], k=GAME_CONFIG[self.gameDifficulty]['treasure']['count'])]
        self.treasures = [Treasure(id=str(index), treasureType=_treasureType) for index, _treasureType in enumerate(treasureTypeList)]

        # initialise the quizzes list
        self.quizzes = [Quiz(id=quizConfig['id'], answer=quizConfig['answer'], mode=quizConfig['mode']) for quizConfig in QUIZ_CONFIG]

        # initialise the energycores list
        self.energycores = [Energycore(id=energycoreConfig['id']) for energycoreConfig in ENERGYCORE_CONFIG]

        # initialize the startTime, endTime, and the timeLimit
        self.startTime = datetime.now()
        self.timeLimit = GAME_CONFIG[self.gameDifficulty]['timeLimit']
        self.endTime = self.startTime + self.timeLimit

        # Initialize the shieldCount, fixingMode, attackChance, connectedCore, attackState
        self.shieldCount = 0
        self.fixingMode = "inactive"
        self.attackChance = GAME_CONFIG[self.gameDifficulty]['attackChance']
        self.connectedCore = None
        self.attackState = "notAttacked"

        # set game state
        self.isGameStarted = True
        self.isGameEnded = True


    def getTreasures(self) -> list[Treasure]:
        """
            Assume game is started.
            Return a list of treasure object.
        """
        return self.treasures

    def getConnectedEnergycore(self) -> Union[Energycore, None]:
        """
            Assume game is started.
            Return the energy core that is connected to the fixing tool if exists
            Return None if there is no energy core connecting to the fixing tool
        """
        assert self.isGameStarted, "game must be started"
        if self.connectedCore==None:
            return None
        else: return self.connectedCore

    def getTreasureById(self, treasureId: str) -> Union[Treasure, bool]:
        """
            Assume game is started.
            treasureId: should be a string only contain number
            Return False if there is no treasure whose id is treasureId.
            Return a treasure object whose id is the same as treasureId.
        """
        # check pre condition
        assert self.isGameStarted, "game must be started"
        if (checkDigit(treasureId)==False):
            raise ValueError('treasureId must only contain numbers "0" to "9"')
            
        for treasure in self.treasures:
            if treasure.getId() == treasureId:
                return treasure
        else:
            return False

    def getEnergycoreById(self, energycoreId) -> Union[Energycore, None]:
        """
            Assume game is started.
            energycoreId: should be a string only contain number
            Return an energy core object if exist. 
            Otherwise return None
        """
        assert self.isGameStarted, "game must be started"
        if (checkDigit(energycoreId)==False):
            raise ValueError('energycoreId must only contain numbers "0" to "9"')
        
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
        assert self.isGameStarted, "game must be started"
        if (checkDigit(quizId)==False):
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
        assert self.isGameStarted, "game must be started"
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
        assert self.isGameStarted, "game must be started"
        assert self.attackState in VALID_ATTACK_STATE, "invalid attribute value of game object"
        return self.attackState

    def setAttackState(self, attackState: str) -> bool:
        """
            Assume game is started.
            Assume the attackState in VALID_ATTACK_STATE
            Set the attack state to be attackState, if it is a valid state. and return True
            Return False otherwise.
        """
        assert self.isGameStarted, "game must be started"
        assert attackState in VALID_ATTACK_STATE, "invalid parameter value"
        self.attackState = attackState
        return True

    def getAttackChanceCount() -> int:
        """
            Assume the game is started
        """
    def setAttackChanceCount()
    def getShieldCount()
    def getTimeLimit()
    def reduceTime()
    def setShieldCount(self, )

    def disconnectedEnergycore(self) -> bool:
        """
            If there is an connected Energy core, disconnected it and return True
            If there is no enercy core that is connected to the fixing tool, return False
        """

    def isAvailableTreasure(self, treasure: Treasure) -> bool:
        """
            Assume the treasure object is part of self.
            If the game is suitable to apply the treasure, return True
            If the game is not suitable to apply the treasure, return False.
            If the treasure is a timeExpander, then ...
            If the treasure is a shield, then ...
            If the treasure is a fixer, then ...
        """
        pass

    def isStart(self) -> bool:
        """
            If the game is started, return True
            If the game is not started, return False
        """
        pass

    def isEnded(self) -> bool:
        """
            If the game is ended, return True
            If the game is not ended, return False
        """

    def expandTimeLimit(self, timeInSecond: int) -> bool:
        pass

    def applyTreasure(self, treasure: Treasure) -> bool:
        pass


