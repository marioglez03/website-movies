from flask import Flask, render_template, request, session
import random
from movies_db import peliculas_db

app = Flask(__name__)
app.secret_key = "supersecreto"

todas_peliculas = list(peliculas_db.keys())


def obtener_relacionadas(pelicula):
    return peliculas_db.get(pelicula, [])


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


    if session["ronda"] > 5:

        todas = [p for sublist in session["todas_relacionadas"] for p in sublist]

        todas = [p for p in todas if p not in session["elecciones"]]

        coincidencias = [p for p in set(todas) if todas.count(p) > 1]

        if coincidencias:
            recomendacion = random.choice(coincidencias)
        else:
            recomendacion = random.choice(todas) if todas else None

        return render_template(
            "resultado.html",
            seleccionadas=session["elecciones"],
            recomendacion=recomendacion
        )


    disponibles = list(set(todas_peliculas) - set(session["elecciones"]))

    opciones = random.sample(disponibles, 2)

    return render_template(
        "peliculas.html",
        pelicula1=opciones[0],
        pelicula2=opciones[1],
        ronda=session["ronda"]
    )


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
