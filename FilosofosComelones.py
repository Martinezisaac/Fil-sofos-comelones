# Programacion paralela y concurrente
# Mtro. Carlos Javier Cruz Franco

# Filosofos Comelones
    # Martinez Isaac
    # Lopez Ruvalcaba Erick 
    # Hernandez Lopez Diego
    # Hernandez Gutierrez Emmanuel

#Librerias
import threading
import concurrent.futures
import time
import random
import tkinter as tk
from tkinter import ttk

# Filosofos Comelones

# Un filosofo solamente tiene dos estados: comer y pensar
# Cuando un filosofo termina de comer, entonces procede a pensar
# Cuando el filosofo termina de pensar entonces quiere volver a comer
    # ¿Que pasa si el filosofo no obtiene los dos tenedores?
        # El filosofo entra en un estado de "Alerta", en donde no esta comiendo, ni tampoco pensando, si no que busca de manera constante obtener los dos tenedores 
        # para continuar con su siguiente estado, es decir, el filosofo quiere comer, y no dejara de tomar tenedores hasta que lo logre
    
    # ¿Como obtiene el filosofo ambos tenedores?
        # Un filosofo evalua primero un tenedor, ya sea el izquierdo el derecho, dependiendo de cual encuentre primero entonces lo agarra
        # Cuando ya agarro un tenedor, entonces se ejecuta un tiempo de reaccion para obtener el otro tenedor
        # Despues del tiempo de reaccion, si el tenedor faltante esta disponible
            # Si el tenedor faltante si esta disponible 
                # Toma el tenedor, por lo tanto ya tiene los dos tenedores
                # Por lo tanto ya puede comer
            # Si el tenedor faltante no esta disponible
                #Suelta el tenedor que ya habia agarrado

        # Si el filosofo pudo lograr obtener los tenedores, entonces come, piensa y repite el ciclo de buscar los tenedores
        # Si aun no ha logrado obtener los dos tenedores, repite el ciclo hasta que lo logre
        # Por cada ciclo el filosofo se espera un segundo antes de buscar el primer tenedor

# Cabe destacar que los tenedores son los recursos que estan disponible, estos se manejan como semafores que solamente pueden ser tomados 1 sola vez al mismo tiempo
# Por lo que un tenedor solo puede ser ocupado por un filosofo, los tenedores ya estan asignados a los filosofos que les corresponden de acuerdo al orden de la mesa
# en el que estan acomodados

# Filosofos Comelones

class Filosofos():
    def __init__(self, nombre, index, table, estados, contador_comer, contador_pensar):
        self.nombre = nombre  # Nombre del filosofo
        self.estado = "Pensando"  # Estado inicial del filosofo
        self.index = index  # Índice para la tabla gráfica
        self.table = table  # Referencia a la tabla gráfica
        self.estados = estados  # Lista para almacenar los estados
        self.contador_comer = contador_comer  # Contador de veces que ha comido
        self.contador_pensar = contador_pensar  # Contador de veces que ha pensado

    # Funciones para devolver el tiempo en función del estado
    def tiempoRevisarTenedor(self):  
        return random.uniform(0.5, 0.7)

    def tiempoPensar(self):  
        return random.uniform(5, 15) 

    def tiempoComer(self):  
        return random.uniform(3, 12)  

    # Método para actualizar la tabla gráfica con colores
    def actualizar_tabla(self, estado, color_tag):
        self.estado = estado
        self.estados[self.index] = estado  # Actualizar la lista de estados
        self.table.item(self.index, values=(self.nombre, self.estado, self.contador_comer[self.index], self.contador_pensar[self.index]))  # Actualizar la tabla visualmente
        self.table.item(self.index, tags=(color_tag,))  # Aplicar etiqueta de color

    # Método para actualizar log en la consola
    def actualizar_log(self, mensaje):
        print(f"{self.nombre}: {mensaje}")

    def revisarTenedores(self, tenedorIzq, tenedorDer, num_izq, num_der):
        while True: 
            self.actualizar_tabla("Revisando tenedores", "amarillo")
            self.actualizar_log("Revisando tenedores")

            if tenedorIzq.acquire(blocking=False):  
                self.actualizar_tabla(f"Tomó tenedor izquierdo (T{num_izq})", "naranja")
                self.actualizar_log(f"Tomó el tenedor izquierdo (T{num_izq})")

                tiempo = self.tiempoRevisarTenedor()  
                time.sleep(tiempo)

                if tenedorDer.acquire(blocking=False):
                    self.actualizar_tabla(f"Tomó ambos tenedores (T{num_izq} y T{num_der})", "verde")
                    self.actualizar_log(f"Tomó ambos tenedores (T{num_izq} y T{num_der})")
                    self.comer(tenedorIzq, tenedorDer)
                else:  
                    tenedorIzq.release()  
                    self.actualizar_tabla(f"Soltó tenedor izquierdo (T{num_izq})", "rojo")
                    self.actualizar_log(f"Soltó el tenedor izquierdo (T{num_izq})")

            elif tenedorDer.acquire(blocking=False):
                self.actualizar_tabla(f"Tomó tenedor derecho (T{num_der})", "naranja")
                self.actualizar_log(f"Tomó el tenedor derecho (T{num_der})")

                tiempo = self.tiempoRevisarTenedor()  
                time.sleep(tiempo)

                if tenedorIzq.acquire(blocking=False):  
                    self.actualizar_tabla(f"Tomó ambos tenedores (T{num_izq} y T{num_der})", "verde")
                    self.actualizar_log(f"Tomó ambos tenedores (T{num_izq} y T{num_der})")
                    self.comer(tenedorIzq, tenedorDer)
                else:  
                    tenedorDer.release()  
                    self.actualizar_tabla(f"Soltó tenedor derecho (T{num_der})", "rojo")
                    self.actualizar_log(f"Soltó el tenedor derecho (T{num_der})")

            time.sleep(1)

    def comer(self, tenedorIzq, tenedorDer): # El filosofo tiene la capacidad de pensar
        self.actualizar_tabla("Comiendo", "verde")
        self.actualizar_log("Está comiendo")
        
        # Incrementar el contador de veces que ha comido
        self.contador_comer[self.index] += 1
        self.table.item(self.index, values=(self.nombre, self.estado, self.contador_comer[self.index], self.contador_pensar[self.index]))
        
        tiempo = self.tiempoComer() # Obtener tiempo de comer
        time.sleep(tiempo) # El filosofo ejecuta si tiempo de comer
            
        self.pensar(tenedorIzq, tenedorDer)

    def pensar(self, tenedorIzq, tenedorDer): # El filosofo tiene la capacidad de pensar
        self.actualizar_tabla("Pensando", "azul")
        self.actualizar_log("Está pensando")
        
        # Incrementar el contador de veces que ha pensado
        self.contador_pensar[self.index] += 1
        self.table.item(self.index, values=(self.nombre, self.estado, self.contador_comer[self.index], self.contador_pensar[self.index]))

        tiempo = self.tiempoPensar() # Obtener tiempo de pensamiento 
        time.sleep(tiempo) #El filosofo ejecuta su tiempo de pensar 

        tenedorIzq.release() # Soltar el tenedor izquierdo
        tenedorDer.release() # Soltar el tenedor derecho


