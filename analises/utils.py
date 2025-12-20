"""
Funções utilitárias para análise de dados
"""

import os
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def configurar_ambiente():
    """
    Configura o ambiente de análise com estilos e configurações padrão
    """
    warnings.filterwarnings("ignore")

    # Tamanho e estilo dos gráficos
    plt.style.use("bmh")
    plt.rcParams["figure.figsize"] = [22, 9]
    plt.rcParams["font.size"] = 21

    # Configuração de exibição das linhas e colunas do pandas
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    pd.set_option("display.expand_frame_repr", False)

    # Configuração do pandas para quantidade de casas decimais
    pd.set_option("display.float_format", lambda x: "%.2f" % x)

    sns.set()


def exibe_boxplot(data, col):
    """
    Exibe múltiplos boxplots lado a lado

    Args:
        data: DataFrame com os dados
        col: Número de colunas para exibição
    """
    indice = 1
    for coluna in data.columns:
        plt.subplot(1, col, indice)
        sns.boxplot(data[coluna]).set(title=coluna)
        indice += 1


def exibe_countplot(data, col):
    """
    Exibe múltiplos countplots lado a lado

    Args:
        data: DataFrame com os dados
        col: Número de colunas para exibição
    """
    indice = 1
    for coluna in data.columns:
        plt.subplot(1, col, indice)
        plt.xticks(rotation=90)
        sns.countplot(data=data, x=data[coluna]).set(
            title=coluna, ylabel="Contagem", xlabel=None
        )
        indice += 1


def plota_ausentes(data, title, x_title, perc_minimo=0):
    """
    Plota gráfico de valores ausentes e retorna estatísticas

    Args:
        data: DataFrame com os dados
        title: Título do gráfico
        x_title: Título do eixo x
        perc_minimo: Percentual mínimo para incluir no gráfico

    Returns:
        DataFrame com estatísticas de valores ausentes
    """
    # Pega as colunas com dados ausentes
    colunas_com_nan = [col for col in data if data[col].isna().sum() > perc_minimo]

    # Plot do gráfico de barras com o percentual
    if len(colunas_com_nan) > 0:
        ax = (
            data[colunas_com_nan]
            .isna()
            .mean()
            .sort_values(ascending=True)
            .mul(100)
            .round(1)
            .plot(kind="barh")
        )
        ax.set_xlabel(x_title)
        ax.set_title(title)
        ax.bar_label(ax.containers[0])

        # Tabela da contagem dos dados faltantes
        print("Contagem de faltantes")
        missing_counts = data[colunas_com_nan].isna().sum().sort_values(ascending=True)
        print(missing_counts)
        return missing_counts
    else:
        print("Contagem de faltantes")
        missing_counts = data.isna().sum()
        print(missing_counts)
        return missing_counts


def carrega_dados(caminho):
    """
    Carrega e concatena múltiplos arquivos CSV de um diretório

    Args:
        caminho: Caminho do diretório contendo os arquivos CSV

    Returns:
        DataFrame consolidado sem duplicatas
    """
    lista_arquivos = os.listdir(caminho)
    lista_arquivos = [arquivo for arquivo in lista_arquivos if arquivo.endswith(".csv")]
    df_list = []

    for arquivo in lista_arquivos:
        caminho_arquivo = os.path.join(caminho, arquivo)

        # Tentar diferentes encodings
        try:
            df_temp = pd.read_csv(
                caminho_arquivo,
                sep=",",
                encoding="utf-8",
                parse_dates=["Data Accesso", "Data Fine Contatto", "Data Nascita"],
                dayfirst=True,
            )
        except UnicodeDecodeError:
            try:
                df_temp = pd.read_csv(
                    caminho_arquivo,
                    sep=",",
                    encoding="latin-1",
                    parse_dates=["Data Accesso", "Data Fine Contatto", "Data Nascita"],
                    dayfirst=True,
                )
            except UnicodeDecodeError:
                df_temp = pd.read_csv(
                    caminho_arquivo,
                    sep=",",
                    encoding="iso-8859-1",
                    parse_dates=["Data Accesso", "Data Fine Contatto", "Data Nascita"],
                    dayfirst=True,
                )

        df_list.append(df_temp)

    df = pd.concat(df_list, ignore_index=True)
    df_unicos = df.drop_duplicates(keep="first")

    return df_unicos


