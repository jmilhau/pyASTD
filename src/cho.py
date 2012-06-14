import astd

s1 = astd.Elem('s1')
s2 = astd.Elem('s2')
s3 = astd.Elem('s3')
s4 = astd.Elem('s4')
s5 = astd.Elem('s5')
s6 = astd.Elem('s6')
s7 = astd.Elem('s7')
s8 = astd.Elem('s8')


a = astd.Automaton(s1,"a")
a.addState(s2)
a.addState(s3)
a.addDFState(s4)
a.addLocalTransition(s1,s2,('e1',))
a.addLocalTransition(s1,s3,('e2',))
a.addLocalTransition(s3,s4,('e5',))
a.addLocalTransition(s2,s4,('e4',))

b = astd.Automaton(s5,"b")
b.addState(s6)
b.addState(s7)
b.addDFState(s8)
b.addLocalTransition(s5,s6,('e2',))
b.addLocalTransition(s5,s7,('e3',))
b.addLocalTransition(s6,s8,('e6',))
b.addLocalTransition(s7,s8,('e7',))

c = astd.Choice(a,b,"c")
c.Bprint()
