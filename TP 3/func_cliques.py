import networkx as nx

def S_in(G,C):
    edg = [e for e in G.edges() if (e[0] in C and e[1] in C)]
    S = 0
    for e in edg:
        S += G[e[0]][e[1]]['weight']
    return S

# No se si "links incident to nodes in C"
# hace referencia a pares de nodos con una
# pata afuera de C y otra adentro,
# o si tambien hay que tener en cuenta los
# edges contenidos completamente en C
# Vamos a suponer que debe haber una pata afuera
def S_tot(G,C):
    edg = [e for e in G.edges() if len([x for x in e if x in C])==1]
    S = 0
    for e in edg:
        S += G[e[0]][e[1]]['weight']
    return S

# x: nodo, G: grafo
def k_i(x,G):
    return sum(G[e[0]][e[1]]['weight'] for e in G.neighbors(x))


# x: nodo, G: grafo, C: cluster
def k_iin(x,G,C):
    K = set(G.neighbors(x)).intersection(set(C))
    k = 0
    for x in K:
        k += G[k][x]['weight']
    return k


# varmod calcula la variacion dQ al
# mover el nodo x al cluster C
def dq(x,G,C):
    if x in C:
        return 0
    else:
    	m = sum(G[e[0]][e[1]]['weight'] for e in G.edges())
    	a = (S_in(G,C)+k_iin(x,G,C))/(2*m) - ((S_tot(G,C)+k_i(x,G))/(2*m))**2
    	b = S_in(G,C)/(2*m) -(S_tot(G,C)/(2*m))**2 -(k_i(x,G)/(2*m))**2
    	dQ = a-b
    	return dQ