from .astd import *

class Choice(ASTD):
    """An Synchronization ASTD class"""    
    _t = "syn"
        
    def __init__(self, b, c, d, newname="" ) :
        """ Constructor for a Synchronization ASTD
        b -- astd that is the LHS operand of the synchronization ASTD (mandatory)
        c -- astd that is the RHS operand of the synchronization ASTD (mandatory)
        d -- list of the event labels to be synch (mandatory)
        newName -- name of the elem ASTD to be constructed """
        super().__init__(newname)
        self.b = b
        self.c = c
        self.delta = set(d)

    def getInit(self) :
        """ Returns a dictionary mapping variables to initial state values """
        r = {}
        r = dict(list(self.b.getInit().items()) + list(self.c.getInit().items()))

        return r

    def getBfinal(self) :
        """ Returns a predicate that must hold in order 
        for the astd to be in a final state """
        fb = self.b.getBfinal()
        fc = self.c.getBfinal()
        return "( "+fb+" ) & ( "+fc+" )"
    
    def toB(self):
        """ Returns a dict that represents the translation of the astd into a B machine"""
        n = self.getName()        
        subB = self.b.toB()
        subC = self.c.toB()
                    
        machine = {}
        machine['MACHINE'] = n
        
        machine['SETS'] = subB['SETS'] + list(set(subC['SETS']) - set(subB['SETS']))        
        machine['VARIABLES'] = subB['VARIABLES'] + subC['VARIABLES']        
        machine['INVARIANT'] = subB['INVARIANT'] + subC['INVARIANT']
        machine['INITIALISATION'] = subB['INITIALISATION'] + subC['INITIALISATION']
        machine['OPERATIONS'] =  {}  
        
        return machine
        
    def __str__(self):
        txt = "ASTD named " + self._name + " of type " + self._t +"\n"
        txt += "    first astd : " + self.b._name + " of type " + self.b._t +"\n"
        txt += "   second astd : " + self.c._name + " of type " + self.c._t +"\n"
        txt += "End of " + self._name        
        return txt
        