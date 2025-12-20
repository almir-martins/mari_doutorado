"""
Módulo para análises de outros aspectos dos dados
(Modalità Dimissione, Problema Principale, etc.)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def analise_dimissione(df):
    """
    Análise de Modalità Dimissione

    Args:
        df: DataFrame com coluna 'Modalità Dimissione'

    Returns:
        dict com estatísticas
    """
    dimissione_counts = df["Modalità Dimissione"].value_counts()
    dimissione_perc = df["Modalità Dimissione"].value_counts(normalize=True) * 100

    print("\n" + "=" * 80)
    print("ANÁLISE DE MODALITÀ DIMISSIONE")
    print("=" * 80)
    print("\nDistribuição:")
    print("-" * 80)

    resumo = pd.DataFrame(
        {"Frequência": dimissione_counts, "Percentual (%)": dimissione_perc.round(2)}
    )
    print(resumo)

    return {
        "counts": dimissione_counts,
        "percentuais": dimissione_perc,
        "resumo": resumo,
    }


def analise_problema_principal(df, top_n=10):
    """
    Análise dos principais problemas

    Args:
        df: DataFrame com coluna 'Problema Principale'
        top_n: Número de problemas principais a exibir

    Returns:
        dict com estatísticas
    """
    problema_counts = df["Problema Principale"].value_counts()
    problema_perc = df["Problema Principale"].value_counts(normalize=True) * 100

    print("\n" + "=" * 80)
    print(f"ANÁLISE DE PROBLEMA PRINCIPALE (Top {top_n})")
    print("=" * 80)
    print("\nProblemas mais frequentes:")
    print("-" * 80)

    top_problemas = pd.DataFrame(
        {
            "Frequência": problema_counts.head(top_n),
            "Percentual (%)": problema_perc.head(top_n).round(2),
        }
    )
    print(top_problemas)

    return {
        "counts": problema_counts,
        "percentuais": problema_perc,
        "top_problemas": top_problemas,
    }


def analise_pacientes_frequentes(df, limite=10):
    """
    Identifica e analisa pacientes frequentes (Heavy Users)

    Args:
        df: DataFrame com coluna 'Paziente'
        limite: Número mínimo de atendimentos para ser considerado frequente

    Returns:
        DataFrame com pacientes frequentes
    """
    atendimentos_por_paciente = (
        df.groupby("Paziente").size().sort_values(ascending=False)
    )
    pacientes_frequentes = atendimentos_por_paciente[
        atendimentos_por_paciente >= limite
    ]

    print("\n" + "=" * 80)
    print(f"PACIENTES FREQUENTES (>= {limite} atendimentos)")
    print("=" * 80)
    print(f"\nTotal de pacientes frequentes: {len(pacientes_frequentes)}")
    print(
        f"Percentual do total: {len(pacientes_frequentes)/df['Paziente'].nunique()*100:.2f}%"
    )
    print(f"\nTop 10 pacientes com mais atendimentos:")
    print("-" * 80)
    print(pacientes_frequentes.head(10))

    return pacientes_frequentes


def analise_temporal_geral(df):
    """
    Análise temporal geral dos atendimentos

    Args:
        df: DataFrame com coluna 'Data Accesso'

    Returns:
        dict com análises temporais
    """
    # Por dia da semana
    atendimentos_dia = df["Dia_Semana"].value_counts()

    # Por mês
    atendimentos_mes = df["Mese_anno_It"].value_counts()

    print("\n" + "=" * 80)
    print("ANÁLISE TEMPORAL GERAL")
    print("=" * 80)

    print("\nAtendimentos por dia da semana:")
    print("-" * 80)
    from config import ORDEM_DIAS

    for dia in ORDEM_DIAS:
        if dia in atendimentos_dia.index:
            print(f"{dia}: {atendimentos_dia[dia]:,}")

    print(f"\nMédia de atendimentos por mês: {atendimentos_mes.mean():.0f}")
    print(
        f"Mês com mais atendimentos: {atendimentos_mes.idxmax()} ({atendimentos_mes.max():,})"
    )
    print(
        f"Mês com menos atendimentos: {atendimentos_mes.idxmin()} ({atendimentos_mes.min():,})"
    )

    return {"por_dia": atendimentos_dia, "por_mes": atendimentos_mes}


def estatisticas_idade(df):
    """
    Estatísticas descritivas da idade dos pacientes

    Args:
        df: DataFrame com coluna 'Età'

    Returns:
        DataFrame com estatísticas
    """
    print("\n" + "=" * 80)
    print("ESTATÍSTICAS DE IDADE")
    print("=" * 80)

    stats = df["Età"].describe()
    print("\nEstatísticas descritivas:")
    print("-" * 80)
    print(stats)

    # Por faixa etária
    print("\nDistribuição por faixa etária:")
    print("-" * 80)
    faixas = df["Fascia d'età"].value_counts()
    faixas_perc = df["Fascia d'età"].value_counts(normalize=True) * 100

    resumo_faixas = pd.DataFrame(
        {"Frequência": faixas, "Percentual (%)": faixas_perc.round(2)}
    )
    print(resumo_faixas)

    return {"stats": stats, "faixas": resumo_faixas}


def relatorio_geral(df):
    """
    Gera relatório geral consolidado

    Args:
        df: DataFrame completo
    """
    print("\n" + "=" * 80)
    print("RELATÓRIO GERAL - RESUMO EXECUTIVO")
    print("=" * 80)

    print(f"\n1. DADOS GERAIS")
    print("-" * 80)
    print(f"Total de atendimentos: {len(df):,}")
    print(f"Total de pacientes únicos: {df['Paziente'].nunique():,}")
    print(
        f"Período: {df['Data Accesso'].min().strftime('%d/%m/%Y')} a {df['Data Accesso'].max().strftime('%d/%m/%Y')}"
    )
    print(f"Média de atendimentos por paciente: {len(df)/df['Paziente'].nunique():.2f}")

    print(f"\n2. DISTRIBUIÇÃO POR SUBGRUPO")
    print("-" * 80)
    subgrupos = df["Sottogruppo Pazienti"].value_counts()
    for subgrupo, count in subgrupos.items():
        perc = count / len(df) * 100
        print(f"{subgrupo}: {count:,} ({perc:.2f}%)")

    print(f"\n3. CATEGORIA URGENZA PREDOMINANTE")
    print("-" * 80)
    cat_predominante = df["Categoria Urgenza"].value_counts().idxmax()
    count_predominante = df["Categoria Urgenza"].value_counts().max()
    perc_predominante = count_predominante / len(df) * 100
    print(f"{cat_predominante}: {count_predominante:,} ({perc_predominante:.2f}%)")

    print(f"\n4. MODALITÀ DIMISSIONE MAIS COMUM")
    print("-" * 80)
    dim_comum = df["Modalità Dimissione"].value_counts().idxmax()
    count_dim = df["Modalità Dimissione"].value_counts().max()
    perc_dim = count_dim / len(df) * 100
    print(f"{dim_comum}: {count_dim:,} ({perc_dim:.2f}%)")

    print("\n" + "=" * 80)