def criar_subcategoria(df):
    """
    Cria coluna de subcategoria de pacientes baseado em número de atendimentos

    Args:
        df: DataFrame com os dados

    Returns:
        DataFrame com coluna 'Sottogruppo Pazienti' adicionada
    """
    # Contar quantos atendimentos cada Paziente teve
    contagem_por_paciente = df.groupby("Paziente").size()

    # Criar categorias
    def categorizar_paciente(num_atendimentos):
        if num_atendimentos < 4:
            return "Common user"
        elif 4 <= num_atendimentos <= 5:
            return "Frequent User"
        elif 6 <= num_atendimentos <= 9:
            return "Heavy User"
        else:  # >= 10
            return "High User"

    # Mapear a categoria para cada paciente
    categoria_por_paciente = contagem_por_paciente.apply(categorizar_paciente)

    # Adicionar a coluna ao dataframe original
    df["Sottogruppo Pazienti"] = df["Paziente"].map(categoria_por_paciente)

    return df


def criar_categoria_urgenza(df):
    """
    Cria coluna de categoria de urgência mapeando os códigos

    Args:
        df: DataFrame com coluna 'Urgenza'

    Returns:
        DataFrame com coluna 'Categoria Urgenza' adicionada
    """
    mapeamento_urgenza = {
        1: "Bianca",
        2: "Verde",
        3: "Gialla",
        4: "Arancione",
        5: "Rossa",
    }

    df["Categoria Urgenza"] = df["Urgenza"].map(mapeamento_urgenza)
    return df


def criar_features_temporais(df):
    """
    Cria features temporais a partir da coluna 'Data Accesso'

    Args:
        df: DataFrame com coluna 'Data Accesso' em formato datetime

    Returns:
        DataFrame com features temporais adicionadas
    """
    from config import MAPEAMENTO_DIAS

    # Dia da semana
    df["Dia_Semana"] = df["Data Accesso"].dt.dayofweek.map(MAPEAMENTO_DIAS)

    # Semana do ano
    df["Settimana"] = df["Data Accesso"].dt.isocalendar().week

    # Mês e ano
    df["Mese_anno"] = df["Data Accesso"].dt.to_period("M")

    # Mês e ano em formato italiano
    mesi_italiani = {
        1: "Gennaio",
        2: "Febbraio",
        3: "Marzo",
        4: "Aprile",
        5: "Maggio",
        6: "Giugno",
        7: "Luglio",
        8: "Agosto",
        9: "Settembre",
        10: "Ottobre",
        11: "Novembre",
        12: "Dicembre",
    }

    df["Mese_anno_It"] = df["Data Accesso"].apply(
        lambda x: f"{mesi_italiani[x.month]}/{x.year}"
    )

    return df


def criar_faixa_etaria(df):
    """
    Cria faixas etárias a partir da coluna 'Età'

    Args:
        df: DataFrame com coluna 'Età'

    Returns:
        DataFrame com coluna 'Fascia d'età' adicionada
    """
    bins = [0, 14, 44, 64, 120]
    labels = ["< 15 anni", "15-44 anni", "45-64 anni", "> 64 anni"]

    df["Fascia d'età"] = pd.cut(df["Età"], bins=bins, labels=labels)

    return df


def preparar_dataframe(df):
    """
    Aplica todas as transformações de preparação no DataFrame

    Args:
        df: DataFrame bruto

    Returns:
        DataFrame preparado
    """
    from config import COLUNAS_REMOVER

    # Remover colunas desnecessárias
    df = df.drop(columns=COLUNAS_REMOVER, errors="ignore")

    # Remover linhas com valores ausentes
    df = df.dropna()

    # Alterar tipos de dados
    if "Sessione Ticket" in df.columns:
        df["Sessione Ticket"] = df["Sessione Ticket"].astype("Int64")
    df["Numero Scheda PS"] = df["Numero Scheda PS"].astype("str")

    # Criar features derivadas
    df = criar_subcategoria(df)
    df = criar_categoria_urgenza(df)
    df = criar_features_temporais(df)
    df = criar_faixa_etaria(df)

    return df
