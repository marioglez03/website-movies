from flask import Flask, render_template, request, session
import pandas as pd
import random
import os
from dotenv import load_dotenv

# --- Cargar variables de entorno desde .env si existe ---
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecreto")  # usar variable de entorno en producción
tmdb_api_key = os.environ.get("TMDB_API_KEY")  # leer API key de TMDB desde variable de entorno

# --- Cargar Excel relativo al proyecto ---
excel_path = os.path.join(os.path.dirname(__file__), "peliculas_relacionadas_muchisimas.xlsx")
df = pd.read_excel(excel_path, header=None)

# Crear lista de relacionadas
df["Relacionadas"] = df[1].apply(lambda x: [p.strip() for p in str(x).split(",")])
todas_peliculas = df[0].tolist()

def obtener_relacionadas(pelicula):
    """Devuelve todas las películas relacionadas con la que elige el usuario."""
    if pelicula in df[0].values:
        fila = df[df[0] == pelicula].iloc[0]
        return fila["Relacionadas"]
    return []

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/peliculas", methods=["GET", "POST"])
def peliculas():
    if "ronda" not in session:
        session["ronda"] = 1
        session["elecciones"] = []
        session["todas_relacionadas"] = []

    if request.method == "POST":
        eleccion = request.form.get("pelicula")
        if eleccion:
            session["elecciones"].append(eleccion)
            relacionadas = obtener_relacionadas(eleccion)
            if relacionadas:
                session["todas_relacionadas"].append(relacionadas)
            session["ronda"] += 1

    # Si ya se completaron 5 rondas, calcular recomendación
    if session["ronda"] > 5:
        todas = [p for sublist in session["todas_relacionadas"] for p in sublist]
        todas = [p for p in todas if p not in session["elecciones"]]

        # Buscar coincidencias
        coincidencias = [p for p in set(todas) if todas.count(p) > 1]

        if coincidencias:
            recomendacion = random.choice(coincidencias)
        else:
            recomendacion = random.choice(todas) if todas else None

        return render_template(
            "resultado.html",
            seleccionadas=session["elecciones"],
            recomendacion=recomendacion,
            tmdb_api_key=tmdb_api_key
        )

    # Mostrar 2 películas aleatorias para esta ronda
    disponibles = list(set(todas_peliculas) - set(session["elecciones"]))
    opciones = random.sample(disponibles, min(2, len(disponibles)))

    return render_template(
        "peliculas.html",
        pelicula1=opciones[0],
        pelicula2=opciones[1],
        ronda=session["ronda"]
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True  # Cambiar a False en producción
    )
