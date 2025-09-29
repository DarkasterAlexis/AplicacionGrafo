import tkinter as tk
from algoritmos import dfs, bfs, kruskal,prim
from cod_grafo import grafo_server
from vista_de_dibujo import dibujar_grafo
from tkinter import filedialog
import csv
import json

botones = []
boton_activo = None

def elegir_inicio(grafo, preferencia='A'):
    """Devuelve un nodo de inicio: preferencia si existe, si no el primer nodo disponible."""
    if not grafo:
        return None
    if preferencia in grafo:
        return preferencia
    return next(iter(grafo))  # primer nodo según orden de inserción

def elegir_destino_bfs(grafo, preferencia='G', inicio=None):
    """Devuelve un destino para BFS: preferencia si existe, si no el último nodo distinto del inicio."""
    if not grafo:
        return None
    if preferencia in grafo:
        return preferencia
    keys = list(grafo.keys())
    # intenta devolver el último distinto del inicio
    for k in reversed(keys):
        if k != inicio:
            return k
    return keys[0] 

def mostrar_dfs():
    global ultimo_resultado
    if not grafo_server:
        actualizar_texto("El grafo está vacío, no se puede ejecutar DFS.")
        return
    inicio = elegir_inicio(grafo_server, 'A')
    if inicio is None:
        actualizar_texto("No hay nodos en el grafo para ejecutar DFS.")
        return
    recorrido = dfs(grafo_server, inicio)
    ultimo_resultado = {"DFS":recorrido,"inicio":inicio}
    actualizar_texto(f"DFS desde {inicio}: {recorrido}\n¿Existe camino {inicio}→G?: {'G' in recorrido}")
    dibujar_grafo(p_frame, grafo_server, titulo="Resultados con el\nAlgoritmo DFS")

def mostrar_bfs():
    global ultimo_resultado
    if not grafo_server:
        actualizar_texto("El grafo está vacío, no se puede ejecutar BFS.")
        return
    inicio = elegir_inicio(grafo_server, 'A')
    destino = elegir_destino_bfs(grafo_server, 'G', inicio)
    if inicio is None or destino is None:
        actualizar_texto("No hay nodos suficientes para ejecutar BFS.")
        return
    # si inicio == destino, camino trivial
    if inicio == destino:
        camino = [inicio]
    else:
        camino = bfs(grafo_server, inicio, destino)
    ultimo_resultado = {"BFS": camino, "inicio": inicio, "destino": destino}
    if camino:
        resultado = f"BFS desde {inicio} hasta {destino}: {camino}\nSaltos: {len(camino)-1}"
    else:
        resultado = f"No existe camino {inicio}→{destino}"
    actualizar_texto(resultado)
    dibujar_grafo(p_frame, grafo_server, camino=camino, titulo="Resultados con el \nAlgoritmo BFS")

def mostrar_kruskal():
    global ultimo_resultado
    mst, costo = kruskal(grafo_server)
    ultimo_resultado = {"Kruskal":mst,"Costo":costo}
    resultado = f"MST: {mst}\nCosto mínimo: {costo}"
    actualizar_texto(resultado)
    dibujar_grafo(p_frame, grafo_server, mst=mst, titulo="Resultados con el \nAlgoritmo KRUSKAL" )
    
def mostrar_prim():
    global ultimo_resultado
    if not grafo_server:
        actualizar_texto("El grafo está vacío, no se puede ejecutar Prim.")
        return
    inicio = elegir_inicio(grafo_server, 'A')
    if inicio is None:
        actualizar_texto("No hay nodos en el grafo para ejecutar Prim.")
        return
    mst, costo=prim(grafo_server,inicio)
    ultimo_resultado = {"Prim":mst,"Costo":costo,"inicio":inicio}
    resultado = F"Prim desde {inicio}: {mst}\nCosto mínimo: {costo}"
    actualizar_texto(resultado)
    dibujar_grafo(p_frame, grafo_server, mst=mst, titulo="Resultados con el \nAlgoritmo PRIM" )
    
def resaltar_boton_activo(btn_active,color):
    global boton_activo
    for btn in botones:
        btn.config(highlightthickness=0)
    btn_active.config(highlightthickness=4,highlightbackground=color,highlightcolor=color)
    boton_activo = btn_active

