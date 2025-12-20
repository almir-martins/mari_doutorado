"""
Módulo de análises de Categoria Urgenza
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config import CORES_URGENZA, ORDEM_URGENZA


def estatisticas_urgenza(df):
    """
    Calcula estatísticas descritivas de Categoria Urgenza

    Args:
        df: DataFrame com coluna 'Categoria Urgenza'

    Returns:
        dict com estatísticas calculadas
    """
    urgenza_counts = df["Categoria Urgenza"].value_counts().sort_index()
    urgenza_perc = (
        df["Categoria Urgenza"].value_counts(normalize=True).sort_index() * 100
    )

    resumo = pd.DataFrame(
        {"Frequência": urgenza_counts, "Percentual (%)": urgenza_perc.round(2)}
    )

    print("=" * 80)
    print("ANÁLISE DE CATEGORIA URGENZA")
    print("=" * 80)
    print("\n1. DISTRIBUIÇÃO DE FREQUÊNCIAS")
    print("-" * 80)
    print(resumo)

    print(f"\nTotal de atendimentos: {len(df):,}")
    print(f"Total de pacientes únicos: {df['Paziente'].nunique():,}")

    print("\n2. ANÁLISE DETALHADA POR CATEGORIA")
    print("-" * 80)

    for categoria in urgenza_counts.index:
        qtd = urgenza_counts[categoria]
        perc = urgenza_perc[categoria]
        pacientes = df[df["Categoria Urgenza"] == categoria]["Paziente"].nunique()
        print(f"\n{categoria}:")
        print(f"  - Atendimentos: {qtd:,} ({perc:.2f}%)")
        print(f"  - Pacientes únicos: {pacientes:,}")

    return {"counts": urgenza_counts, "percentuais": urgenza_perc, "resumo": resumo}


def grafico_barras_urgenza(
    urgenza_counts, urgenza_perc, salvar=False, caminho_saida=None
):
    """
    Cria gráficos de barras de distribuição de Categoria Urgenza

    Args:
        urgenza_counts: Series com contagens por categoria
        urgenza_perc: Series com percentuais por categoria
        salvar: Se True, salva o gráfico
        caminho_saida: Caminho para salvar o gráfico
    """
    fig, axes = plt.subplots(1, 2, figsize=(24, 8))

    # Ordenar as categorias
    urgenza_ordenada = urgenza_counts.reindex(
        [cat for cat in ORDEM_URGENZA if cat in urgenza_counts.index]
    )
    urgenza_perc_ordenada = urgenza_perc.reindex(
        [cat for cat in ORDEM_URGENZA if cat in urgenza_perc.index]
    )

    # Gráfico 1: Frequência Absoluta
    ax1 = axes[0]
    bars1 = ax1.bar(
        range(len(urgenza_ordenada)),
        urgenza_ordenada.values,
        color=[CORES_URGENZA.get(cat, "#95A5A6") for cat in urgenza_ordenada.index],
        edgecolor="black",
        linewidth=1.5,
    )

    ax1.set_xlabel("Categoria de Urgenza", fontsize=16, fontweight="bold")
    ax1.set_ylabel("Frequência Absoluta", fontsize=16, fontweight="bold")
    ax1.set_title(
        "Distribuição de Atendimentos por Categoria de Urgenza",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )
    ax1.set_xticks(range(len(urgenza_ordenada)))
    ax1.set_xticklabels(urgenza_ordenada.index, fontsize=14)
    ax1.grid(axis="y", alpha=0.3, linestyle="--")

    # Adicionar valores nas barras
    for bar in bars1:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{int(height):,}",
            ha="center",
            va="bottom",
            fontsize=13,
            fontweight="bold",
        )

    # Gráfico 2: Percentual
    ax2 = axes[1]
    bars2 = ax2.bar(
        range(len(urgenza_perc_ordenada)),
        urgenza_perc_ordenada.values,
        color=[
            CORES_URGENZA.get(cat, "#95A5A6") for cat in urgenza_perc_ordenada.index
        ],
        edgecolor="black",
        linewidth=1.5,
    )

    ax2.set_xlabel("Categoria de Urgenza", fontsize=16, fontweight="bold")
    ax2.set_ylabel("Percentual (%)", fontsize=16, fontweight="bold")
    ax2.set_title(
        "Distribuição Percentual por Categoria de Urgenza",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )
    ax2.set_xticks(range(len(urgenza_perc_ordenada)))
    ax2.set_xticklabels(urgenza_perc_ordenada.index, fontsize=14)
    ax2.grid(axis="y", alpha=0.3, linestyle="--")

    # Adicionar valores nas barras
    for bar in bars2:
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.2f}%",
            ha="center",
            va="bottom",
            fontsize=13,
            fontweight="bold",
        )

    plt.tight_layout()

    if salvar and caminho_saida:
        plt.savefig(caminho_saida, dpi=300, bbox_inches="tight")

    plt.show()


def grafico_pizza_urgenza(urgenza_counts, salvar=False, caminho_saida=None):
    """
    Cria gráfico de pizza de Categoria Urgenza

    Args:
        urgenza_counts: Series com contagens por categoria
        salvar: Se True, salva o gráfico
        caminho_saida: Caminho para salvar o gráfico
    """
    fig, ax = plt.subplots(figsize=(14, 10))

    urgenza_ordenada = urgenza_counts.reindex(
        [cat for cat in ORDEM_URGENZA if cat in urgenza_counts.index]
    )

    colors_pie = [CORES_URGENZA.get(cat, "#95A5A6") for cat in urgenza_ordenada.index]

    wedges, texts, autotexts = ax.pie(
        urgenza_ordenada.values,
        labels=urgenza_ordenada.index,
        colors=colors_pie,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 14, "fontweight": "bold"},
        explode=[0.05] * len(urgenza_ordenada),
    )

    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(13)
        autotext.set_fontweight("bold")

    ax.set_title(
        "Distribuição Percentual de Categoria Urgenza",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )

    legend_labels = [
        f"{cat}: {urgenza_ordenada[cat]:,} atendimentos"
        for cat in urgenza_ordenada.index
    ]
    ax.legend(
        legend_labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=12
    )

    plt.tight_layout()

    if salvar and caminho_saida:
        plt.savefig(caminho_saida, dpi=300, bbox_inches="tight")

    plt.show()


def analise_urgenza_subgrupo(df):
    """
    Análise cruzada de Categoria Urgenza por Sottogruppo Pazienti

    Args:
        df: DataFrame com colunas necessárias

    Returns:
        dict com tabelas de análise cruzada
    """
    urgenza_subgrupo = pd.crosstab(
        df["Categoria Urgenza"],
        df["Sottogruppo Pazienti"],
        margins=True,
        margins_name="Total",
    )

    urgenza_subgrupo_perc = (
        pd.crosstab(
            df["Categoria Urgenza"], df["Sottogruppo Pazienti"], normalize="index"
        )
        * 100
    )

    print("\n3. TABELA CRUZADA: CATEGORIA URGENZA x SOTTOGRUPPO PAZIENTI")
    print("=" * 80)
    print(urgenza_subgrupo)

    print("\n4. PERCENTUAIS POR CATEGORIA DE URGENZA")
    print("=" * 80)
    print(urgenza_subgrupo_perc.round(2))

    return {"tabela": urgenza_subgrupo, "percentuais": urgenza_subgrupo_perc}


def heatmap_urgenza_subgrupo(df, salvar=False, caminho_saida=None):
    """
    Cria heatmap de Categoria Urgenza por Sottogruppo Pazienti

    Args:
        df: DataFrame com colunas necessárias
        salvar: Se True, salva o gráfico
        caminho_saida: Caminho para salvar o gráfico
    """
    urgenza_subgrupo = pd.crosstab(df["Categoria Urgenza"], df["Sottogruppo Pazienti"])

    # Reordenar categorias
    urgenza_subgrupo = urgenza_subgrupo.reindex(
        [cat for cat in ORDEM_URGENZA if cat in urgenza_subgrupo.index]
    )

    fig, ax = plt.subplots(figsize=(16, 10))

    sns.heatmap(
        urgenza_subgrupo,
        annot=True,
        fmt="d",
        cmap="YlOrRd",
        cbar_kws={"label": "Frequência"},
        linewidths=0.5,
        linecolor="gray",
        ax=ax,
        annot_kws={"fontsize": 12, "fontweight": "bold"},
    )

    ax.set_xlabel("Sottogruppo Pazienti", fontsize=16, fontweight="bold")
    ax.set_ylabel("Categoria Urgenza", fontsize=16, fontweight="bold")
    ax.set_title(
        "Distribuição de Categoria Urgenza por Sottogruppo Pazienti",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=12)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=12)

    plt.tight_layout()

    if salvar and caminho_saida:
        plt.savefig(caminho_saida, dpi=300, bbox_inches="tight")

    plt.show()


def evolucao_temporal_urgenza(df, salvar=False, caminho_saida=None):
    """
    Análise temporal de Categoria Urgenza

    Args:
        df: DataFrame com colunas necessárias
        salvar: Se True, salva o gráfico
        caminho_saida: Caminho para salvar o gráfico
    """
    urgenza_mes = pd.crosstab(df["Mese_anno_It"], df["Categoria Urgenza"])

    # Reordenar categorias
    urgenza_mes = urgenza_mes[
        [cat for cat in ORDEM_URGENZA if cat in urgenza_mes.columns]
    ]

    print("\n5. DISTRIBUIÇÃO TEMPORAL: CATEGORIA URGENZA POR MÊS")
    print("=" * 80)
    print(urgenza_mes)

    fig, ax = plt.subplots(figsize=(24, 10))

    for cat in urgenza_mes.columns:
        color = CORES_URGENZA.get(cat, "#95A5A6")
        ax.plot(
            urgenza_mes.index,
            urgenza_mes[cat],
            marker="o",
            linewidth=2.5,
            markersize=8,
            label=cat,
            color=color,
        )

    ax.set_xlabel("Mês/Ano", fontsize=16, fontweight="bold")
    ax.set_ylabel("Frequência de Atendimentos", fontsize=16, fontweight="bold")
    ax.set_title(
        "Evolução Temporal de Categoria Urgenza", fontsize=18, fontweight="bold", pad=20
    )
    ax.legend(
        title="Categoria Urgenza", fontsize=13, title_fontsize=14, loc="upper left"
    )
    ax.grid(True, alpha=0.3, linestyle="--")
    plt.xticks(rotation=45, ha="right", fontsize=11)

    plt.tight_layout()

    if salvar and caminho_saida:
        plt.savefig(caminho_saida, dpi=300, bbox_inches="tight")

    plt.show()


def analise_urgenza_idade(df):
    """
    Análise cruzada de Categoria Urgenza por Fascia d'età

    Args:
        df: DataFrame com colunas necessárias

    Returns:
        dict com tabelas de análise cruzada
    """
    urgenza_idade = pd.crosstab(
        df["Categoria Urgenza"], df["Fascia d'età"], margins=True, margins_name="Total"
    )

    urgenza_idade_perc = (
        pd.crosstab(df["Categoria Urgenza"], df["Fascia d'età"], normalize="index")
        * 100
    )

    print("\n6. TABELA CRUZADA: CATEGORIA URGENZA x FASCIA D'ETÀ")
    print("=" * 80)
    print(urgenza_idade)

    print("\n7. PERCENTUAIS POR CATEGORIA DE URGENZA")
    print("=" * 80)
    print(urgenza_idade_perc.round(2))

    return {"tabela": urgenza_idade, "percentuais": urgenza_idade_perc}


def resumo_executivo_urgenza(df, urgenza_counts, urgenza_perc):
    """
    Gera resumo executivo da análise de Categoria Urgenza

    Args:
        df: DataFrame completo
        urgenza_counts: Series com contagens
        urgenza_perc: Series com percentuais
    """
    print("\n" + "=" * 80)
    print("RESUMO EXECUTIVO - ANÁLISE DE CATEGORIA URGENZA")
    print("=" * 80)

    # Categoria mais frequente
    categoria_mais_freq = urgenza_counts.idxmax()
    perc_mais_freq = urgenza_perc.max()

    print(f"\n1. CATEGORIA MAIS FREQUENTE:")
    print(
        f"   {categoria_mais_freq}: {urgenza_counts[categoria_mais_freq]:,} "
        f"atendimentos ({perc_mais_freq:.2f}%)"
    )

    # Categoria menos frequente
    categoria_menos_freq = urgenza_counts.idxmin()
    perc_menos_freq = urgenza_perc.min()

    print(f"\n2. CATEGORIA MENOS FREQUENTE:")
    print(
        f"   {categoria_menos_freq}: {urgenza_counts[categoria_menos_freq]:,} "
        f"atendimentos ({perc_menos_freq:.2f}%)"
    )

    print("\n" + "=" * 80)
