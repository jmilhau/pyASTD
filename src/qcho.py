import astd

s1 = astd.Elem('s1')
s2 = astd.Elem('s2')
s3 = astd.Elem('s3')
c = astd.Automaton(s1,"c")
c.addState(s2)
c.addDFState(s3)
c.addLocalTransition(s1,s2,('e1','xx'))
c.addLocalTransition(s2,s3,('e2','xx'))

d = astd.qChoice(c,"xx","{x4,x5,x6}",'dd')
e = astd.Kleene(d,'ee')

e.Bprint()
