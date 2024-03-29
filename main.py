from datetime import datetime

from fastapi import FastAPI
from game import *
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from treasure import *
from energyCore import *
from htmlTemplate import *
GAME_NOT_RUNNING_ASSERTION_STRING="game is not running"

app = FastAPI()
game: Game = Game()
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
    if len(treasures) == 0:
        return page + "You don't have any treasure" + MY_TREASURES_TEMPLATE_TAIL
    for treasure in treasures:
        if treasure.getState() == "collected":
            page += MY_COLLECTED_TREASURE_ITEM_TEMPLATE.format(id=treasure.getId(), treasureType=treasure.getType())
        elif treasure.getState() == "used":
            page += MY_USED_TREASURE_ITEM_TEMPLATE.format(id=treasure.getId(), treasureType=treasure.getType())
    return page + MY_TREASURES_TEMPLATE_TAIL

@app.get("/energycores/connect/", response_class=HTMLResponse) # 4
async def connectEnergyCore(energycoreId: str, mode: str):
    assert gameIsRunning, GAME_NOT_RUNNING_ASSERTION_STRING
    assert mode in VALID_FIXING_MODE, f"invalid mode: {mode}, mode should be one of: {str(VALID_FIXING_MODE)}"
    energycore: Union[Energycore, None] = game.getEnergycoreById(energycoreId)
    connectedEnergyCore: Union[Energycore, None] = game.getConnectedEnergycore()
    if energycore == None: # b
        print("flag1")
        return ENERGY_CORE_NOT_EXIST_TEMPLATE.format(id=energycoreId)
    elif connectedEnergyCore == None and energycore.getState()=="unfixed": # c
        print("flag2")
        # connect energy core to the fixing tool
        game.connectEnergycore(energycore) 
        energycore.setState("fixing")
        print(energycore.toDictionary())
        # set the fixing mode
        game.setFixingMode(mode)
        if mode=="shed":
            # set attack count for this fixing
            game.setAttackCountForThisFixing(0)
            return ENERGY_CORE_CONNECT_SUCCESS_TEMPLATE_SHED.format(id=energycore.getId())
        elif mode=="nonshed":
            # set attack count for this fixing
            game.setAttackCountForThisFixing(0)            
            return ENERGY_CORE_CONNECT_SUCCESS_TEMPLATE_NONSHED.format(id=energycore.getId())
        else:
            return f"error: something went wrong, mode={mode}"
    elif connectedEnergyCore != None: # d
        print("flag3")
        return ALREADY_CONNECTED_A_ENERGY_CORE_TEMPLATE.format(id=connectedEnergyCore.getId())
    elif connectedEnergyCore == None and energycore.getState() == "fixed": # e
        print("flag4")
        return ENERGY_CORE_ALREADY_FIXED_TEMPLATE.format(id=energycore.getId())
    else:
        print("flag5")
        return "undefined branch"

@app.get("/quizzes/answer/", response_class=HTMLResponse) # 5
async def answerQuiz(quizId: str, answer: str):
    assert gameIsRunning, GAME_NOT_RUNNING_ASSERTION_STRING
    connectedEnergycore: Union[Energycore, None] = game.getConnectedEnergycore()
    quiz = game.getQuizById(quizId)
    if game.isEnded() == True:
        return QUIZ_GAME_END_TEMPLATE
    elif connectedEnergycore == None: # b
        return NO_CONNECTED_ENERGY_CORE_TEMPLATE
    elif quiz == None: # c
        return QUIZ_NOT_EXIST_TEMPLATE
    elif quiz != None and quiz.getState() == "answered": # d
        return QUIZ_ALREADY_ANSWERED_TEMPLATE
    elif quiz.getMode() != game.getFixingMode():# e
        return QUIZ_MODE_NOT_MATCH_TEMPLATE.format(quizMode = quiz.getMode(), fixingMode = game.getFixingMode())
    elif quiz.getAnswer() != answer: # f
        # panelty
        game.reduceTimeLimit(10)
        return QUIZ_WRONG_ANSWER_TEMPLATE
    else: # g : energycore connected, valid quiz, correct answer
        quiz.setState("answered")
        game.disconnectedEnergycore()
        connectedEnergycore.setState("fixed")
        # set the fixing mode to be inactive once fixed the connected energy core
        game.setFixingMode("inactive")
        if game.getAttackState() == "attacked": # snow monster manage to attack
            game.setAttackState("notAttacked")
            return renderSuccessAnswer(connectedEnergycore, game, attacked=True)
        elif game.getAttackState() == "notAttacked": # snow monster not manage to attack
            game.setAttackState("notAttacked")
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

    game.expandTimeLimit(int(timeInSecond))
    return SUCCESS_EXPAND_TIME_TEMPLATE.format(timeLimit = game.getRemainingTimeLimit(), timeExpand = timeInSecond)


