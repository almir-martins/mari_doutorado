"""
Script principal para executar todas as análises
"""

import os
import sys
from pathlib import Path

# Importações locais
from config import CAMINHO_2022, CAMINHO_2023, CAMINHO_2024
from utils import configurar_ambiente, carrega_dados, preparar_dataframe
from analise_urgenza import (
    estatisticas_urgenza,
    grafico_barras_urgenza,
    grafico_pizza_urgenza,
    analise_urgenza_subgrupo,
    heatmap_urgenza_subgrupo,
    evolucao_temporal_urgenza,
    analise_urgenza_idade,
    resumo_executivo_urgenza,
)


def carregar_dados_completos():
    """
    Carrega dados de todos os anos e consolida

    Returns:
        DataFrame consolidado
    """
    print("Carregando dados...")
    print("-" * 80)

    ano_2022_raw = carrega_dados(CAMINHO_2022)
    print(f"Dados 2022 carregados: {len(ano_2022_raw)} registros")

    ano_2023_raw = carrega_dados(CAMINHO_2023)
    print(f"Dados 2023 carregados: {len(ano_2023_raw)} registros")

    ano_2024_raw = carrega_dados(CAMINHO_2024)
    print(f"Dados 2024 carregados: {len(ano_2024_raw)} registros")

    import pandas as pd

    df_raw = pd.concat([ano_2022_raw, ano_2023_raw, ano_2024_raw], ignore_index=True)

    print(f"\nTotal consolidado: {len(df_raw)} registros")
    print("Dados carregados com sucesso!\n")

    return df_raw


def executar_analise_completa(salvar_graficos=False, diretorio_saida="./output"):
    """
    Executa todas as análises do projeto

    Args:
        salvar_graficos: Se True, salva os gráficos gerados
        diretorio_saida: Diretório para salvar os gráficos
    """
    # Configurar ambiente
    print("=" * 80)
    print("INICIANDO ANÁLISE DE DADOS MARI DOUTORADO")
    print("=" * 80)
    print()

    configurar_ambiente()

    # Criar diretório de saída se necessário
    if salvar_graficos:
        Path(diretorio_saida).mkdir(parents=True, exist_ok=True)
        print(f"Gráficos serão salvos em: {diretorio_saida}\n")

    # Carregar dados
    df_raw = carregar_dados_completos()

    # Preparar dados
    print("Preparando dados...")
    print("-" * 80)
    df = preparar_dataframe(df_raw.copy())
    print(f"Dados preparados: {len(df)} registros após limpeza")
    print(f"Colunas: {', '.join(df.columns)}\n")

    # =========================================================================
    # ANÁLISE DE CATEGORIA URGENZA
    # =========================================================================
    print("\n" + "=" * 80)
    print("ANÁLISE DE CATEGORIA URGENZA")
    print("=" * 80 + "\n")

    # Estatísticas descritivas
    stats_urgenza = estatisticas_urgenza(df)

    # Gráficos de barras
    print("\nGerando gráficos de barras...")
    caminho_barras = (
        os.path.join(diretorio_saida, "urgenza_barras.png") if salvar_graficos else None
    )
    grafico_barras_urgenza(
        stats_urgenza["counts"],
        stats_urgenza["percentuais"],
        salvar=salvar_graficos,
        caminho_saida=caminho_barras,
    )

    # Gráfico de pizza
    print("\nGerando gráfico de pizza...")
    caminho_pizza = (
        os.path.join(diretorio_saida, "urgenza_pizza.png") if salvar_graficos else None
    )
    grafico_pizza_urgenza(
        stats_urgenza["counts"], salvar=salvar_graficos, caminho_saida=caminho_pizza
    )

    # Análise cruzada com subgrupos
    analise_subgrupo = analise_urgenza_subgrupo(df)

    # Heatmap subgrupos
    print("\nGerando heatmap Urgenza x Subgrupo...")
    caminho_heatmap_sub = (
        os.path.join(diretorio_saida, "urgenza_subgrupo_heatmap.png")
        if salvar_graficos
        else None
    )
    heatmap_urgenza_subgrupo(
        df, salvar=salvar_graficos, caminho_saida=caminho_heatmap_sub
    )

    # Evolução temporal
    print("\nGerando análise temporal...")
    caminho_temporal = (
        os.path.join(diretorio_saida, "urgenza_temporal.png")
        if salvar_graficos
        else None
    )
    evolucao_temporal_urgenza(
        df, salvar=salvar_graficos, caminho_saida=caminho_temporal
    )

    # Análise por idade
    analise_idade = analise_urgenza_idade(df)

    # Resumo executivo
    resumo_executivo_urgenza(df, stats_urgenza["counts"], stats_urgenza["percentuais"])

    print("\n" + "=" * 80)
    print("ANÁLISE CONCLUÍDA COM SUCESSO!")
    print("=" * 80)

    return df


def executar_analise_rapida():
    """
    Executa apenas análises estatísticas sem gráficos (mais rápido)
    """
    configurar_ambiente()

    # Carregar e preparar dados
    df_raw = carregar_dados_completos()
    df = preparar_dataframe(df_raw.copy())

    # Apenas estatísticas
    stats_urgenza = estatisticas_urgenza(df)
    analise_urgenza_subgrupo(df)
    analise_urgenza_idade(df)
    resumo_executivo_urgenza(df, stats_urgenza["counts"], stats_urgenza["percentuais"])

    return df


if __name__ == "__main__":
    # Verificar argumentos da linha de comando
    if len(sys.argv) > 1 and sys.argv[1] == "--rapido":
        print("Executando análise rápida (sem gráficos)...\n")
        df = executar_analise_rapida()
    elif len(sys.argv) > 1 and sys.argv[1] == "--salvar":
        print("Executando análise completa e salvando gráficos...\n")
        diretorio = sys.argv[2] if len(sys.argv) > 2 else "./output"
        df = executar_analise_completa(salvar_graficos=True, diretorio_saida=diretorio)
    else:
        print("Executando análise completa (gráficos apenas na tela)...\n")
        df = executar_analise_completa(salvar_graficos=False)

    print("\nDataFrame final disponível na variável 'df'")
