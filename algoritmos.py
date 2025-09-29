import heapq

from collections import deque

def dfs(grafo, inicio, visitados=None):
    if visitados is None:
        visitados = []
    visitados.append(inicio)
    for vecino in grafo[inicio]:
        if vecino not in visitados:
            dfs(grafo, vecino, visitados)
    return visitados

def bfs(grafo, inicio, objetivo):
    visitados = set([inicio])
    cola = deque([(inicio, [inicio])])
    while cola:
        nodo, camino = cola.popleft()
        if nodo == objetivo:
            return camino
        for vecino in grafo[nodo]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino]))
    return None

def kruskal(grafo):
    aristas = []
    for u in grafo:
        for v, w in grafo[u].items():
            if (v, u, w) not in aristas:
                aristas.append((u, v, w))
    aristas.sort(key=lambda x: x[2])  

    padre = {n: n for n in grafo}

    def encontrar(n):
        if padre[n] != n:
            padre[n] = encontrar(padre[n])
        return padre[n]

    def unir(u, v):
        ru, rv = encontrar(u), encontrar(v)
        if ru != rv:
            padre[rv] = ru
            return True
        return False

    mst = []
    costo = 0
    for u, v, w in aristas:
        if unir(u, v):
            mst.append((u, v, w))
            costo += w
    return mst, costo

def prim(grafo,inicio='A'):
    if inicio is None:
        inicio = list(grafo.keys())[0]
    
    visitados = set([inicio])
    aristas=[]
    mst = []
    costo=0
    
    for vecino,peso in grafo[inicio].items():
        heapq.heappush(aristas,(peso, inicio, vecino))
        
    while aristas and len(mst) < len(grafo)-1:
        peso,u,v =heapq.heappop(aristas)
        if v not in visitados:
            visitados.add(v)
            mst.append((u,v,peso))
            costo += peso
            
            for vecino, w in grafo[v].items():
                if vecino not in visitados:
                    heapq.heappush(aristas,(w, v,vecino ))
    return mst, costo 
    