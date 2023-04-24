from typing import Union

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
VALID_FIXING_MODE = ("shed", "nonshed")
VALID_ATTACK_STATE = ("attacked", "notAttacked")
ATTACK_TIME = 15
class Game:
    def __init__(self) -> None:
        pass
    
    def getTreasureById(treasureId: str) -> Union[Treasure, bool]:
        pass
    
    def getTreasures() -> list[Treasure]:
        """
            Return a list of treasure object
        """
    
    def getEnergycoreById(energycoreId) -> Union[Energycore, bool]:
        """
            Return an energy core object if exist, or return False
        """
    
    def getConnectedEnergycore() -> Union[Energycore, bool]:
        """
            Return the energy core that is connected to the fixing tool if exists
            Return False if there is no energy core connecting to the fixing tool
        """

    def getQuizById(quizId: str) -> Union[Quiz, bool]:
        """
            Return a quiz Object whose id = quizId if there exists such a quiz.
            Otherwise, return False
        """

    def getFixingMode() -> str:
        """
            Return "shed" if the human is answering the questions under the shed
            Return "nonshed" if the human is not answering the questions under the shed
        """

    def getAttackState() -> str:
        """
            Return "attacked" if the snow monster has successfully attacted the human
            Otherwise return "notAttacked"
        """   

    def setAttackState(attackState: str) -> bool:
        """
            Assume the attackState in VALID_ATTACK_STATE
            Set the attack state to be attackState, if it is a valid state. and return True
            Return False otherwise.
        """
        assert attackState in VALID_ATTACK_STATE

    def disconnectedEnergycore() -> bool:
        """
            If there is an connected Energy core, disconnected it and return true
            If there is no enercy core that is connected to the fixing tool, return false
        """

    def isAvailableTreasure(treasure: Treasure) -> bool:
        pass
    
    def applyTreasure(treasure: Treasure) -> bool:
        pass