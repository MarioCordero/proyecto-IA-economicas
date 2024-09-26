def determinar_origen(antecedente):
    """
    Determina el origen de la propuesta según el antecedente.
    """
    if "docente" in antecedente.lower() or "estudiante" in antecedente.lower():
        return "Propuesto por la Universidad"
    elif "institución" in antecedente.lower() or "grupo" in antecedente.lower() or "solicitud" in antecedente.lower():
        return "Solicitado por una Entidad Externa"
    else:
        return "Origen Desconocido"

def indicador_pertinencia(origen):
    """
    Calcula el indicador de pertinencia. Si fue solicitado por una entidad externa,
    se considera pertinente.
    """
    if origen == "Solicitado por una Entidad Externa":
        return "Pertinente"
    else:
        return "No Pertinente"