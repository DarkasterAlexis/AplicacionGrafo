import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def dibujar_grafo(p_frame, grafo, camino=None, mst=None, titulo="Grafo de Servidores"):
    fig, ax = plt.subplots(figsize=(5,4))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("skyblue")
    
    G = nx.Graph()
    for u in grafo:
        for v, w in grafo[u].items():
            G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)

    nx.draw_networkx_nodes(G, pos, node_size=600, node_color="lightsteelblue", ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold", ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color="dimgray", ax=ax)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)

    if camino:
        edges_camino = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges_camino, edge_color="red", width=4, ax=ax)

    if mst:
        edges_mst = [(u, v) for u, v, _ in mst]
        nx.draw_networkx_edges(G, pos, edgelist=edges_mst, edge_color="lime", width=4, ax=ax)
        
    ax.set_title(titulo, fontweight="bold", fontsize="19", color="orange")
    ax.axis("off")
    
    for widget in p_frame.winfo_children():
        widget.destroy()
        
    cv = FigureCanvasTkAgg(fig,master=p_frame)
    cv.draw()
    cv.get_tk_widget().pack(fill="both",expand=True)
    plt.close(fig)