# Función para crear la interfaz gráfica
def crear_interfaz():
    root = tk.Tk()
    root.title("Filosofos Comelones")
    
    # Crear tabla
    table = ttk.Treeview(root, columns=("Nombre", "Estado", "Veces Comido", "Veces Pensado"), show='headings', height=5)
    table.heading("Nombre", text="Filósofo")
    table.heading("Estado", text="Estado")
    table.heading("Veces Comido", text="Veces Comido")
    table.heading("Veces Pensado", text="Veces Pensado")
    table.pack()

    # Agregar etiquetas de color
    table.tag_configure("amarillo", background="yellow")
    table.tag_configure("naranja", background="orange")
    table.tag_configure("verde", background="lightgreen")
    table.tag_configure("rojo", background="red")
    table.tag_configure("azul", background="lightblue")

    # Crear estados iniciales y agregar las filas
    estados = ["Pensando"] * 5
    contador_comer = [0] * 5
    contador_pensar = [0] * 5
    filosofos_nombres = ["Socrates", "Aristoteles", "Platon", "Rigoberto", "Juan"]
    for i, nombre in enumerate(filosofos_nombres):
        table.insert("", "end", iid=i, values=(nombre, "Pensando", 0, 0))

    return root, table, estados, contador_comer, contador_pensar #Devolver la tabla
# Definición de variables
tenedor1 = threading.Semaphore(1)  
tenedor2 = threading.Semaphore(1)  
tenedor3 = threading.Semaphore(1)  
tenedor4 = threading.Semaphore(1)  
tenedor5 = threading.Semaphore(1)  
# .acquire() #Aduñarse del tenedor | Bloquear el recurso 
# .release() #Dejar el tenedor libre | Desbloquear el recurso

# Iniciar la interfaz gráfica
root, table, estados, contador_comer, contador_pensar = crear_interfaz()

# Creación de objetos (5 filósofos comelones)
filosofo1 = Filosofos("Socrates", 0, table, estados, contador_comer, contador_pensar)
filosofo2 = Filosofos("Aristoteles", 1, table, estados, contador_comer, contador_pensar)
filosofo3 = Filosofos("Platon", 2, table, estados, contador_comer, contador_pensar)
filosofo4 = Filosofos("Rigoberto", 3, table, estados, contador_comer, contador_pensar)
filosofo5 = Filosofos("Juan", 4, table, estados, contador_comer, contador_pensar)

# Ejecución en threads
def iniciar_filosofos():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(filosofo1.revisarTenedores, tenedor5, tenedor1, 5, 1)
        executor.submit(filosofo2.revisarTenedores, tenedor1, tenedor2, 1, 2)
        executor.submit(filosofo3.revisarTenedores, tenedor2, tenedor3, 2, 3)
        executor.submit(filosofo4.revisarTenedores, tenedor3, tenedor4, 3, 4)
        executor.submit(filosofo5.revisarTenedores, tenedor4, tenedor5, 4, 5)

threading.Thread(target=iniciar_filosofos).start() # Iniciar los filósofos en segundo plano
root.mainloop() # Ejecutar la interfaz gráfica