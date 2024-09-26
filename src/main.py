import fileManager
import indicadores

def main():
    # Cargar los datos del archivo XLS
    ruta_archivo = "../doc/Vigencias de proyecto.xlsx"  # Usa una raw string para evitar problemas con las barras invertidas
    # actividades = cargar_datos_xls(ruta_archivo)

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
