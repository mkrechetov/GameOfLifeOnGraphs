from utils import *
Glst = nx.readwrite.graph6.read_graph6('graph5c.g6')
Glst = [G for G in Glst if nx.is_connected(G)]
print("There are ", len(Glst), " connected graphs in this list.")

steps = {}

for i in range(len(Glst)):
    for j in range(i+1, len(Glst)):
        result = testing(Glst[i], Glst[j])
        steps[(i, j)] = result
        if (result >= 3):
        	print('Graphs no. {} and no. {} steps are {}'.format(i, j, result))
        
print('Longest proof took {} steps'.format(max(list(steps.values()))))

         
