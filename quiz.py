VALID_QUIZ_STATE = ("answered", "notAnswered")

class Quiz:
    def __init__(self, id: str, answer: str, mode: str) -> None:
        """
            id: a string of nubmers
            answer: a string in VALID_ANSWER
            mode: a string 
        """
        for char in id:
            if char not in "0123456789":
                raise ValueError(f"invalid id:{id}")
        else:
            self.id: str = id
        
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
    