def resaltar_borde(event):
    if event.widget != boton_activo:
        event.widget.config(highlightthickness=2, highlightbackground="cyan",highlightcolor="cyan")
    
def quitar_resaltado(event):
    if event.widget != boton_activo:
        event.widget.config(highlightthickness=0)

def actualizar_texto(texto):
    salida_texto.config(state="normal")
    salida_texto.delete(1.0, tk.END)
    salida_texto.insert(tk.END, texto)
    salida_texto.config(state="disabled")
    
def saliPprograma():
    ventana.quit()
    ventana.destroy()

ventana = tk.Tk()
ventana.title("ANALISIS DE CONECTIVIDAD DE LA RED DE SERVIDORES ")
ventana.geometry("500x400")
ventana.state("zoomed")
ventana.configure(bg="black")

def centro_ventana(top):
    top.update_idletasks()
    w = top.winfo_width()
    h = top.winfo_height()
    ws = top.winfo_screenwidth()
    hs = top.winfo_screenheight()
    x = (ws // 2)-(w // 2)
    y = (hs // 2)-(h // 2)
    top.geometry(f"{w}x{h}+{x}+{y}")

def elimina_nodo():
    top = tk.Toplevel(ventana, bg="darkviolet")
    top.title("Eliminar Nodo")  
    tk.Label(top, text="Ingrese el Nodo a eliminar:  ",font=("Arial",12),
             bg="violet",fg="#0B3D91").pack(pady=5)
    entry = tk.Entry(top,font=("Arial",12),bg="yellow",
                     fg="darkblue",insertbackground="red",  
                     highlightthickness=2,highlightbackground="gray", 
                     highlightcolor="green")
    entry.pack(pady=10)
     
    def confirmar():
        nodo = entry.get().strip()
        if nodo in grafo_server:
            grafo_server.pop(nodo)
            for vecin in grafo_server.values():
                if nodo in vecin:
                    vecin.pop(nodo)
            actualizar_texto(f"El nodo {nodo} se ha eliminado correctamente.")
            dibujar_grafo(p_frame, grafo_server, titulo=f"Grafo actualizado (sin {nodo})")
            top.destroy()
        else: 
            actualizar_texto(f"El nodo '{nodo}' no existe en el grafo. ")
            top.destroy()
    btn_confirmar= tk.Button(top, text="Confirmar", command=confirmar, bg="red",fg="white",
              font=("Arial", 10, "bold"),width=12,height=4 )
    btn_confirmar.pack(pady=10,ipadx=10,ipady=5)
    
    top.bind("<Return>",lambda e: btn_confirmar.invoke())
    entry.bind("<Return>",lambda e: btn_confirmar.invoke())
    entry.focus()
    top.geometry("300x130")
    top.resizable(False,False)
    centro_ventana(top)
    
def exportar_texto_actual():
    global ultimo_resultado
    try:
        if not ultimo_resultado:
            actualizar_texto("No hay resultados para exportar.")
            return
    except NameError:
        actualizar_texto("No hay resultados para exportar.")
        return

    # Ventana emergente para elegir formato
    top = tk.Toplevel(ventana,bg="maroon")
    top.title("Elegir formato")
    top.geometry("300x180")
    top.resizable(False, False)
    top.lift()
    top.attributes("-topmost", True)
    top.focus_force()
    top.attributes("-topmost", False)
    centro_ventana(top)

    tk.Label(top, text="Seleccione el formato de exportación:", font=("Arial", 12,"bold"),bg="lightcoral").pack(pady=10)

    def guardar_csv():
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if ruta:
            with open(ruta, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                for k, v in ultimo_resultado.items():
                    writer.writerow([k, v])
            actualizar_texto(f"Resultados exportados a CSV: {ruta}")
        top.destroy()

    def guardar_json():
        ruta = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if ruta:
            with open(ruta, "w", encoding="utf-8") as file:
                json.dump(ultimo_resultado, file, indent=4)
            actualizar_texto(f"Resultados exportados a JSON: {ruta}")
        top.destroy()

    tk.Button(top, text="CSV", command=guardar_csv, font=("Bauhaus 93", 13,"bold"),width=10,height=2, bg="orange", fg="darkblue").pack(pady=5)
    tk.Button(top, text="JSON", command=guardar_json, font=("Bauhaus 93", 13,"bold"),width=10,height=2, bg="purple", fg="white").pack(pady=5)
    
frame_izq = tk.Frame(ventana,bg="black",highlightthickness=0,borderwidth=0)
frame_izq.pack(side=tk.LEFT,fill=tk.Y,expand=False)
frame_izq.grid_rowconfigure(0, weight=1)
frame_izq.grid_rowconfigure(2, weight=1)
frame_der = tk.Frame(ventana,bg="black",highlightthickness=0,borderwidth=0)
frame_der.pack(side=tk.RIGHT,fill=tk.Y,expand=False)
frame_der.grid_rowconfigure(0, weight=1)
frame_der.grid_rowconfigure(2, weight=1)

conten_izq = tk.Frame(frame_izq, bg="black")
conten_izq.grid(row=1, column=0)
conten_der = tk.Frame(frame_der, bg="black")
conten_der.grid(row=1, column=0)


btn_dfs = tk.Button(
    conten_izq, text="Recorrer RED",
    relief="solid",bd=2,
    highlightthickness=0,highlightbackground="black",
    command=lambda: [mostrar_dfs(),resaltar_boton_activo(btn_dfs,"blue")], 
    width=30,height=3, bg="black",fg="lightblue",
    font=("Bauhaus 93",18,"bold"))
btn_bfs = tk.Button(
    conten_izq, text="Calcular distancia minimas",
    relief="solid",bd=2,
    command=lambda: [mostrar_bfs(),resaltar_boton_activo(btn_bfs,"red")], 
    width=30,height=3, bg="black",fg="lightblue",    font=("Bauhaus 93",18,"bold"),
    highlightthickness=0,highlightbackground="black")
btn_kruskal = tk.Button(
    conten_izq, text="Árbol de Expansión minima",
    relief="solid",bd=2,    
    command=lambda: [mostrar_kruskal(),resaltar_boton_activo(btn_kruskal,"yellow")], 
    width=30,height=3, bg="black",fg="lightblue",    
    font=("Bauhaus 93",18,"bold"),
    highlightthickness=0,highlightbackground="black")
btn_prim = tk.Button(
    conten_izq, text="Comparar con Prim",
    relief="solid",bd=2,
    command=lambda: [mostrar_prim(),resaltar_boton_activo(btn_prim,"green")],
    width=30,height=3,bg="black",fg="lightblue",
    font=("Bauhaus 93",18,"bold"),
    highlightthickness=0,highlightbackground="black")
btn_salida = tk.Button(
    conten_der, text="EXIT",
    relief="solid",bd=2,
    command=saliPprograma,
    width=30,height=3, bg="black",fg="lightblue",   font=("Bauhaus 93",18,"bold"),
    highlightthickness=0,highlightbackground="black")
btn_eliminar = tk.Button(
    conten_der, text="Eliminar Nodo",
    relief="solid",bd=2,
    command=elimina_nodo,
    width=30,height=3,bg="black",fg="lightblue",
    font=("Bauhaus 93",18,"bold"),
    highlightthickness=0,highlightbackground="black")
btn_exportar = tk.Button(
    conten_der, text="Exportar Resultados",
    relief="solid",bd=2,
    command=lambda: [exportar_texto_actual(),resaltar_boton_activo(btn_dfs,"blue")], 
    width=30,height=3,bg="black",fg="lightblue",
    font=("Bauhaus 93",18,"bold"),
    highlightthickness=0,highlightbackground="black")

btn_dfs.pack(pady=0)
btn_bfs.pack(pady=0)
btn_kruskal.pack(pady=0)
btn_exportar.pack(pady=0)
btn_eliminar.pack(pady=0)
btn_prim.pack(pady=0)
btn_salida.pack(pady=0)

botones=[btn_dfs,btn_bfs,btn_kruskal,btn_prim,btn_eliminar,btn_exportar,btn_salida]

for btn in botones:
    btn.bind("<Enter>", resaltar_borde)
    btn.bind("<Leave>", quitar_resaltado)

salida_texto = tk.Text(
    ventana, wrap="word", height=5, width=70, state="disabled", 
    font=("Bookman Old Style",18),bg="gray25",fg="darkblue",
    relief="flat", borderwidth=2)
salida_texto.pack(pady=10)

p_frame = tk.Frame(ventana, bg="black",highlightthickness=0,borderwidth=0)
p_frame.pack(fill="both", expand=True)

ventana.mainloop()
