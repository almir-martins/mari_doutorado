"""
API Flask para disponibilizar análises via web
Exemplo de como hospedar as análises em um servidor
"""

from flask import Flask, jsonify, send_file, request
import pandas as pd
import os
from pathlib import Path
from io import BytesIO
import matplotlib

matplotlib.use("Agg")  # Backend sem GUI para servidor

from config import CAMINHO_2022, CAMINHO_2023, CAMINHO_2024
from utils import configurar_ambiente, carrega_dados, preparar_dataframe
from analise_urgenza import (
    estatisticas_urgenza,
    analise_urgenza_subgrupo,
    analise_urgenza_idade,
)
from analise_geral import (
    analise_dimissione,
    analise_problema_principal,
    relatorio_geral,
)

app = Flask(__name__)

# Variável global para cachear dados (evitar recarregar sempre)
_df_cache = None


def obter_dados():
    """Obtém dados com cache"""
    global _df_cache

    if _df_cache is None:
        print("Carregando dados...")
        configurar_ambiente()

        df_2022 = carrega_dados(CAMINHO_2022)
        df_2023 = carrega_dados(CAMINHO_2023)
        df_2024 = carrega_dados(CAMINHO_2024)

        df_raw = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)
        _df_cache = preparar_dataframe(df_raw)
        print(f"Dados carregados: {len(_df_cache)} registros")

    return _df_cache


@app.route("/")
def home():
    """Página inicial com informações da API"""
    return jsonify(
        {
            "api": "Análise Mari Doutorado",
            "versao": "1.0",
            "endpoints": {
                "/status": "Status e informações básicas",
                "/analise/urgenza": "Estatísticas de Categoria Urgenza",
                "/analise/dimissione": "Estatísticas de Modalità Dimissione",
                "/analise/problemas": "Top problemas principais",
                "/analise/resumo": "Resumo geral",
                "/dados/total": "Total de registros",
                "/dados/periodo": "Período dos dados",
            },
        }
    )


