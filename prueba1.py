import pandas as pd
import random

# --- Cargar Excel sin encabezados ---
df = pd.read_excel(
    r"C:\Users\usuario\Downloads\peliculas_relacionadas_muchisimas.xlsx",
    header=None
)

# Columna 0 = Película, Columna 1 = Relacionadas
df["Relacionadas"] = df[1].apply(lambda x: [p.strip() for p in str(x).split(",")])

def obtener_relacionadas(pelicula):
    """Devuelve todas las películas relacionadas con la que elige el usuario."""
    if pelicula in df[0].values:
        fila = df[df[0] == pelicula].iloc[0]
        return fila["Relacionadas"]
    else:
        return []

# --- Interactivo ---
print("🎬 Bienvenido al recomendador de películas 🎬\n")

peliculas_elegidas = []
todas_relacionadas = []

# El usuario elige 5 películas
for i in range(5):
    pelicula = input(f"Elige la película #{i+1}: ").strip()
    peliculas_elegidas.append(pelicula)

    relacionadas = obtener_relacionadas(pelicula)
    if relacionadas:
        todas_relacionadas.append(relacionadas)
        print(f"   👉 Relacionadas con '{pelicula}': {relacionadas}")
    else:
        print(f"   ⚠️ '{pelicula}' no está en la base de datos.")

# --- Buscar coincidencias ---
if todas_relacionadas:
    # Unir todas las listas en una sola
    todas = [p for sublist in todas_relacionadas for p in sublist]

    # Contar repeticiones
    coincidencias = [p for p in todas if todas.count(p) > 1]

    # Quitar las películas que eligió el usuario
    coincidencias = [p for p in coincidencias if p not in peliculas_elegidas]

    if coincidencias:
        recomendacion_final = random.choice(coincidencias)
        print("\n✨ Coincidencias encontradas ✨")
        print(set(coincidencias))
        print(f"\n🎯 Recomendación final para ti: {recomendacion_final}")
    else:
        print("\n⚠️ No hubo coincidencias entre las recomendaciones.")
else:
    print("\n⚠️ No se pudieron generar recomendaciones.")
