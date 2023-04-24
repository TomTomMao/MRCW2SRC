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
class Game:
    def __init__(self) -> None:
        pass