@app.route("/status")
def status():
    """Status da API e dados carregados"""
    try:
        df = obter_dados()
        return jsonify(
            {
                "status": "online",
                "registros_carregados": len(df),
                "pacientes_unicos": int(df["Paziente"].nunique()),
                "periodo_inicio": df["Data Accesso"].min().strftime("%Y-%m-%d"),
                "periodo_fim": df["Data Accesso"].max().strftime("%Y-%m-%d"),
                "colunas": list(df.columns),
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/analise/urgenza")
def analise_urgenza_endpoint():
    """Retorna estatísticas de Categoria Urgenza"""
    try:
        df = obter_dados()

        urgenza_counts = df["Categoria Urgenza"].value_counts().to_dict()
        urgenza_perc = (
            (df["Categoria Urgenza"].value_counts(normalize=True) * 100)
            .round(2)
            .to_dict()
        )

        # Análise por subgrupo
        urgenza_subgrupo = pd.crosstab(
            df["Categoria Urgenza"], df["Sottogruppo Pazienti"]
        ).to_dict()

        return jsonify(
            {
                "status": "success",
                "distribuicao": {
                    "contagem": urgenza_counts,
                    "percentual": urgenza_perc,
                },
                "por_subgrupo": urgenza_subgrupo,
                "total_atendimentos": len(df),
                "pacientes_unicos": int(df["Paziente"].nunique()),
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/analise/dimissione")
def analise_dimissione_endpoint():
    """Retorna estatísticas de Modalità Dimissione"""
    try:
        df = obter_dados()

        dimissione_counts = df["Modalità Dimissione"].value_counts().to_dict()
        dimissione_perc = (
            (df["Modalità Dimissione"].value_counts(normalize=True) * 100)
            .round(2)
            .to_dict()
        )

        return jsonify(
            {
                "status": "success",
                "distribuicao": {
                    "contagem": dimissione_counts,
                    "percentual": dimissione_perc,
                },
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/analise/problemas")
def analise_problemas_endpoint():
    """Retorna top problemas principais"""
    try:
        df = obter_dados()
        top_n = request.args.get("top", default=10, type=int)

        problema_counts = df["Problema Principale"].value_counts().head(top_n).to_dict()
        problema_perc = (
            (df["Problema Principale"].value_counts(normalize=True) * 100)
            .head(top_n)
            .round(2)
            .to_dict()
        )

        return jsonify(
            {
                "status": "success",
                "top_problemas": {
                    "contagem": problema_counts,
                    "percentual": problema_perc,
                },
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/analise/resumo")
def resumo_endpoint():
    """Retorna resumo geral das análises"""
    try:
        df = obter_dados()

        # Categoria urgenza predominante
        cat_urgenza = df["Categoria Urgenza"].value_counts()

        # Subgrupos
        subgrupos = df["Sottogruppo Pazienti"].value_counts()

        # Faixas etárias
        faixas = df["Fascia d'età"].value_counts()

        resumo = {
            "status": "success",
            "dados_gerais": {
                "total_atendimentos": len(df),
                "pacientes_unicos": int(df["Paziente"].nunique()),
                "media_atendimentos_paciente": round(
                    len(df) / df["Paziente"].nunique(), 2
                ),
                "periodo_inicio": df["Data Accesso"].min().strftime("%Y-%m-%d"),
                "periodo_fim": df["Data Accesso"].max().strftime("%Y-%m-%d"),
            },
            "categoria_urgenza": {
                "predominante": cat_urgenza.idxmax(),
                "contagem": int(cat_urgenza.max()),
                "percentual": round(cat_urgenza.max() / len(df) * 100, 2),
            },
            "subgrupos": subgrupos.to_dict(),
            "faixas_etarias": faixas.to_dict(),
        }

        return jsonify(resumo)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/dados/filtrar")
def filtrar_dados():
    """
    Filtra dados por parâmetros
    Exemplo: /dados/filtrar?categoria=Verde&ano=2023
    """
    try:
        df = obter_dados()

        # Aplicar filtros
        if "categoria" in request.args:
            categoria = request.args["categoria"]
            df = df[df["Categoria Urgenza"] == categoria]

        if "ano" in request.args:
            ano = int(request.args["ano"])
            df = df[df["Data Accesso"].dt.year == ano]

        if "subgrupo" in request.args:
            subgrupo = request.args["subgrupo"]
            df = df[df["Sottogruppo Pazienti"] == subgrupo]

        return jsonify(
            {
                "status": "success",
                "filtros_aplicados": dict(request.args),
                "registros_encontrados": len(df),
                "pacientes_unicos": int(df["Paziente"].nunique()),
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/dados/exportar/<formato>")
def exportar_dados(formato):
    """
    Exporta dados filtrados
    Formatos: csv, json, excel
    """
    try:
        df = obter_dados()

        # Aplicar filtros se houver
        if "categoria" in request.args:
            categoria = request.args["categoria"]
            df = df[df["Categoria Urgenza"] == categoria]

        # Preparar exportação
        if formato == "csv":
            output = BytesIO()
            df.to_csv(output, index=False, encoding="utf-8")
            output.seek(0)
            return send_file(
                output,
                mimetype="text/csv",
                as_attachment=True,
                download_name="dados_analise.csv",
            )

        elif formato == "json":
            return jsonify(
                {
                    "status": "success",
                    "dados": df.to_dict(orient="records")[
                        :1000
                    ],  # Limitar a 1000 registros
                }
            )

        elif formato == "excel":
            output = BytesIO()
            df.to_excel(output, index=False, engine="openpyxl")
            output.seek(0)
            return send_file(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment=True,
                download_name="dados_analise.xlsx",
            )

        else:
            return (
                jsonify(
                    {"status": "error", "message": f"Formato não suportado: {formato}"}
                ),
                400,
            )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/recarregar")
def recarregar_dados():
    """Força recarregamento dos dados"""
    global _df_cache
    _df_cache = None

    df = obter_dados()

    return jsonify(
        {
            "status": "success",
            "message": "Dados recarregados com sucesso",
            "registros": len(df),
        }
    )


if __name__ == "__main__":
    # Configuração para desenvolvimento
    app.run(host="0.0.0.0", port=5000, debug=True)

    # Para produção, use um servidor WSGI como Gunicorn:
    # gunicorn -w 4 -b 0.0.0.0:5000 app:app
