import tkinter as tk
from tkinter import messagebox
import serial
import time
import threading

arduino_port = "COM3" 
baud_rate = 9600
arduino = None

def conectar():
    global arduino
    try:
        arduino = serial.Serial(arduino_port, baud_rate)
        time.sleep(2)
        lbConection.config(text="Estado: Conectado", fg="green")
        messagebox.showinfo("Conexión", "Conexión establecida.")
        start_reading()
    except serial.SerialException:
        messagebox.showerror("Error", "No se pudo conectar al Arduino. Verifique la conexión.")
        
def desconectar():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        lbConection.config(text="Estado: Desconectado", fg="red")
        messagebox.showinfo("Conexión", "Conexión terminada.")
    else:
        messagebox.showwarning("Advertencia", "No hay una conexión activa.")
        
def enviar_limite():
    global arduino
    if arduino and arduino.is_open:
        try:
            limite = tbLimitTemp.get()
            if limite.isdigit():
                arduino.write(f"{limite}\n".encode())
                messagebox.showinfo("Enviado", f"Límite de temperatura ({limite}°C) enviado.")
            else:
                messagebox.showerror("Error", "Ingrese un valor numérico para el límite.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el límite: {e}")
    else:
        messagebox.showwarning("Advertencia", "Conecte al Arduino antes de enviar el límite.")
        
def read_from_arduino():
    global arduino
    while arduino and arduino.is_open:
        try:
            data = arduino.readline().decode().strip()
            if "Temperatura" in data:
                temp_value = data.split(":")[1].strip().split(" ")[0]
                lbTemp.config(text=f"{temp_value} °C")
                time.sleep(1)
        except Exception as e:
            print(f"Error Leyendo datos: {e}")
            break
        
def start_reading():
    thread = threading.Thread(target=read_from_arduino)
    thread.daemon = True
    thread.start()

# Interfaz gráfica
root = tk.Tk()
root.title("Monitoreo de Temperatura")
root.geometry("350x350")

# Etiqueta de título de temperatura
lbTitleTemp = tk.Label(root, text="Temperatura Actual", font=("Arial", 12))
lbTitleTemp.pack()

# Etiqueta para mostrar la temperatura
lbTemp = tk.Label(root, text="-- °C", font=("Arial", 24))
lbTemp.pack()

# Etiqueta de estado de conexión
lbConection = tk.Label(root, text="Estado: Desconectado", fg="red", font=("Arial", 10))
lbConection.pack(pady=5)

# Entrada para el límite de temperatura
lbLimitTemp = tk.Label(root, text="Límite de Temperatura:")
lbLimitTemp.pack(pady=5)
tbLimitTemp = tk.Entry(root, width=10)
tbLimitTemp.pack(pady=5)

# Botón para enviar el límite de temperatura
btnEnviar = tk.Button(root, text="Enviar Límite", command=enviar_limite, font=("Arial", 10))
btnEnviar.pack(pady=5)

# Botón de Conectar
btnConectar = tk.Button(root, text="Conectar", command=conectar, font=("Arial", 10))
btnConectar.pack(pady=5)

# Botón de Desconectar
btnDesconectar = tk.Button(root, text="Desconectar", command=desconectar, font=("Arial", 10))
btnDesconectar.pack(pady=5)

# Ejecuta la interfaz
root.mainloop()
