from flask import Flask, render_template, request, session, redirect, url_for
import random
import os
from movies_db import peliculas_db
from series_db import series_db

app = Flask(__name__)
app.secret_key = "supersecreto"

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")

todas_peliculas = list(peliculas_db.keys())
todas_series = list(series_db.keys())

def obtener_relacionadas_pelicula(pelicula):
    return peliculas_db.get(pelicula, [])

def obtener_relacionadas_serie(serie):
    return series_db.get(serie, [])

# ── INDEX ──
@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

# ── PELÍCULAS ──
@app.route("/peliculas", methods=["GET", "POST"])
def peliculas():
    # Reiniciar sesión si venimos de "Elige otra película"
    if request.method == "GET" and request.args.get("reiniciar") == "1":
        session.clear()
        return redirect(url_for("peliculas"))

    # Inicializar variables de sesión
    if "ronda" not in session:
        session["ronda"] = 1
        session["elecciones"] = []
        session["todas_relacionadas"] = []

    # Registrar elección de usuario
    if request.method == "POST":
        eleccion = request.form.get("pelicula")
        if eleccion:
            session["elecciones"].append(eleccion)
            relacionadas = obtener_relacionadas_pelicula(eleccion)
            if relacionadas:
                session["todas_relacionadas"].append(relacionadas)
            session["ronda"] += 1

    # Fin de las 5 rondas: mostrar recomendación
    if session["ronda"] > 5:
        todas = [p for sublist in session["todas_relacionadas"] for p in sublist]
        todas = [p for p in todas if p not in session["elecciones"]]
        coincidencias = [p for p in set(todas) if todas.count(p) > 1]

        recomendacion = random.choice(coincidencias) if coincidencias else random.choice(todas) if todas else None

        return render_template(
            "resultado.html",
            seleccionadas=session["elecciones"],
            recomendacion=recomendacion,
            tmdb_key=TMDB_API_KEY,
            tipo="movie"
        )

    # Mostrar dos opciones distintas
    disponibles = list(set(todas_peliculas) - set(session["elecciones"]))
    opciones = random.sample(disponibles, 2)

    return render_template(
        "peliculas.html",
        pelicula1=opciones[0],
        pelicula2=opciones[1],
        ronda=session["ronda"],
        tmdb_key=TMDB_API_KEY
    )

# ── SERIES ──
@app.route("/series", methods=["GET", "POST"])
def series():
    # Reiniciar sesión si venimos de "Elige otra serie"
    if request.method == "GET" and request.args.get("reiniciar") == "1":
        session.clear()
        return redirect(url_for("series"))

    # Inicializar variables de sesión
    if "ronda" not in session:
        session["ronda"] = 1
        session["elecciones"] = []
        session["todas_relacionadas"] = []

    # Registrar elección de usuario
    if request.method == "POST":
        eleccion = request.form.get("pelicula")
        if eleccion:
            session["elecciones"].append(eleccion)
            relacionadas = obtener_relacionadas_serie(eleccion)
            if relacionadas:
                session["todas_relacionadas"].append(relacionadas)
            session["ronda"] += 1

    # Fin de las 5 rondas: mostrar recomendación
    if session["ronda"] > 5:
        todas = [p for sublist in session["todas_relacionadas"] for p in sublist]
        todas = [p for p in todas if p not in session["elecciones"]]
        coincidencias = [p for p in set(todas) if todas.count(p) > 1]

        recomendacion = random.choice(coincidencias) if coincidencias else random.choice(todas) if todas else None

        return render_template(
            "resultado.html",
            seleccionadas=session["elecciones"],
            recomendacion=recomendacion,
            tmdb_key=TMDB_API_KEY,
            tipo="tv"
        )

    # Mostrar dos opciones distintas
    disponibles = list(set(todas_series) - set(session["elecciones"]))
    opciones = random.sample(disponibles, 2)

    return render_template(
        "series.html",
        serie1=opciones[0],
        serie2=opciones[1],
        ronda=session["ronda"],
        tmdb_key=TMDB_API_KEY
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
