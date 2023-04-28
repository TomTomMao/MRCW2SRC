ENERGY_CORE_NOT_EXIST_TEMPLATE = """<html><head><title>Energy core not exist</title></head><body><p>The energy core id {id} is not valid.</p></body></html>"""
ENERGY_CORE_CONNECT_SUCCESS_TEMPLATE_SHED = """<html><head><title>Energy core connected success</title></head><body><p>Energy Core {id} is connected to the fixing tool successfully. </br>The fixing mode is "shed".</p>
<p>You should answer the question paper under the blue shed, by scanning the artcode of the correct answer.</p>
<p>You will be safe from being attacked by the snow monster</p>
<p>But the questions are difficult</p>
<p>Open your artCode app and scan the art code on it!</p>
<p>Don't cheat if you do not want make the game boring</p></body></html>""" 
ENERGY_CORE_CONNECT_SUCCESS_TEMPLATE_NONSHED = """<html><head><title>Energy core connected success</title></head><body><p>Energy Core {id} is connected to the fixing tool successfully. </br>The fixing mode is "nonshed".</p>
<p>You should answer the question paper on the other table, by scanning the artcode of the correct answer.</p>
<p>The quizzes are fairly easy, but you might be attacked by the snow monster</p>
<p>Open your artCode app and scan the art code on it!</p>
<p>Don't cheat if you do not want make the game boring</p></body></html>""" 
ALREADY_CONNECTED_A_ENERGY_CORE_TEMPLATE = """<html><head><title>Invalid Connect: Already Connect</title></head><body><p>The fixing tool has already connected to the energy core (id:{id})</p></body></html>""" 
ENERGY_CORE_ALREADY_FIXED_TEMPLATE =  """<html><head><title>Invalid Connect: Already fixed</title></head><body><p>The energy core (id:{id}) has already been fixed</p></body></html>""" 


VALID_ENERGY_CORE_STATE = ("fixed", "unfixed", "fixing")
class Energycore:
    def __init__(self, id: str):
        """
            id: a string of numbers
        """
        for char in id:
            if char not in "0123456789":
                raise ValueError(f"Invalid Id {id}")
        self.id = id
        self.state = "unfixed"
    
    def getId(self) -> str:
        return self.id
    
    def getState(self) -> str:
        return self.state

    def setState(self, newState: str) -> None:
        if newState not in VALID_ENERGY_CORE_STATE:
            raise ValueError(f"invalide newState: {newState}, should be in {VALID_ENERGY_CORE_STATE}") 
        self.state = newState
    def toDictionary(self) -> dict:
        """
            Return a dictionary like this: {"id": "1", "state": "fixed"}
        """
        return {"id": self.getId(), "state": self.getState()}
