import pandas as pd #Libreria para leer archivos xlsx

def cargar_datos_xls(ruta_archivo):
    df = pd.read_excel(ruta_archivo)
    
    actividades = []
    
    # Recorrer filas del archivo XLS y extraer columnas relevantes
    for index, row in df.iterrows():
        codigo_inscripcion = row['Código de inscripción']
        nombre = row['Nombre']
        fecha_inicio = row['Fecha de inicio']
        fecha_fin = row['Fecha de fin']
        antecedentes = row['Antecedentes']
        
        # Guardar cada actividad con sus antecedentes
        actividades.append({
            "codigo_inscripcion": codigo_inscripcion,
            "nombre": nombre,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "antecedentes": antecedentes,
        })
    
    return actividades