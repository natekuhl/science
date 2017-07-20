import graphviz as gv

j=0

g1 = gv.Graph(format='png')
g1.node('A', 'happy little node')
g1.node('B')
g1.node('{}'.format(j))
g1.edge('A' , 'B')



