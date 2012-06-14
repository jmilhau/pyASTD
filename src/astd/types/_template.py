from .astd import *

class Kleene(ASTD):
    """An Kleene Closure ASTD class"""    
    _t = "kle"
        
    def __init__(self, b, newname="" ) :
        """ Constructor for a Kleene ASTD
        b -- astd that is the operand of the Closure Kleene ASTD (mandatory)
        newName -- name of the elem ASTD to be constructed """
        super().__init__(newname)
        self.b = b

    def getInit(self) :
        """ Returns a dictionary mapping variables to initial state values """
        r = {}
        r["State_" + n] = "notstarted"
        r = dict(list(r.items()) + list(self.b.getInit().items()))
        return r

    def getBfinal(self) :
        """ Returns a predicate that must hold in order 
        for the astd to be in a final state """
        finalp = "State_" + n + " = notstarted" 
        p = self.b.getBfinal()
        if p != "true":
                finalp += " or ("+ p +")"        
        return finalp
    
    def toB(self):
        """ Returns a dict that represents the translation of the astd into a B machine"""
   
        
    def __str__(self):
        txt = "ASTD named " + self._name + " of type " + self._t +"\n"
        txt += "   Sub ASTD : " + self.b._name + " of type " + self.b._t +"\n"
        txt += "End of " + self._name        
        return txt
        
    
      