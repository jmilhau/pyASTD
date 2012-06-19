from .astd import *

class Synchronization(ASTD):
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
        
        Bops = set(list(subB['OPERATIONS'].keys()))
        Cops = set(list(subC['OPERATIONS'].keys()))
        BCops = Bops & Cops
        
        set1 = self.delta & BCops
        set2 = self.delta - BCops
        set3 = (Bops | Cops) - self.delta
        
        for sigma in set1 :
            op = {}
            op['param'] = subB['OPERATIONS'][sigma]['param']   
            op['name'] = sigma
            op['PRE'] = []
            op['THEN'] = []
            op['TYPE'] = subB['OPERATIONS'][sigma]['TYPE'] + subC['OPERATIONS'][sigma]['TYPE']
            pre =  getPre(subB['OPERATIONS'][sigma]['PRE']) + " &\n " + getPre(subC['OPERATIONS'][sigma]['PRE'])
            then = getThen(subB['OPERATIONS'][sigma]['THEN'])+" ||\n"+getThen(subC['OPERATIONS'][sigma]['THEN'])            
            op['PRE'].append("("+pre+ ")") 
            op['THEN'].append((pre,then))                        
            machine['OPERATIONS'][sigma] = op 
            
        for sigma in set2 :
            op = {}
            if sigma in Bops :
                op['param'] = subB['OPERATIONS'][sigma]['param']  
                op['TYPE'] = subB['OPERATIONS'][sigma]['TYPE']
            else :
                op['param'] = subC['OPERATIONS'][sigma]['param']
                op['TYPE'] = subC['OPERATIONS'][sigma]['TYPE']
            op['name'] = sigma
            op['PRE'] = ["false"]
            op['THEN'] = [("false","skip")]
            machine['OPERATIONS'][sigma] = op
            
        for sigma in set3 :
            op = {}
            op['name'] = sigma
            op['PRE'] = []
            op['THEN'] = []
            if sigma in BCops :
                op['TYPE'] = subB['OPERATIONS'][sigma]['TYPE'] + subC['OPERATIONS'][sigma]['TYPE']
                op['param'] = subB['OPERATIONS'][sigma]['param']
                pre1 =  getPre(subB['OPERATIONS'][sigma]['PRE']) 
                pre2 =  getPre(subC['OPERATIONS'][sigma]['PRE'])
                then1 = getThen(subB['OPERATIONS'][sigma]['THEN'])
                then2 = getThen(subC['OPERATIONS'][sigma]['THEN'])
                op['PRE'].append("(" +pre1+ ")" ) 
                op['PRE'].append("(" +pre2+ ")" )
                op['THEN'].append((pre1,then1))                        
                op['THEN'].append((pre2,then2))                        
            elif sigma in Bops :
                op['TYPE'] = subB['OPERATIONS'][sigma]['TYPE']
                op['param'] = subB['OPERATIONS'][sigma]['param']
                pre1 = getPre(subB['OPERATIONS'][sigma]['PRE']) 
                then1 = getThen(subB['OPERATIONS'][sigma]['THEN'])
                op['PRE'].append("(" + pre1+ ")" ) 
                op['THEN'].append((pre1,then1))                        
            else :
                op['TYPE'] = subC['OPERATIONS'][sigma]['TYPE']
                op['param'] = subC['OPERATIONS'][sigma]['param']
                pre2 =  getPre(subC['OPERATIONS'][sigma]['PRE']) 
                then2 = getThen(subC['OPERATIONS'][sigma]['THEN'])
                op['PRE'].append("(" +pre2+ ")")
                op['THEN'].append((pre2,then2))  
            machine['OPERATIONS'][sigma] = op

        return machine
        
    def __str__(self):
        txt = "ASTD named " + self._name + " of type " + self._t +"\n"
        txt += "    first astd : " + self.b._name + " of type " + self.b._t +"\n"
        txt += "   second astd : " + self.c._name + " of type " + self.c._t +"\n"
        txt += "End of " + self._name        
        return txt
        