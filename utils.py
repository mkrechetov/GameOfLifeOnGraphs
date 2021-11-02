import numpy as np
import networkx as nx
import itertools

def next_vertex_state(J, state, alive_rule=1, dead_rule=1):
    n = len(J)
    alive = state.copy()
    dead = list(set(range(n)).difference(set(alive)))

    if len(alive) == 0:
        return alive
    else:
        new_alive = []
        new_dead = []

        for node in range(n):
            neighbors_alive = sum([J[node][i] for i in alive])
            neighbors_dead = sum([J[node][i] for i in dead])

            if (neighbors_alive >= alive_rule) and (neighbors_dead >= dead_rule):
                new_alive.append(node)
            else:
                new_dead.append(node)
        
        return new_alive

def next_value_state(J, values, all_states):    
	
	new_values = []
	for node in range(len(J)):
		neighbors = [values[other] for other in all_states[node]]
		new_values.append(sum(neighbors))#/len(neighbors)
	for node in range(len(J)):
		values[node] += new_values[node]
	for node in range(len(J)):
		values[node] /= sum(values)#[node]

def dist(a, b):
    if len(a) != len(b):
        return np.inf
    else:
        d = 0
        for i in range(len(a)):
            d += np.abs(a[i]-b[i])
        return d

def testing(G, H, max_iter=100):
	JG = nx.adjacency_matrix(G).todense().tolist()
	JH = nx.adjacency_matrix(H).todense().tolist()
	
	statesG = [[node] for node in list(G.nodes())]
	all_statesG = [statesG]
	
	statesH = [[node] for node in list(H.nodes())]
	all_statesH = [statesH]

	for i in range(max_iter):
		new_stateG = []
		new_stateH = []
		for node in list(G.nodes()):
			new_stateG.append(next_vertex_state(JG, all_statesG[-1][node]))
			new_stateH.append(next_vertex_state(JH, all_statesH[-1][node]))
		all_statesG.append(new_stateG)
		all_statesH.append(new_stateH)
		#print("iter {} states for G are: {}".format(i, all_statesG[-1]))
		#print("iter {} states for H are: {}".format(i, all_statesH[-1]))		


	valuesG = [1 for _ in list(G.nodes())]
	valuesH = [1 for _ in list(H.nodes())]

	for i in range(max_iter):
		next_value_state(JG, valuesG, all_statesG[i])
		next_value_state(JH, valuesH, all_statesH[i])
		#print("iter {} vals for G are: {}".format(i, valuesG))
		#print("iter {} vals for H are: {}".format(i, valuesH))

		if dist(valuesG, valuesH) != 0:
		    #print("G and H are not isomorphic. Verified in {} steps".format(i+1))
		    return i+1
		    
		#print("Seems that G and H are isomorphic. Verified in {} steps".format(max_iter))
	return max_iter

def distance(G, H, max_iter=100):
	JG = nx.adjacency_matrix(G).todense().tolist()
	JH = nx.adjacency_matrix(H).todense().tolist()

	
	statesG = [[node] for node in list(G.nodes())]
	all_statesG = [statesG]
	
	statesH = [[node] for node in list(H.nodes())]
	all_statesH = [statesH]

	for i in range(max_iter):
		new_stateG = []
		new_stateH = []
		for node in list(G.nodes()):
			new_stateG.append(next_vertex_state(JG, all_statesG[-1][node]))
			new_stateH.append(next_vertex_state(JH, all_statesH[-1][node]))
		all_statesG.append(new_stateG)
		all_statesH.append(new_stateH)

	valuesG = [1 for _ in list(G.nodes())]
	valuesH = [1 for _ in list(H.nodes())]

	for i in range(max_iter):
		next_value_state(JG, valuesG, all_statesG[i])
		next_value_state(JH, valuesH, all_statesH[i])

	return dist(valuesG, valuesH)
	    

def features(G, max_iter=10, dim=1):
	JG = nx.adjacency_matrix(G).todense().tolist()


	statesG = [[node] for node in list(G.nodes())]
	all_statesG = [statesG]

	for i in range(max_iter):
		new_stateG = []
		for node in list(G.nodes()):
			new_stateG.append(next_vertex_state(JG, all_statesG[-1][node]))
		all_statesG.append(new_stateG)

	valuesG = [1 for _ in list(G.nodes())]
	f = sorted(valuesG)[-dim:]

	for i in range(max_iter):
		next_value_state(JG, valuesG, all_statesG[i])
		f+= sorted(valuesG)[-dim:]
		#f.append(min(valuesG))		
		#f.append(max(valuesG))

	return f


def if_blink(G):
	J = nx.adjacency_matrix(G).todense().tolist()
	states = {}
	for node in list(G.nodes()):
		states[node] = [set([node])]
	
	total_length = len(J)
	while total_length != 0:
		total_length = 0

		for node in list(G.nodes()):
			next_node_state = set(next_vertex_state(J, list(states[node][-1])))
			total_length += len(next_node_state)
			if next_node_state in states[node]:
				return True
			else:
				states[node].append(next_node_state)
	return False	

def depth(G):
	J = nx.adjacency_matrix(G).todense().tolist()
	states = {}
	for node in list(G.nodes()):
		states[node] = [set([node])]
	
	depth = [1 for node in list(G.nodes())]
	at_least_one_new = True
	while at_least_one_new:
		at_least_one_new = False
		
		for node in list(G.nodes()):
			next_node_state = set(next_vertex_state(J, list(states[node][-1])))
			
			if next_node_state in states[node]:
				pass
			else:
				at_least_one_new = True
				depth[node] += 1
			states[node].append(next_node_state)

	return depth	

def depth_features(G, k=1):
	J = nx.adjacency_matrix(G).todense().tolist()
	combs = [list(itertools.combinations(list(range(len(J))), d)) for d in range(1, k+1)]
	depths = []

	for comb in combs:
		states = {}
		for node_tuple in comb:
			states[node_tuple] = [set(node_tuple)]
		
		depth = {}
		for node_tuple in comb:
			depth[node_tuple] = 1

		at_least_one_new = True
		while at_least_one_new:
			at_least_one_new = False
			
			for node_tuple in comb:
				next_node_state = set(next_vertex_state(J, list(states[node_tuple][-1])))
				
				if next_node_state in states[node_tuple]:
					pass
				else:
					at_least_one_new = True
					depth[node_tuple] += 1
				states[node_tuple].append(next_node_state)

		depths += sorted(list(depth.values()))
	return depths	


def get_states(G, max_iter=10):
	JG = nx.adjacency_matrix(G).todense().tolist()
	statesG = [[node] for node in list(G.nodes())]
	all_statesG = [statesG]

	for i in range(max_iter):
		new_stateG = []
		for node in list(G.nodes()):
			new_stateG.append(next_vertex_state(JG, all_statesG[-1][node]))
		all_statesG.append(new_stateG)

	return all_statesG
		    
