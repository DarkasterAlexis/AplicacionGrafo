import tkinter as tk
from tkinter import ttk,filedialog,simpledialog,messagebox
from algoritmos import dfs, bfs, kruskal, prim
import copy
from cod_grafo import grafo_server
from vista_de_dibujo import dibujar_grafo 
import csv, json
from tkinter import font as tkfont
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame

#Inicializar el mezclador de sonidos
pygame.mixer.init()

sonido_hover = pygame.mixer.Sound("sounds/hover.wav")
sonido_click = pygame.mixer.Sound("sounds/click.wav")

#Copia del grafo original yy estructura del historial
grafo_original = copy.deepcopy(grafo_server)

# ---------------- GLOBALS ----------------
historial = []
botones = []
boton_activo = None
ultimo_resultado = {}

# ---------------- FUNCIONES AUXILIARES ----------------
def elegir_inicio(grafo, preferencia='A'):
    if not grafo:
        return None
    if preferencia in grafo:
        return preferencia
    return next(iter(grafo))

def elegir_destino_bfs(grafo, preferencia='G', inicio=None):
    if not grafo:
        return None
    if preferencia in grafo:
        return preferencia
    keys = list(grafo.keys())
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
    recorrido = dfs(grafo_server, inicio)
    ultimo_resultado = {"DFS": recorrido, "inicio": inicio}
    actualizar_texto(f"DFS desde {inicio}: {recorrido}\n¿Existe camino {inicio}→G?: {'G' in recorrido}")
    dibujar_grafo(p_frame, grafo_server, titulo="Resultados con el\nAlgoritmo DFS")

def mostrar_bfs():
    global ultimo_resultado
    if not grafo_server:
        actualizar_texto("El grafo está vacío, no se puede ejecutar BFS.")
        return
    inicio = elegir_inicio(grafo_server, 'A')
    destino = elegir_destino_bfs(grafo_server, 'G', inicio)
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
    ultimo_resultado = {"Kruskal": mst, "Costo": costo}
    resultado = f"MST: {mst}\nCosto mínimo: {costo}"
    actualizar_texto(resultado)
    dibujar_grafo(p_frame, grafo_server, mst=mst, titulo="Resultados con el \nAlgoritmo KRUSKAL" )
    
def mostrar_prim():
    global ultimo_resultado
    if not grafo_server:
        actualizar_texto("El grafo está vacío, no se puede ejecutar Prim.")
        return
    inicio = elegir_inicio(grafo_server, 'A')
    mst, costo = prim(grafo_server, inicio)
    ultimo_resultado = {"Prim": mst, "Costo": costo, "inicio": inicio}
    resultado = f"Prim desde {inicio}: {mst}\nCosto mínimo: {costo}"
    actualizar_texto(resultado)
    dibujar_grafo(p_frame, grafo_server, mst=mst, titulo="Resultados con el \nAlgoritmo PRIM" )

def actualizar_texto(texto, fg="orange"):
    salida_canvas.delete("texto_resultado")
    salida_canvas.create_text(
        salida_canvas.winfo_width() // 2,     # centro X
        salida_canvas.winfo_height() // 2,    # centro Y
        text=texto,
        fill=fg,
        font=("Bookman Old Style", 18),
        width=salida_canvas.winfo_width() - 80,  # ajusta para que el texto no se salga
        tags="texto_resultado",
        anchor="center",
        justify="center"
    )

def saliPprograma():
    ventana.quit()
    ventana.destroy()

