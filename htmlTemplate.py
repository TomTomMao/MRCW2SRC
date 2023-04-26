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
            Fail to Attack
        </title>
        </head>
        <body>
            Success to attack!
        </body>
    </html>
"""