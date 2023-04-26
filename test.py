from game import *
# g = Game()
# gameDifficulty = "hard"
# r = [random.choices(
#     GAME_CONFIG[gameDifficulty]['treasure']['types'], weights=GAME_CONFIG[gameDifficulty]['treasure']['weights'], k=GAME_CONFIG[gameDifficulty]['treasure']['count'])][0]
# print(r)

import quiz
import treasure
import energyCore

# t1 = Treasure("1", "timeExpander")
# t2 = Treasure("2", "timeExpander")
# t3 = Treasure("3", "timeExpander")
# t4 = Treasure("4", "timeExpander")
# # print(t1.toDictionary())
# print(json.dumps({"treasures": [t1.toDictionary(), t2.toDictionary(), t3.toDictionary()]}))#

# print(g.isStart())

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

print(readQuiz("./quiz.csv"))