def centra_ventana(win, ancho=400, alto=200):
    win.update_idletasks()
    ancho_ventana = ancho
    alto_ventana = alto
    x = (win.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y = (win.winfo_screenheight() // 2) - (alto_ventana // 2)
    win.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

def elimina_nodo():
    global grafo_server

    if not grafo_server:
        actualizar_texto("El grafo está vacío, no se puede eliminar un nodo.")
        return

    def confirmar(event=None):
        nodo = entry.get()
        if nodo in grafo_server:
            del grafo_server[nodo]
            for k in grafo_server:
                if nodo in grafo_server[k]:
                    del grafo_server[k][nodo]
            actualizar_texto(f"Nodo '{nodo}' eliminado correctamente.")
            dibujar_grafo(p_frame, grafo_server, titulo="Grafo actualizado")
        else:
            actualizar_texto(f"El nodo '{nodo}' no existe en el grafo.")
        ventana_popup.destroy()

    def cancelar():
        ventana_popup.destroy()

    ventana_popup = tk.Toplevel(ventana)
    ventana_popup.title("Eliminar Nodo")
    ventana_popup.configure(bg="#2c2f33")  # Color de fondo
    ventana_popup.geometry("400x200")  # Tamaño de ventana
    ventana_popup.resizable(False, False)
    
    centra_ventana(ventana_popup,ancho=400,alto=200)

    label = tk.Label(ventana_popup, text="Ingrese el nodo a eliminar:", 
                     bg="#2c2f33", fg="white", font=("Arial", 14))
    label.pack(pady=20)

    entry = tk.Entry(ventana_popup, font=("Arial", 14), width=20)
    entry.pack(pady=10)
    entry.focus_set()
    historial.append(copy.deepcopy(grafo_server))
    frame_botones = tk.Frame(ventana_popup, bg="#2c2f33")
    frame_botones.pack(pady=10)

    btn_ok = tk.Button(frame_botones, text="OK", bg="#4CAF50", fg="white", 
                       font=("Arial", 12, "bold"), width=10, command=confirmar)
    btn_ok.pack(side=tk.LEFT, padx=10)

    btn_cancelar = tk.Button(frame_botones, text="Cancelar", bg="#f44336", fg="white", 
                             font=("Arial", 12, "bold"), width=10, command=cancelar)
    btn_cancelar.pack(side=tk.LEFT, padx=10)
    
    ventana_popup.bind("<Return>",confirmar)

    ventana_popup.transient(ventana)  # Para que la ventana sea modal
    ventana_popup.grab_set()
    ventana.wait_window(ventana_popup)

def exportar_texto_actual():
    if not ultimo_resultado:
        actualizar_texto("No hay resultados para exportar.")
        return

    def exportar(formato):
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{formato}",
            filetypes=[(f"{formato.upper()} files", f"*.{formato}"), ("All files", "*.*")],
        )
        if not filename:
            return

        try:
            if formato == "csv":
                with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    for clave, valor in ultimo_resultado.items():
                        writer.writerow([clave, valor])
            elif formato == "json":
                with open(filename, "w", encoding="utf-8") as jsonfile:
                    json.dump(ultimo_resultado, jsonfile, ensure_ascii=False, indent=4)
            actualizar_texto(f"Resultados exportados correctamente a {filename}")
        except Exception as e:
            actualizar_texto(f"Error al exportar: {str(e)}")
        ventana_popup.destroy()

    def cancelar():
        ventana_popup.destroy()
        
    def on_enter(event,color):
        event.widget['background'] = color
    
    def on_leave(event,color_original):
        event.widget['background'] = color_original

    ventana_popup = tk.Toplevel(ventana)
    ventana_popup.title("Exportar Resultados")
    ventana_popup.configure(bg="#2c2f33")
    ventana_popup.resizable(False, False)

    centra_ventana(ventana_popup, ancho=400, alto=220)

    label = tk.Label(ventana_popup, text="Selecciona el formato de exportación:",
                     bg="#2c2f33", fg="white", font=("Arial", 14))
    label.pack(pady=20)

    frame_botones = tk.Frame(ventana_popup, bg="#2c2f33")
    frame_botones.pack(pady=10)

    color_csv= "#2196F3"
    color_csv_hover = "#1769aa"
    btn_csv = tk.Button(frame_botones, text="CSV", bg=color_csv, fg="white",
                        font=("Arial", 12, "bold"), width=10,
                        command=lambda: exportar("csv"))
    btn_csv.pack(side=tk.LEFT, padx=10)
    btn_csv.bind("<Enter>",lambda e: on_enter(e, color_csv_hover))
    btn_csv.bind("<Leave>",lambda e: on_leave(e, color_csv))

    color_json="#FF9800"
    color_json_hover="#e67c00"
    btn_json = tk.Button(frame_botones, text="JSON", bg=color_json, fg="darkblue",
                         font=("Arial", 12, "bold"), width=10,
                         command=lambda: exportar("json"))
    btn_json.pack(side=tk.LEFT, padx=10)
    btn_json.bind("<Enter>",lambda e: on_enter(e,color_json_hover))
    btn_json.bind("<Leave>",lambda e: on_leave(e,color_json))

    color_cancelar= "#f44336"
    color_cancelar_hover="#d32f2f"
    btn_cancelar = tk.Button(ventana_popup, text="Cancelar", bg=color_cancelar, fg="white",
                              font=("Arial", 12, "bold"), width=15, command=cancelar)
    btn_cancelar.pack(pady=15)
    btn_cancelar.bind("<Enter>",lambda e: on_enter(e, color_cancelar_hover))
    btn_cancelar.bind("<Leave>",lambda e: on_leave(e, color_cancelar))

    ventana_popup.bind("<Return>", lambda e: exportar("csv"))  # Enter por defecto exporta CSV

    ventana_popup.transient(ventana)
    ventana_popup.grab_set()
    ventana.wait_window(ventana_popup)
    
def actualizar_canvas():
    """Redibuja el grafo en el área p_frame"""
    dibujar_grafo(p_frame, grafo_server, titulo="Grafo Actualizado")

def reiniciar_grafo():
    global grafo_server, historial
    grafo_server = copy.deepcopy(grafo_original)
    historial.clear()
    actualizar_canvas()
    messagebox.showinfo("Reiniciar", "El grafo ha vuelto a su estado original.")

def retroceder_accion():
    global grafo_server, historial
    if historial:
        grafo_server = historial.pop()
        actualizar_canvas()
        messagebox.showinfo("Retroceder", "Se deshizo la última acción.")
    else:
        messagebox.showwarning("Retroceder", "No hay acciones para deshacer.")

# -------- FUNCIONES PARA BORDES --------
def resaltar_boton_activo(btn, color):
    global boton_activo
    for b in botones:
        b.itemconfig(b.octagono_id, outline=b.borde_color, width=3)
        b.activo = False
    btn.itemconfig(btn.octagono_id, outline=color, width=5)
    btn.activo = True
    boton_activo = btn
        
def crear_boton_octagonal(parent, text, command=None,bg="black", fg="lightblue",
    border_color="black",active_color="cyan",width=None, height=None, padx=20, pady=10):

    fuente = tkfont.Font(family="Bauhaus 93", size=18, weight="bold")
    text_width = fuente.measure(text)
    text_height = fuente.metrics("linespace")

    # Si no hay width/height definidos, calcular con padding
    if width is None:
        width = text_width + padx * 2
    if height is None:
        height = text_height + pady * 2

    offset = min(20, width // 6, height // 6)  # ajuste dinámico del corte
    canvas = tk.Canvas(parent, width=width, height=height, bg=bg, highlightthickness=0)

    # Puntos del octágono (basados en width y height)
    points = [
        offset, 0,
        width - offset, 0,
        width, offset,
        width, height - offset,
        width - offset, height,
        offset, height,
        0, height - offset,
        0, offset
    ]

    polygon = canvas.create_polygon(points, outline=border_color, fill=bg, width=2)

    # Texto centrado
    text_id = canvas.create_text(width // 2, height // 2, text=text, fill=fg, font=fuente)

    canvas.text_id = text_id
    canvas.default_fg = fg
    canvas.active_color = active_color

    # Hover
    def on_enter(event):
        canvas.itemconfig(polygon, outline=active_color, width=4)
        sonido_hover.play()
    def on_leave(event):
        if boton_activo != canvas:
            canvas.itemconfig(polygon, outline=border_color, width=2)
            canvas.itemconfig(text_id,fill=fg)
    def on_click(event):
        sonido_click.play()
        if command:
            command()
        marcar_boton_activo(canvas)

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_click)

    return canvas

def marcar_boton_activo(btn):
    global boton_activo
    for b in botones:
        try:
            if b != btn:  # solo resetear los que no son el actual
                b.itemconfig(b.text_id, fill=b.default_fg)
                b.itemconfig(b.find_all()[0], outline="black", width=2)  # resetear borde
        except tk.TclError:
            pass  # botón ya destruido
    try:
        # Marcar el activo
        btn.itemconfig(btn.text_id, fill=btn.active_color)
        btn.itemconfig(btn.find_all()[0], outline=btn.active_color, width=4)
        boton_activo = btn
    except tk.TclError:
        pass #boton destruido
   

def actualizar_texto_octagonal(canvas, texto, fg="orange",
                               font=("Bookman Old Style", 18)):
    # Elimina texto previo
    canvas.delete("texto_resultado")

    # Dibuja nuevo texto centrado dentro del canvas
    canvas.create_text(canvas.winfo_width()//2,
                       canvas.winfo_height()//2,
                       text=texto, fill=fg, font=font,
                       width=canvas.winfo_width()-80,  # ajuste para que el texto no se salga
                       tags="texto_resultado", anchor="center", justify="center")

# -------- SALIDA OCTOGONAL --------
def crear_texto_octagonal(parent, width=600, height=200,
                          border_color="orange", borde_ancho=4,
                          bg_octagono="black", fg="orange",
                          font=("Bookman Old Style", 18)):

    # Crear Canvas
    canvas = tk.Canvas(parent, width=width, height=height,
                       bg=bg_octagono, highlightthickness=0, bd=0)

    # Calcular puntos del octágono
    offset = min(40, width // 6, height // 6)
    points = [
        offset, 0,
        width - offset, 0,
        width, offset,
        width, height - offset,
        width - offset, height,
        offset, height,
        0, height - offset,
        0, offset
    ]

    # Dibujar octágono
    canvas.create_polygon(points, outline=border_color,
                          fill=bg_octagono, width=borde_ancho)

    # Retornar el canvas
    return canvas

#CREAR FRAME OCTOGONAL
def crear_frame_octagonal(parent, bg="black", border_color="cyan", borde_ancho=4):
    """
    Crea un Canvas que contiene un frame centrado y dibuja un borde octagonal
    alrededor (redibuja al cambiar tamaño). Asegura que el octágono quede
    DETRÁS del frame interno para que el contenido sea visible.
    Retorna (canvas, frame_interno).
    """
    canvas = tk.Canvas(parent, bg=bg, highlightthickness=0, bd=0)
    # Frame interno donde irá el grafo
    frame_interno = tk.Frame(canvas, bg=bg)
    # Crear window; lo posicionaremos luego en el centro
    frame_window = canvas.create_window(0, 0, window=frame_interno, anchor="nw")

    def redibujar_octagono(event=None):
        # Evitar dibujar cuando el canvas no tiene tamaño real
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w <= 10 or h <= 10:
            return

        # Borrar borde anterior y crear nuevo
        canvas.delete("borde")

        offset = min(40, max(6, w // 6), max(6, h // 6))  # ajuste dinámico y seguro
        points = [
            offset, 0,
            w - offset, 0,
            w, offset,
            w, h - offset,
            w - offset, h,
            offset, h,
            0, h - offset,
            0, offset
        ]

        # Dibujar el octágono; lo creamos con tag "borde"
        canvas.create_polygon(points, outline=border_color, fill=bg, width=borde_ancho, tags="borde")

        # Asegurarnos de que el borde quede DETRÁS de la ventana (frame_interno)
        try:
            canvas.tag_lower("borde", frame_window)
        except Exception:
            # Si falla, al menos bajar la etiqueta 'borde' a fondo
            canvas.tag_lower("borde")

        # Centrar el frame interno dentro del canvas
        canvas.coords(frame_window, w // 2, h // 2)
        canvas.itemconfig(frame_window, anchor="center")

    # Redibujar en cada cambio de tamaño
    canvas.bind("<Configure>", redibujar_octagono)

    # Forzar un primer redibujado una vez que el widget tenga tamaño
    # (ayuda si el canvas se crea con tamaño 1x1 inicialmente)
    canvas.update_idletasks()
    redibujar_octagono()

    return canvas, frame_interno

# ---------------- VENTANA PRINCIPAL ----------------
ventana = tk.Tk()
ventana.title("ANÁLISIS DE CONECTIVIDAD DE LA RED DE SERVIDORES")
ventana.state("zoomed")
ventana.configure(bg="black")

# ---------------- ESTILOS TTK ----------------
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton",font=("Bauhaus 93", 18, "bold"),padding=(40,30),
                background="black",foreground="lightblue",borderwidth=2,
                focusthickness=3,focuscolor="none",relief="flat")
style.map("TButton",
          background=[("active", "gray20")],
          relief=[("pressed", "groove"), ("!pressed", "flat")])

# Estilos con solo borde coloreado
style.configure("Blue.TButton", bordercolor="blue", focusthickness=4)
style.configure("Red.TButton", bordercolor="red", focusthickness=4)
style.configure("Yellow.TButton", bordercolor="yellow", focusthickness=4)
style.configure("Green.TButton", bordercolor="green", focusthickness=4)
style.configure("Hover.TButton", bordercolor="cyan", focusthickness=3)

# ---------------- FRAMES ----------------
frame_superior = tk.Frame(ventana, bg="black")
frame_superior.pack(pady=2)


frame_izq_sup = tk.Frame(frame_superior, bg="black")
frame_izq_sup.pack(side=tk.LEFT, padx=30)
conten_izq_sup = tk.Frame(frame_izq_sup, bg="black")
conten_izq_sup.pack(expand=True)

frame_izq = tk.Frame(ventana, bg="black")
frame_izq.pack(side=tk.LEFT, fill=tk.Y, expand=False,padx=30)
conten_izq = tk.Frame(frame_izq, bg="black")
conten_izq.pack(expand=True)

frame_centro_sal = tk.Frame(frame_superior,bg="black")
frame_centro_sal.pack(side=tk.LEFT)

frame_der_sup = tk.Frame(frame_superior, bg="black")
frame_der_sup.pack(side=tk.RIGHT, padx=30)
conten_der_sup = tk.Frame(frame_der_sup, bg="black")
conten_der_sup.pack(expand=True)

frame_der = tk.Frame(ventana, bg="black")
frame_der.pack(side=tk.RIGHT, fill=tk.Y, expand=False,padx=30)
conten_der = tk.Frame(frame_der, bg="black")
conten_der.pack(expand=True)

# ---------------- BOTONES ----------------
# === BOTONES IZQUIERDA ===
btn_retroceder = crear_boton_octagonal(conten_izq_sup, text="⮌ Deshacer Acción",command=retroceder_accion,
    width=400, height=100,bg="black", fg="lightblue",border_color="black", active_color="orange")

btn_dfs = crear_boton_octagonal(conten_izq, text="Recorrer RED",command=mostrar_dfs,
    width=400, height=100,bg="black", fg="lightblue",border_color="black", active_color="blue")

btn_bfs = crear_boton_octagonal(conten_izq, text="Calcular distancias mínimas",command=mostrar_bfs,
    width=400, height=100,bg="black", fg="lightblue",border_color="black", active_color="red")

btn_kruskal = crear_boton_octagonal(conten_izq, text="Árbol de Expansión mínima",command=mostrar_kruskal,
    width=400, height=100,bg="black", fg="lightblue",border_color="black", active_color="yellow")

btn_prim = crear_boton_octagonal(conten_izq, text="Comparar con Prim",command=mostrar_prim,
    width=400, height=100,bg="black", fg="lightblue",border_color="black", active_color="green")

# === BOTONES DERECHA ===
btn_reiniciar = crear_boton_octagonal(conten_der_sup, text="Reiniciar Grafo ↺",command=reiniciar_grafo,
    width=400, height=100,bg="black", fg="lightblue",border_color="black", active_color="yellow")

btn_exportar = crear_boton_octagonal(conten_der, text="Exportar Resultados",command=exportar_texto_actual,
    width=400, height=100,bg="black", fg="lightblue",border_color="black", active_color="blue")

btn_eliminar = crear_boton_octagonal(conten_der, text="Eliminar Nodo",command=elimina_nodo,
    width=400, height=100,bg="black", fg="lightblue",border_color="black", active_color="red")

btn_salida = crear_boton_octagonal(conten_der, text="EXIT",command=saliPprograma,
    width=400, height=100,bg="black", fg="lightblue",border_color="black", active_color="red")

# Empaquetar y centrar
for b in [btn_dfs, btn_bfs, btn_kruskal, btn_prim,btn_retroceder]:
    b.pack(pady=7)

for b in [btn_exportar, btn_eliminar, btn_salida,btn_reiniciar]:
    b.pack(pady=7)

botones = [btn_dfs, btn_bfs, btn_kruskal, btn_prim, btn_exportar, btn_eliminar, btn_salida,btn_retroceder,btn_reiniciar]

# ---------------- AREA DE SALIDA OCTOGONAL ----------------
# Crear área octagonal
salida_canvas = crear_texto_octagonal(
    frame_centro_sal, width=900, height=220,
    border_color="orange", borde_ancho=6,
    bg_octagono="black", fg="orange"
)
salida_canvas.pack(pady=10)

# -------- FRAME PARA GRAFOS --------
p_canvas, p_frame = crear_frame_octagonal(
    ventana, bg="black", border_color="cyan", borde_ancho=4
)
p_canvas.pack(pady=20, expand=True, fill="both")


ventana.mainloop()