from datetime import datetime

from fastapi import FastAPI
from game import *
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from treasure import *
from energyCore import *
GAME_NOT_RUNNING_ASSERTION_STRING="game is not running"

app = FastAPI()
game = Game()
@app.get("/")
async def root():
    return {"message": "hello world"}
@app.get("/test", response_class=HTMLResponse)
async def rsp():
    return """
    <a href="/treasures/">treasures<a>
    """
@app.get("/treasures/use/{treasureId}", response_class=HTMLResponse) # 1
async def useTreasure(treasureId):
    assert gameIsRunning, GAME_NOT_RUNNING_ASSERTION_STRING
    treasure = game.getTreasureById(treasureId)
    if treasure == None: # b
        # treasure doesn't exist
        return TREASURE_NOT_EXIST_TEMPLATE.format(id=treasureId)
    elif treasure.getState() == "uncollected": # c
        # if the treasure not collected, return a page showing treaure is not collected
        return TREASURE_NOT_COLLECTED_TEMPLATE.format(id=treasureId)
    elif treasure.getState() == "used": # d
        return TREASURE_ALREADY_USED_TEMPLATE.format(id=treasureId)
    elif treasure.getState() == "collected": # e,f
        # if the treasue is collected
        # check if the treasure is available to use
        availablility = game.isAvailableTreasure(treasure) # boolean True, or a string of reason for unavailibility
        if availablility == True: # e
            game.applyTreasure(treasure)
            treasure.setState("used")
            return TREASURE_USE_SUCCESS_TEMPLATE.format(id=treasureId, treasureType=treasure.getType())
        else: # f
            return TREASUE_USE_FAIL_TEMPLATE.format(id=treasureId, treasureType=treasure.getType(), reason=availablility)
    else:
        treasureGetState = "None"
        availablility = "None"
        if treasure != False : 
            treasureGetState = treasure.getState()
            if treasureGetState == "collected":
                availablility = game.isAvailableTreasure(treasure)
        return f"""undefined condition: in '/treasures/use/{treasureId}'
        treasure: {treasure}
        treasure.getState() = {treasureGetState}
        availability = {availablility}
        """
    
@app.get("/treasures/collect/{treasureId}", response_class=HTMLResponse) # 2
async def collectTreasure(treasureId):
    assert gameIsRunning, GAME_NOT_RUNNING_ASSERTION_STRING
    treasure: Union[Treasure, None] = game.getTreasureById(treasureId)
    if treasure == None: # b
        # treasure not exist
        return TREASURE_NOT_EXIST_TEMPLATE.format(id=treasureId)
    elif treasure.getState() == "uncollected": # c
        treasure.setState("collected")
        return TREASURE_COLLECT_SUCCESS_TEMPLATE.format(treasureType=treasure.getType())
    elif treasure.getState() in ("collected", "used"): # d
        return TREASURE_UNABLE_COLLECT_TEMPLATE.format(id=treasureId)
    else:
        return f"""undefined condition: in 'treasures/collect/{treasureId}'"""

@app.get("/treasures/my", response_class=HTMLResponse) # 3
async def showTreasures():
    assert gameIsRunning, GAME_NOT_RUNNING_ASSERTION_STRING
    page = MY_TREASURES_TEMPLATE_HEAD
    treasures = game.getTreasures()
    for treasure in treasures:
        page += MY_TREASURE_ITEM_TEMPLATE.format(id=treasure.getId(), treasureType=treasure.getType())
    return page + MY_TREASURES_TEMPLATE_TAIL

@app.get("/energycores/connect/", response_class=HTMLResponse) # 4
async def connectEnergyCore(energycoreId: str, mode: str):
    assert gameIsRunning, GAME_NOT_RUNNING_ASSERTION_STRING
    assert mode in VALID_FIXING_MODE, f"invalid mode: {mode}, mode should be one of: {str(VALID_FIXING_MODE)}"
    energycore = game.getEnergycoreById(energycoreId)
    if energycore == None: # b
        return ENERGY_CORE_NOT_EXIST_TEMPLATE.format(id=energycore.getId())
    elif game.getConnectedEnergycore() == None and energycore.getState()=="unfixed": # c
        # connect energy core to the fixing tool
        game.connectEnergycore(energycore) 
        energycore.setState("fixing")
        # set the fixing mode
        game.setFixingMode(mode)
        if mode=="shed":
            return ENERGY_CORE_CONNECT_SUCCESS_TEMPLATE_SHED.format(id=energycore.getId())
        elif mode=="nonshed":
            return ENERGY_CORE_CONNECT_SUCCESS_TEMPLATE_NONSHED.format(id=energycore.getId())
        else:
            return f"error: something went wrong, mode={mode}"
    elif game.getConnectedEnergycore() != None: # d
        return ALREADY_CONNECTED_A_ENERGY_CORE_TEMPLATE.format(id=game.getConnectedEnergycore().getId())
    elif game.getConnectedEnergycore() == None and energycore.getState() == "fixed": # e
        return ENERGY_CORE_ALREADY_FIXED_TEMPLATE.format(id=energycore.getId())
    else:
        return "undefined branch"

