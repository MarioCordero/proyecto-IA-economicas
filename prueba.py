import spacy
from geopy.geocoders import Nominatim

# Cargar el modelo de lenguaje en español de spaCy
nlp = spacy.load("es_core_news_md")

# Cargar el geolocalizador para ubicar distritos
geolocator = Nominatim(user_agent="geoapiExercises")

# Lista de distritos más pobres de Costa Rica (ejemplo)
distritos_pobres = ["Distrito 1", "Distrito 2", "Distrito 3"]

# Texto de ejemplo (este texto vendría del informe)
texto = """
    En el distrito de Distrito 1 se realizaron dos obras de teatro,
    mientras que en el Distrito 3 hubo una presentación de danza.
    Además, en el Distrito 2 se organizó un evento cultural.
"""

# Procesar el texto con spaCy
doc = nlp(texto)

# Extraer las actividades culturales y sus ubicaciones
actividades = []
for sent in doc.sents:
    actividades_encontradas = []
    distritos_encontrados = []
    for ent in sent.ents:
        if ent.label_ == "LOC":  # spaCy detecta ubicaciones
            distritos_encontrados.append(ent.text)
        if "teatro" in sent.text or "danza" in sent.text or "evento cultural" in sent.text:
            actividades_encontradas.append(sent.text)
    
    if distritos_encontrados and actividades_encontradas:
        for distrito in distritos_encontrados:
            if distrito in distritos_pobres:
                actividades.append((distrito, actividades_encontradas))

# Mostrar resultados
for distrito, actividad in actividades:
    print(f"En {distrito}, se realizaron las siguientes actividades culturales: {actividad}")