"""
Script de teste para verificar se todos os módulos estão funcionando
Execute este script para validar a instalação
"""

import sys
import os


def testar_importacoes():
    """Testa se todas as importações necessárias funcionam"""
    print("=" * 60)
    print("TESTE 1: Verificando Importações")
    print("=" * 60)

    modulos_necessarios = [
        ("pandas", "pd"),
        ("numpy", "np"),
        ("matplotlib.pyplot", "plt"),
        ("seaborn", "sns"),
    ]

    erros = []

    for modulo, alias in modulos_necessarios:
        try:
            __import__(modulo)
            print(f"✓ {modulo}")
        except ImportError as e:
            print(f"✗ {modulo} - ERRO: {e}")
            erros.append(modulo)

    if erros:
        print(f"\n⚠ ATENÇÃO: {len(erros)} módulos com erro!")
        print("Execute: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ Todas as importações OK!\n")
        return True


def testar_modulos_locais():
    """Testa se os módulos locais podem ser importados"""
    print("=" * 60)
    print("TESTE 2: Verificando Módulos Locais")
    print("=" * 60)

    modulos_locais = [
        "config",
        "utils",
        "analise_urgenza",
        "analise_geral",
    ]

    erros = []

    for modulo in modulos_locais:
        try:
            __import__(modulo)
            print(f"✓ {modulo}.py")
        except ImportError as e:
            print(f"✗ {modulo}.py - ERRO: {e}")
            erros.append(modulo)

    if erros:
        print(f"\n⚠ ATENÇÃO: {len(erros)} módulos locais com erro!")
        return False
    else:
        print("\n✓ Todos os módulos locais OK!\n")
        return True


def testar_configuracoes():
    """Testa se as configurações estão corretas"""
    print("=" * 60)
    print("TESTE 3: Verificando Configurações")
    print("=" * 60)

    try:
        from config import (
            CAMINHO_2022,
            CAMINHO_2023,
            CAMINHO_2024,
            CORES_URGENZA,
            ORDEM_URGENZA,
        )

        print(f"✓ Caminhos configurados:")
        print(f"  - 2022: {CAMINHO_2022}")
        print(f"  - 2023: {CAMINHO_2023}")
        print(f"  - 2024: {CAMINHO_2024}")

        # Verificar se diretórios existem
        diretorios_existem = True
        for caminho in [CAMINHO_2022, CAMINHO_2023, CAMINHO_2024]:
            if not os.path.exists(caminho):
                print(f"  ⚠ Diretório não encontrado: {caminho}")
                diretorios_existem = False

        if diretorios_existem:
            print("✓ Todos os diretórios de dados existem")
        else:
            print("⚠ ATENÇÃO: Alguns diretórios não foram encontrados")
            print("  Ajuste os caminhos em config.py")

        print(f"\n✓ Cores configuradas: {len(CORES_URGENZA)} categorias")
        print(f"✓ Ordem de urgenza: {', '.join(ORDEM_URGENZA)}")

        print("\n✓ Configurações OK!\n")
        return diretorios_existem

    except Exception as e:
        print(f"✗ ERRO nas configurações: {e}\n")
        return False


def testar_funcoes_basicas():
    """Testa funções básicas sem carregar dados"""
    print("=" * 60)
    print("TESTE 4: Testando Funções Básicas")
    print("=" * 60)

    try:
        from utils import configurar_ambiente

        print("Configurando ambiente...")
        configurar_ambiente()
        print("✓ Ambiente configurado com sucesso")

        # Testar criação de DataFrame de exemplo
        import pandas as pd
        import numpy as np

        df_teste = pd.DataFrame(
            {
                "Paziente": [1, 1, 2, 2, 3],
                "Urgenza": [1, 2, 3, 4, 5],
                "Età": [25, 25, 45, 45, 70],
            }
        )

        print(f"✓ DataFrame de teste criado: {df_teste.shape}")

        # Testar função de subcategoria
        from utils import criar_subcategoria

        df_teste = criar_subcategoria(df_teste)

        if "Sottogruppo Pazienti" in df_teste.columns:
            print("✓ Função criar_subcategoria OK")
        else:
            print("✗ Função criar_subcategoria FALHOU")
            return False

        # Testar função de categoria urgenza
        from utils import criar_categoria_urgenza

        df_teste = criar_categoria_urgenza(df_teste)

        if "Categoria Urgenza" in df_teste.columns:
            print("✓ Função criar_categoria_urgenza OK")
        else:
            print("✗ Função criar_categoria_urgenza FALHOU")
            return False

        print("\n✓ Funções básicas OK!\n")
        return True

    except Exception as e:
        print(f"✗ ERRO ao testar funções: {e}\n")
        import traceback

        traceback.print_exc()
        return False


def teste_completo_rapido():
    """Executa um teste completo rápido (se os dados existirem)"""
    print("=" * 60)
    print("TESTE 5 (Opcional): Teste com Dados Reais")
    print("=" * 60)
    print("Este teste requer que os dados estejam disponíveis.")

    resposta = input("Deseja executar teste com dados reais? (s/n): ").strip().lower()

    if resposta != "s":
        print("Teste com dados reais pulado.\n")
        return True

    try:
        from config import CAMINHO_2022
        from utils import carrega_dados, preparar_dataframe

        print(f"\nCarregando dados de {CAMINHO_2022}...")
        df = carrega_dados(CAMINHO_2022)
        print(f"✓ Dados carregados: {len(df)} registros")

        print("Preparando dados...")
        df = preparar_dataframe(df)
        print(f"✓ Dados preparados: {len(df)} registros")

        # Testar análise
        from analise_urgenza import estatisticas_urgenza

        print("\nExecutando análise de urgenza...")
        stats = estatisticas_urgenza(df)

        print("\n✓ Análise completa executada com sucesso!")
        print(f"✓ Categorias encontradas: {len(stats['counts'])}")

        return True

    except Exception as e:
        print(f"✗ ERRO no teste completo: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Executa todos os testes"""
    print("\n" + "=" * 60)
    print("TESTE DE VALIDAÇÃO - ANÁLISE MARI DOUTORADO")
    print("=" * 60 + "\n")

    resultados = []

    # Teste 1: Importações
    resultados.append(("Importações", testar_importacoes()))

    # Teste 2: Módulos locais
    resultados.append(("Módulos Locais", testar_modulos_locais()))

    # Teste 3: Configurações
    resultados.append(("Configurações", testar_configuracoes()))

    # Teste 4: Funções básicas
    resultados.append(("Funções Básicas", testar_funcoes_basicas()))

    # Teste 5: Opcional - com dados reais
    resultados.append(("Teste com Dados", teste_completo_rapido()))

    # Resumo
    print("=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)

    for nome, resultado in resultados:
        status = "✓ PASSOU" if resultado else "✗ FALHOU"
        print(f"{nome:.<40} {status}")

    testes_passados = sum(1 for _, r in resultados if r)
    total_testes = len(resultados)

    print(f"\nTotal: {testes_passados}/{total_testes} testes passaram")

    if testes_passados == total_testes:
        print("\n🎉 SUCESSO! Todos os testes passaram!")
        print("Você pode executar: python main.py\n")
        return 0
    else:
        print("\n⚠ ATENÇÃO! Alguns testes falharam.")
        print("Verifique os erros acima e corrija antes de continuar.\n")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
