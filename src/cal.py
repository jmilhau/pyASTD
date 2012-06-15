import astd

s1 = astd.Elem('s1')
s2 = astd.Elem('s2')

a = astd.Automaton(s1,"a")
a.addDFState(s2)
a.addLocalTransition(s1,s2,('e1',))
a.addLocalTransition(s2,s2,('e2',))

b = astd.Call(a,"b")
b.Bprint()