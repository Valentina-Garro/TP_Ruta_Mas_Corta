import os
import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx

archivo = 'distancias.txt'

def cargar_grafo(desde_archivo):
    G = nx.Graph()
    try:
        with open(desde_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                ciudad1, ciudad2, distancia = linea.strip().split(',')
                distancia = int(distancia)
                G.add_edge(ciudad1.strip(), ciudad2.strip(), weight=distancia)
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se pudo encontrar el archivo {desde_archivo}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al leer el archivo: {e}")
    return G

G = cargar_grafo(archivo)

# Calcular ruta más corta
def calcular_ruta():
    origen = origen_combobox.get()
    destino = destino_combobox.get()

    if not origen or not destino:
        messagebox.showwarning("Advertencia", "Necesita seleccionar ciudades para origen y destino.")
        return
    if origen == destino:
        messagebox.showinfo("Ruta", "La ciudad de origen y destino es la misma.")
        return
    
    try:
        # Usando Dijkstra 
        ruta_corta = nx.dijkstra_path(G, origen, destino, weight="weight")
        distancia_total = nx.dijkstra_path_length(G, origen, destino, weight="weight")
        
        for item in ruta_tree.get_children():
            ruta_tree.delete(item)
        
        distancia_acumulada = 0
        for i, ciudad in enumerate(ruta_corta):
            if i > 0:
                distancia_acumulada += G[ruta_corta[i-1]][ciudad]['weight']
            ruta_tree.insert("", "end", values=(ciudad, distancia_acumulada))
        
    except nx.NetworkXNoPath:
        messagebox.showerror("Error", "No hay una ruta disponible.")

# Configurar la ventana 
root = tk.Tk()
root.title("RUTA MÁS CORTA.")
root.geometry("650x500")

frame_superior = tk.Frame(root)
frame_superior.pack(pady=10, fill="x")

# Tabla de las ciudades
ciudades_frame = tk.Frame(frame_superior)
ciudades_frame.pack(side="left", padx=10)
ciudades_tree = ttk.Treeview(ciudades_frame, columns=("Nombre"), show="headings", height=8)
ciudades_tree.heading("Nombre", text="Nombre")
ciudades_tree.column("Nombre", width=120, anchor="center")
##
ciudades_scroll = ttk.Scrollbar(ciudades_frame, orient="vertical", command=ciudades_tree.yview)
ciudades_tree.configure(yscroll=ciudades_scroll.set)
ciudades_tree.pack(side="left")

# Llenar tabla ciudades
ciudades_unicas = list(set(G.nodes))
for ciudad in ciudades_unicas:
    ciudades_tree.insert("", "end", values=(ciudad,))

# Tabla de distancias
distancias_frame = tk.Frame(frame_superior)
distancias_frame.pack(side="left", padx=10, pady=10)
distancias_tree = ttk.Treeview(frame_superior, columns=("Nodo 1", "Nodo 2", "Valor"), show="headings", height=6)
distancias_tree.heading("Nodo 1", text="Nodo 1")
distancias_tree.heading("Nodo 2", text="Nodo 2")
distancias_tree.heading("Valor", text="Valor")
distancias_tree.column("Nodo 1", width=120, anchor="center")
distancias_tree.column("Nodo 2", width=120, anchor="center")
distancias_tree.column("Valor", width=90, anchor="center")

###
distancias_scrollbar = ttk.Scrollbar(frame_superior, orient="vertical", command=distancias_tree.yview)
distancias_tree.configure(yscroll=distancias_scrollbar.set)
distancias_scrollbar.pack(side="right", fill="y")
distancias_tree.pack(side="left", fill="both", expand=True)
##

# Llenar tabla distancias
for ciudad1, ciudad2, datos in G.edges(data=True):
    distancias_tree.insert("", "end", values=(ciudad1, ciudad2, datos["weight"]))

# Selección de origen y destino
frame_inferior = tk.Frame(root)
frame_inferior.pack(pady=10)

tk.Label(frame_inferior, text="Origen").grid(row=0, column=0, padx=5, pady=5)
origen_combobox = ttk.Combobox(frame_inferior, values=ciudades_unicas, width=15, state="readonly")
origen_combobox.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inferior, text="Destino").grid(row=1, column=0, padx=5, pady=5)
destino_combobox = ttk.Combobox(frame_inferior, values=ciudades_unicas, width=15, state="readonly")
destino_combobox.grid(row=1, column=1, padx=5, pady=5)

ruta_button = tk.Button(frame_inferior, text="Calcular", command=calcular_ruta)
ruta_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Tabla para ruta más corta y la distancia 
ruta_tree = ttk.Treeview(root, columns=("Nombre", "Valor"), show="headings", height=6)
ruta_tree.heading("Nombre", text="Nombre")
ruta_tree.heading("Valor", text="Valor")
ruta_tree.column("Nombre", width=120, anchor="center")
ruta_tree.column("Valor", width=80, anchor="center")
ruta_tree.pack(pady=10)

root.mainloop()
