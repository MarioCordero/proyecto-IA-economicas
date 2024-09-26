import pandas as pd #Libreria para leer archivos xlsx

def seleccionar_archivo(ventana, callback):
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*"))
    )
    if ruta_archivo:
        label_ruta.config(text=f"Archivo seleccionado: {ruta_archivo}")
        callback(ruta_archivo)  # Llama al callback con la ruta del archivo
        ventana.destroy()  # Cierra la ventana
    return ruta_archivo