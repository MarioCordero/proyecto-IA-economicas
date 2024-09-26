import fileManager
import indicadores
import pandas as pd #Libreria para leer archivos xlsx
import userInterface


def main():
    # Clase "controladora"

    ruta_archivo = ""  # Usa una raw string para evitar problemas con las barras invertidas
    ucr_bite = True

    if(ucr_bite) :
        userInterface.initializeUI(ruta_archivo)
        df = pd.read_excel(ruta_archivo, skiprows=6)
        # Iterar sobre las filas y columnas a partir de la fila 7
        for index, row in df.iterrows():
            codigo_inscripcion = row['Código de inscripción']
            nombre = row['Nombre']
            fecha_inicio = row['Fecha de inicio']
            fecha_fin = row['Fecha de fin']
            antecedentes = row['Antecedentes']

    # actividades = cargar_datos_xls(ruta_archivo)


    # Imprimir los nombres de las columnas
    print(df.columns)

    # Procesar las actividades
    # for actividad in actividades:
    #     antecedentes = actividad['antecedentes']
        
    #     # Determinar el origen de la actividad
    #     origen = determinar_origen(antecedentes)
        
    #     # Calcular el indicador de pertinencia
    #     pertinencia = indicador_pertinencia(origen)
        
    #     # Mostrar resultados
    #     print(f"Actividad: {actividad['nombre']}")
    #     print(f"Origen: {origen}")
    #     print(f"Pertinencia: {pertinencia}\n")

if __name__ == "__main__":
    main()