from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import folium
import os

app = Flask(__name__)

coordenadas_bairros = {
    "Kobrasol": [-27.5917, -48.6135],
    "Campinas": [-27.5936, -48.6123],
    "Barreiros": [-27.5808, -48.6118],
    "Forquilhinhas": [-27.6045, -48.6228],
    "Ingleses": [-27.4372, -48.3992],
    "Trindade": [-27.5868, -48.5207],
    "Estreito": [-27.5898, -48.5786],
    "Capoeiras": [-27.6002, -48.5891],
    "Coqueiros": [-27.6034, -48.5906],
    "Centro": [-27.5954, -48.5480],
    "Ipiranga": [-27.6097, -48.6293],
    "Areias": [-27.6041, -48.6317],
    "Jardim Atlântico": [-27.5798, -48.5936],
    "Rio Tavares": [-27.6500, -48.4770],
    "Canasvieiras": [-27.4309, -48.4607],
}

@app.route("/", methods=["GET", "POST"])
def home():

    tabela = None
    tabela_sexo = None
    mapa_html = None

    if request.method == "POST":

        arquivo = request.files["arquivo"]

        if arquivo:

            df = pd.read_excel(arquivo, engine="openpyxl")

            df["Sexo"] = df["Sexo"].astype(str).str.strip()
            df["Região onde mora"] = (
                df["Região onde mora"]
                .astype(str)
                .str.strip()
            )

            tabela = df.to_html(
                classes="table table-striped",
                index=False
            )

            tabela_sexo_df = (
                df["Sexo"]
                .value_counts()
                .reset_index()
            )

            tabela_sexo_df.columns = [
                "Sexo",
                "Quantidade"
            ]

            tabela_sexo = tabela_sexo_df.to_html(
            classes="table table-striped tabela-sexo",
            index=False
            )
            fig, ax = plt.subplots()

            ax.bar(
                tabela_sexo_df["Sexo"],
                tabela_sexo_df["Quantidade"]
            )

            ax.set_title("Quantidade por Sexo")
            ax.set_xlabel("Sexo")
            ax.set_ylabel("Quantidade")

            plt.tight_layout()

            os.makedirs("static", exist_ok=True)

            plt.savefig("static/grafico.png")
            plt.close()

            mapa = folium.Map(
                location=[-27.5954, -48.5480],
                zoom_start=11
            )

            for _, aluno in df.iterrows():

                bairro = aluno["Região onde mora"]

                if bairro in coordenadas_bairros:

                    lat, lon = coordenadas_bairros[bairro]

                    folium.Marker(
                        [lat, lon],
                        popup=f"""
                        <b>{aluno['Nome']}</b><br>
                        Turma: {aluno['Turma']}<br>
                        Bairro: {bairro}
                        """
                    ).add_to(mapa)

            mapa_html = mapa._repr_html_()

    return render_template(
        "index.html",
        tabela=tabela,
        tabela_sexo=tabela_sexo,
        mapa_html=mapa_html
    )
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
