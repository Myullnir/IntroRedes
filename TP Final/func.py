import igraph
import networkx as nx
import numpy as np

def clusterize(nx_Graph, method="infomap"):
    """
    Calcula el agrupamiento en comunidades de un grafo.
    
    In:
        nx_Graph: grafo de networkx
        method: metodo de clustering, puede ser: "infomap", "fastgreedy", "eigenvector", "louvain", "edge_betweenness","label_prop", "walktrap", ""
        
    Out:
        labels_dict: diccionario de nodo : a label al cluster al que pertenece.
    """
    if method == "edge_betweenness":
        nx_Graph = max(nx.connected_component_subgraphs(nx_Graph), key=len)#se queda con la componente más grande.
        print("AVISO: restringiendo a la componente connexa mas grade. De otro modo falla el algoritmo de deteccion de comunidades edge_betweenness.")
    
    isdirected = nx.is_directed(nx_Graph)
    np_adj_list = nx.to_numpy_matrix(nx_Graph)
    g = igraph.Graph.Weighted_Adjacency(np_adj_list.tolist(),mode=igraph.ADJ_UPPER)
   
    if method=="infomap":
        labels = g.community_infomap(edge_weights="weight").membership
    if method=="label_prop":
        labels = g.community_label_propagation(weights="weight").membership
    if method=="fastgreedy":
        labels = g.community_fastgreedy(weights="weight").as_clustering().membership
    if method=="eigenvector":
        labels = g.community_leading_eigenvector(weights="weight").membership
    if method=="louvain":
        labels = g.community_multilevel(weights="weight").membership
    if method=="edge_betweenness":
        labels = g.community_edge_betweenness(weights="weight", directed=isdirected).as_clustering().membership
    if method=="walktrap":
        labels = g.community_walktrap(weights="weight").as_clustering().membership
    
    label_dict = {node:label for node,label in zip(nx_Graph.nodes(), labels)}
    return label_dict


##################################################################
#cluster_nodos = {nro del cluster: [lista de nodos del cluster]}

# mem(x) = cluster que contiene a x
def mem(x,cluster_nodos):
    for c in cluster_nodos.keys():
        if x in cluster_nodos[c]:
            return c

# devuelve el valor de silhouette de x
def sil(x,G,cluster_nodos):
    cn = cluster_nodos
    c = mem(x,cn)
    a = np.mean([nx.shortest_path_length(G,x,y) for y in cn[c] if y!=x])
    b = min(min([nx.shortest_path_length(G,x,y) for y in cn[k]]) for k in cn.keys() if k!=c)
    return (b-a)/max(a,b)

