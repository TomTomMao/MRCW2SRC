VALID_QUIZ_STATE = ("answered", "notAnswered")
VALID_ANSWER = ("A", "B", "C", "D")
VALID_QUIZ_MODE = ("shed", "nonshed")
class Quiz:
    def __init__(self, id: str, answer: str, mode: str) -> None:
        """
            id: a string of numbers
            answer: a string showing the correct answer of the quiz, must in VALID_ANSWER
            mode: a string showing if it is under the shed or not, must in VALID_QUIZ_MODE
            state: a string showing if it is answered, must in VALID_QUIZ_STATE
        """
        for char in id:
            if char not in "0123456789":
                raise ValueError(f"invalid id:{id}, it must be a stirng of numbers")
        else:
            self.id: str = id
        
        if answer not in VALID_ANSWER:
            raise ValueError(f"invalid answer: {answer}, should be in {VALID_ANSWER}")

        if mode not in VALID_QUIZ_MODE:
            raise ValueError(f"invalid mode: {mode}, should be in {VALID_QUIZ_MODE}")

        self.answer: str = answer
        self.mode: str = mode
        self.state: str = "notAnswered"
    
    def getId(self) -> str:
        return self.id

    def getAnswer(self) -> str:
        return self.answer

    def getMode(self) -> str:
        return self.mode

    def getState(self) -> str:
        return self.state

    def setState(self, newState) -> None:
        if newState not in VALID_QUIZ_STATE:
            raise ValueError(f"invalid newState: {newState}, it should be in {VALID_QUIZ_STATE}")
        else:
            self.state = newState
    
    def toDictionary(self) -> dict:
        """
            Return a dictionary like this: {"id": "1", "answer": "A", "mode": "nonshed"}
        """
        return {"id": self.getId(), "answer": self.getAnswer(), "mode": self.getMode()}