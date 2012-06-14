from .astd import *
     
class Elem(ASTD):
    """An elementary ASTD class"""    
    _t = "elem"    
    def __str__(self):
        return "elem"

    def toB(self):  
        """ Returns a dict that represents the translation of the astd into a B machine"""      
        n = self.getName()    
        machine = {}
        machine['MACHINE'] = n
        machine['SETS'] =  []                        
        machine['VARIABLES'] =  []
        machine['INVARIANT'] =  []
        machine['INITIALISATION'] =  []                           
        machine['OPERATIONS'] = {}
        return machine

    def getBfinal(self) :
        """ Returns a predicate that must hold in order 
        for the astd to be in a final state """
        return "true"
        
    def getInit(self) :
        """ Returns a dictionary mapping variables to initial state values """
        return {}
                