@app.get("/attack", response_class=HTMLResponse) # 9
async def attack():
    assert gameIsRunning, GAME_NOT_RUNNING_ASSERTION_STRING
    attackCountForThisFixing: Union[int, None] = game.getAttackCountForThisFixing()
    if game.getAttackChanceCount() == 0: # b
        return FAILURE_ATTACK_TEMPLATE.format(reason="You don't have any attack chance")
    elif game.getConnectedEnergycore() == None: # c1
        game.setAttackChanceCount(game.getAttackChanceCount() - 1)
        reason="They are not fixing any energy core"
        return FAILURE_ATTACK_TEMPLATE.format(reason=reason)
    elif game.getFixingMode() == "shed": # c2
        game.setAttackChanceCount(game.getAttackChanceCount() - 1)
        reason="They are under the shed"
        return FAILURE_ATTACK_TEMPLATE.format(reason=reason)
    elif attackCountForThisFixing!=None and attackCountForThisFixing >= SINGLE_FIX_MAX_ATTACK:
        # if it is greater than or equal to the max attack count for a single fix, return false attack
        reason=f"You can't attack them for this quiz now"
        return FAILURE_ATTACK_TEMPLATE.format(reason=reason)
    elif game.getConnectedEnergycore() != None and game.getFixingMode() == "nonshed": # c3
        if game.getShieldCount() >= 1:
            game.setShieldCount(game.getShieldCount() - 1)
            game.setAttackChanceCount(game.getAttackChanceCount() - 1)
            reason="They used a shield"
            return FAILURE_ATTACK_TEMPLATE.format(reason=reason)
        else:
            # don't have shield
            game.setAttackChanceCount(game.getAttackChanceCount() - 1)
            game.setAttackState("attacked")
            game.reduceTime(-1) # -1 refers to use the value in the GAME_CONFIG
            attackCountForThisFixing: Union[int, None] = game.getAttackCountForThisFixing()
            if attackCountForThisFixing == None:
                return ERROR_PAGE_TEMPLATE.format(errorMessage = "AttackCountForThisFixing is None")
            else:
                game.setAttackCountForThisFixing(attackCountForThisFixing + 1) # increment by 1
            return SUCCESS_ATTACK_TEMPLATE
    else:
        return ERROR_PAGE_TEMPLATE.format(errorMessage="something went wrong")


@app.get("/game/info") # 10
async def getGameInfo(json:str):
    return game.getInfoJSON()

@app.get("/dashboard") # 11
async def showDashboard():
    return FileResponse('dashboard.html')



def gameIsRunning():
    return game.isStart() and (game.isEnded()==False)

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
        attackedPHTML = """<h2 style="color: red">The snow monster attacked you when you fixing the energy core</h2><p>Next time, connect to the quiz under the shed, which can protect you.</p>"""
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
                    <p>time remaining: {timeLimit} seconds</p>
                    <h2>Energy cores:</h2>
                        {cores}
                </body>
            </html>
        """.format(energycoreId=connectedEnergycore.getId(), 
                   attacked=attackedPHTML,
                   timeLimit=game.getRemainingTimeLimit(), 
                   cores=energycoresListHTML)