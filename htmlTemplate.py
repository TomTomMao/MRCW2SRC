NO_CONNECTED_ENERGY_CORE_TEMPLATE = f"""
    <html>
        <head>
        <title>
            No energy core connected
        </title>
        </head>
        <body>
            There is no energy core connected
        </body>
    </html>
"""
QUIZ_GAME_END_TEMPLATE ="""
<html>
        <head>
        <title>
            Game Over
        </title>
        </head>
        <body>
            You can't fixing energy cores now. Because the game is over</b>
            If you want to keep playing, click <a href="../../game/expand?timeInSecond=60" target="_blank" role="button" class="btn btn-primary m-1">expand time</a> to expand time
        </body>
    </html>
"""
QUIZ_NOT_EXIST_TEMPLATE = f"""
    <html>
        <head>
        <title>
            Quiz not exists
        </title>
        </head>
        <body>
            This quiz does not exist
        </body>
    </html>
"""

QUIZ_ALREADY_ANSWERED_TEMPLATE = f"""
    <html>
        <head>
        <title>
            Quiz already answered
        </title>
        </head>
        <body>
            This quiz has already been answered.
        </body>
    </html>
"""

QUIZ_MODE_NOT_MATCH_TEMPLATE = """
    <html>
        <head>
        <title>
            Wrong quiz mode
        </title>
        </head>
        <body>
            This quiz mode {quizMode} is not the same as the fixingMode {fixingMode}
        </body>
    </html>
"""

QUIZ_WRONG_ANSWER_TEMPLATE = """
    <html>
        <head>
        <title>
            Wrong answer
        </title>
        </head>
        <body>
            Your answer is incorrect.
            The time limit is reduced.
        </body>
    </html>
"""

FAILURE_ATTACK_TEMPLATE = """
    <html>
        <head>
        <title>
            Fail to Attack
        </title>
        </head>
        <body>
            Fail to attack. Reason: {reason}
        </body>
    </html>
"""

SUCCESS_ATTACK_TEMPLATE = """
    <html>
        <head>
        <title>
            Success to Attack
        </title>
        </head>
        <body>
            Success to attack!
        </body>
    </html>
"""

ERROR_PAGE_TEMPLATE = """
    <html>
        <head>
        <title>
            Error
        </title>
        </head>
        <body>
            {errorMessage}
        </body>
    </html>
    
"""