@app.get("/quizzes/answer/", response_class=HTMLResponse) # 5
async def answerQuiz(quizId: str, answer: str):
    assert gameIsRunning, GAME_NOT_RUNNING_ASSERTION_STRING
    connectedEnergycore = game.getConnectedEnergycore()
    quiz = game.getQuizById(quizId)
    if connectedEnergycore != None: # b
        return NO_CONNECTED_ENERGY_CORE_TEMPLATE
    elif quiz == None: # c
        return QUIZ_NOT_EXIST_TEMPLATE
    elif quiz != None and quiz.getState() == "answered": # d
        return QUIZ_ALREADY_ANSWERED_TEMPLATE
    elif quiz.getMode() != game.getFixingMode():# e
        return QUIZ_MODE_NOT_MATCH_TEMPLATE.format(quizMode = quiz.getMode(), fixingMode = game.getFixingMode())
    elif quiz.getAnswer() != answer: # f
        return QUIZ_WRONG_ANSWER_TEMPLATE
    else: # g : energycore connected, valid quiz, correct answer
        if game.getAttackState() == "attacked": # snow monster manage to attack
            quiz.setState("answered")
            game.disconnectedEnergycore()
            connectedEnergycore.setState("fixed")
            game.setAttackState("notAttacked")
            return renderSuccessAnswer(connectedEnergycore, game, attacked=True)
        elif game.getAttackState() == "notAttacked": # snow monster not manage to attack
            return renderSuccessAnswer(connectedEnergycore, game, attacked=False)

@app.get("/hints", response_class=HTMLResponse) # 6
async def showHint():
    assert gameIsRunning, GAME_NOT_RUNNING_ASSERTION_STRING
    return HINTS_TEMPLATE

@app.get("/game/start/{difficulty}", response_class=HTMLResponse) # 7
async def startGame(difficulty):
    assert difficulty in VALID_DIFFICULTY, "invalid difficulty :{difficulty}"
    game.initialise(difficulty=difficulty)
    return SNOW_MONSTER_INSTRUCTION_TEMPLATE

@app.get("/game/expand/", response_class=HTMLResponse) # 8
async def expandGame(timeInSecond: str):
    assert game.isStart(), "Game is not started! Can't expand"
    all_number:bool = True
    for digit in timeInSecond:
        if digit not in "0123456789":
            all_number = False
    assert all_number, "query argument timeInSecond should be a string only with numbers"

    game.expandTimeLimit(timeInSecond)
    return SUCCESS_EXPAND_TIME_TEMPLATE.format(timeLimit = game.getRemainingTimeLimit(), timeExpand = timeInSecond)


@app.get("/attack", response_class=HTMLResponse) # 9
async def attack():
    assert gameIsRunning, GAME_NOT_RUNNING_ASSERTION_STRING
    if game.getAttackChanceCount() == 0: # b
        return NO_MORE_ATTACK_CHANCE
    elif game.getConnectedEnergycore() == None: # c1
        game.setAttackChanceCount(game.getAttackChanceCount() - 1)
        reason="They are not fixing any energy core"
        return FAILURE_ATTACK_TEMPLATE.format(reason=reason)
    elif game.getFixingMode() == "shed": # c2
        game.setAttackChanceCount(game.getAttackChanceCount() - 1)
        reason="They are under the shed"
        return FAILURE_ATTACK_TEMPLATE.format(reason=reason)
    elif game.getConnectedEnergycore() != None and game.getFixingMode() == "nonshed": # c3
        if game.getShieldCount() >= 1:
            game.setShieldCount(game.getShieldCount() - 1)
            game.setAttackChanceCount(game.getAttackChanceCount() - 1)
            reason="They used a shield"
            return FAILURE_ATTACK_TEMPLATE.format(reason=reason)
        else:
            game.setShieldCount(game.getShieldCount() - 1)
            game.setAttackChanceCount(game.getAttackChanceCount() - 1)
            game.setAttackState("attacked")
            game.reduceTime(-1) # use the value in the GAME_CONFIG
            return SUCCESS_ATTACK_TEMPLATE



@app.get("/game/info") # 10
async def getGameInfo(json:str):
    return game.getInfo()

@app.get("/dashboard") # 11
async def showDashboard():
    return dashboard.html



def gameIsRunning():
    return game.isStarted() and (game.isEnded()==False)

def renderSuccessAnswer(connectedEnergycore: Energycore, game: Game, attacked: bool):
    """
        Assume the game is running
        Return a page showing that the user has fixed an energy core successfully
    """
    energycores = game.getEnergycores()
    energycoresListHTML = "<ul>"
    for energycore in energycores:
        energycoresListHTML += "<li>"
        energycoresListHTML += f"id: {energycore.getId()}: state: {energycore.getState()}" 
        energycoresListHTML += "</li>"
    energycoresListHTML += "</ul>"
    if attacked:
        attackedPHTML = """<p stype="{{colour: red}}">The snow monster attacked you when you fixing the energy core</p>"""
    else:
        attackedPHTML = ""
    return """
            <html>
                <head>
                    <title>
                        Energy core Fixed
                    </title>
                </head>
                <body>
                    <h1>You have successfuly fixed the energy core {energycoreId}</h1>
                    {attacked}
                    <p>time remaining: {timeLimit}</p>
                    <h2>Energy cores:</h2>
                        {cores}
                </body>
            </html>
        """.format(energycoreId=connectedEnergycore.getId(), 
                   attacked=attackedPHTML,
                   timeLimit=game.getRemainingTimeLimit(), 
                   cores=energycoresListHTML)