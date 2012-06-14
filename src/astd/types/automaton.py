from .astd import *

class Automaton(ASTD):
    """An automaton ASTD class"""    
    _t = "aut"
        
    def __init__(self, i, newname="" ) :
        """ Constructor for an automaton ASTD
        newName -- name of the elem ASTD to be constructed
        i -- astd that is the initial state of the automaton (mandatory) """
        super().__init__(newname)
        self._sigma = set()
        self._N = set()
        self._v = {}
        self._delta = set()
        self._SF = set()
        self._DF = set()
        self.addState(i)
        self._n0 = i.getName() 

    def getInit(self) :
        """ Returns a dictionary mapping variables to initial state values """
        n = self.getName()
        r1 = {}
        r1["State_" + n] = self._n0
        r2 = {}
        for subname,s in self._v.items():
            r2 = dict(list(r2.items()) + list(s.getInit().items()))                    
        r = dict(list(r1.items()) + list(r2.items()))
        return r

    def getBfinal(self) :
        """ Returns a predicate that must hold in order 
        for the astd to be in a final state """
        n = self.getName()
        finalp = "true"
        finalp += " & ".join(map(lambda x:"State_" + n + " = " + x,list(self._SF)))        
        for s in list(self._DF):
            p = self._v[s].getBfinal()
            if p != "true":
                finalp += " & ( " + p + " )"
            elif self._v[s].getType() == "elem" :
                finalp += " & State_" + n + " = " + s
        finalp = finalp.replace("true & ","")
        finalp = finalp.replace(" & true","")
        return finalp
           
    
    def addState(self,i) :
        """ Adds a state to the ASTD
        i -- astd that is the state to be added to the automaton """
        iName = i.getName()
        self._N.add(iName)
        self._v[iName] = i       
    
    def addAsDeepFinalState(self,i):
        """ Adds a state to the ASTD and makes it deep final
        i -- astd that is the state to be added as deep final into the automaton """
        self.addState(i)
        self._DF.add(i.getName())
        assert self._SF.isdisjoint(self._DF)

    def addDFState(self,i):
        """ Adds a state to the ASTD and makes it deep final
        i -- astd that is the state to be added as deep final into the automaton """
        self.addAsDeepFinalState(i)

    def addAsShallowFinalState(self,i):
        """ Adds a state to the ASTD and makes it shallow final
        i -- astd that is the state to be added as deep final into the automaton """
        self.addState(i)
        self._DF.add(i.getName())
        assert self._SF.isdisjoint(self._DF)
        
    def addSFState(self,i):
        """ Adds a state to the ASTD and makes it shallow final
        i -- astd that is the state to be added as deep final into the automaton """
        self.addAsShallowFinalState(i)  

    def addLocalTransition(self, sFrom, sTo, event, predicate=True, final=False):        
        """ Adds a local transition to the ASTD.
        sFrom -- source state
        sTo -- destination state
        event -- tuple containing event name and each parameters name (if any)
        predicate -- guard of the transition
        final -- indicates if the transition is final """
        t = 'loc', sFrom.getName() , '', sTo.getName(), event, predicate, final
        self._delta.add(t)
        self._sigma.add(event[0])

    def addFromSubTransition(self,sFrom ,sFromb , sTo , event, predicate=True, blackhole=False):
        """ Adds a local transition to the ASTD.
        sFrom -- source state at the current level of depth
        sFromb -- deep source state
        sTo -- destination state
        event -- tuple containing event name and each parameters name (if any)
        predicate -- guard of the transition
        final -- indicates if the transition is final """
        if sFrom._t != "aut" :
            raise TypeError("ASTD " +sFrom.getName()+ " should be of type automaton")
        elif sFromb.getName() in sFrom._N :
            t = 'fsub', sFrom.getName(), sFromb.getName(), sTo.getName(), event, predicate, False
            self._delta.add(t)
            self._sigma.add(event[0])
        else :
            raise ASTDNotFound(sFromb.getName())
    
    def addToSubTransition(self,sFrom, sTo, sTob , event, predicate=True, blackhole=False):
        """ Adds a local transition to the ASTD.
        sFrom -- source state
        sTo -- destination state at the current level of depth
        sFromb -- deep destination state
        event -- tuple containing event name and each parameters name (if any)
        predicate -- guard of the transition
        final -- indicates if the transition is final """
        if sTo._t != "aut" :
            raise TypeError("ASTD " +sTo.getName()+ " should be of type automaton")
        elif sTob.getName() in sTo._N :
            t = 'tosub', sFrom.getName(), sTob.getName(), sTo.getName(), event, predicate, False
            self._delta.add(t)
            self._sigma.add(event[0])
        else :
            raise ASTDNotFound(sFromb.getName())
    
    def toB(self):
        """ Returns a dict that represents the translation of the astd into a B machine"""

        n = self.getName()

        submachines = {}
        submachines['MACHINE'] = n
        submachines['SETS'] =  []                        
        submachines['VARIABLES'] =  []
        submachines['INVARIANT'] =  []
        submachines['INITIALISATION'] =  []               
        submachines['OPERATIONS'] =  {}
                            
        for subname,s in self._v.items():
            sub = s.toB()
            submachines['SETS'] += sub['SETS']
            submachines['VARIABLES'] += sub['VARIABLES']
            submachines['INVARIANT'] += sub['INVARIANT']            
            submachines['INITIALISATION'] += sub['INITIALISATION']
            for k in sub['OPERATIONS'].keys() :
                if k not in submachines['OPERATIONS'].keys() :
                    temp = {}
                    temp['PRE'] = []
                    temp['THEN'] = []
                    temp['param'] = ()
                    temp['name'] = k
                    submachines['OPERATIONS'][k] = temp
                submachines['OPERATIONS'][k] = mergeOperationsWithStates( \
                        submachines['OPERATIONS'][k],n,sub['OPERATIONS'][k],subname)
                    
        machine = {}
        machine['MACHINE'] = n

        autStates = "{" + (','.join(self._N)) + "}"
        machine['SETS'] = submachines['SETS'] + [ "AutState_" + n + " = " + autStates]        
                
        machine['VARIABLES'] = submachines['VARIABLES'] + [ "State_" + n ]
        machine['INVARIANT'] = submachines['INVARIANT'] + [ "State_" + n + " :  AutState_" + n ]
        machine['INITIALISATION'] =  submachines['INITIALISATION'] + [ "State_" + n + " := " + self._n0 ]
               
        machine['OPERATIONS'] =  {}
        
        for sigma in self._sigma:
            op = {}
            op['PRE'] = []
            op['THEN'] = []
            
            for x in [ y for y in self._delta if y[4][0] == sigma ] :
                pre = "State_" + n + " = " + x[1]
                then = "State_" + n + " := " + x[3] 
                if x[0] == 'tosub' :
                    then += " || State_" + x[3] + " := " + x[2]
                if x[0] == 'fsub' :
                    pre += " & State_" + x[1] + " = " + x[2]
                if x[5] != True :
                    pre += " & " + x[5]
                if x[6] == True :
                    pre += " & " + self._v[x[1]].getBfinal()                
                op['PRE'].append(pre)                
                op['THEN'].append((pre,then))            
            op['param'] = x[4][1:]    
            op['name'] = x[4][0]    
            machine['OPERATIONS'][op['name']] = op
        machine['OPERATIONS'] = mergeOperations(machine['OPERATIONS'],submachines['OPERATIONS'])
        
        return machine        
        
    def __str__(self):
        txt = "ASTD named " + self._name + " of type " + self._t +"\n"
        for stateName, state in self._v.items() :
            txt += "  State " + stateName + " : " + state._t + "\n"
        txt += "  Initial state : " + self._n0 + "\n"
        for f in self._DF :
            txt += "  Deep final state : " + str(f) + "\n"
        for f in self._SF :
            txt += "  Shallow final state : " + str(f) + "\n"
        txt += "\n  Transitions ------\n"
        for d in self._delta :
            txt += "    > " + str(d) + "\n"        
        txt += "  ------ End of transitions\n"
        txt += "End of " + self._name        
        return txt
        
    
      