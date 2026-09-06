import time

import pandas as pd
from sqlalchemy import text

from database import engine


def carregar_clientes(clientes):
    inseridos = 0
    atualizados = 0
    query = text("""
        INSERT INTO clientes (
            id_cliente,
            nome,
            estado,
            idade
        )
        VALUES (
            :id_cliente,
            :nome,
            :estado,
            :idade
        )
        ON CONFLICT (id_cliente)
        DO UPDATE SET
            nome = EXCLUDED.nome,
            estado = EXCLUDED.estado,
            idade = EXCLUDED.idade
    """)

    with engine.begin() as connection:
        for cliente in clientes.to_dict(orient="records"):
            connection.execute(query, cliente)
            verificar = text("""
            SELECT EXISTS (
            SELECT 1
            FROM clientes
            WHERE id_cliente = :id_cliente
            )
            """)

            existe = connection.execute(
                verificar,
                {"id_cliente": cliente["id_cliente"]}
            ).scalar()

            if existe:
                atualizados += 1
            else:
                inseridos += 1
            connection.execute(query, cliente)

    return inseridos, atualizados

inicio = time.time()

try:
    arquivo = "data/clientes.csv"

    # ============================================================
    # 1. LEITURA DOS DADOS
    # ============================================================

    clientes = pd.read_csv(arquivo)

    # ============================================================
    # 2. NORMALIZAÇÃO DOS DADOS
    # ============================================================

    clientes["estado"] = (
        clientes["estado"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # ============================================================
    # 3. REGRAS DE DATA QUALITY
    # ============================================================

    ufs_validas = {
        "AC", "AL", "AP", "AM", "BA", "CE", "DF",
        "ES", "GO", "MA", "MT", "MS", "MG", "PA",
        "PB", "PR", "PE", "PI", "RJ", "RN", "RS",
        "RO", "RR", "SC", "SP", "SE", "TO"
    }

    estado_valido = clientes["estado"].isin(ufs_validas)

    idade_valida = (
        (clientes["idade"] >= 18)
        & (clientes["idade"] <= 100)
    )

    # ============================================================
    # 4. MOTIVO DA REJEIÇÃO
    # ============================================================

    clientes["motivo_rejeicao"] = ""

    clientes.loc[
        ~idade_valida,
        "motivo_rejeicao"
    ] = "idade fora do intervalo permitido"

    clientes.loc[
        ~estado_valido,
        "motivo_rejeicao"
    ] = "estado invalido"

    # ============================================================
    # 5. CLASSIFICAÇÃO DOS REGISTROS
    # ============================================================

    registro_valido = idade_valida & estado_valido

    clientes_validos = clientes.loc[
        registro_valido,
        ["id_cliente", "nome", "estado", "idade"]
    ]

    clientes_quarentena = clientes.loc[
        ~registro_valido
    ]

    # ============================================================
    # 6. MÉTRICAS DA EXECUÇÃO
    # ============================================================

    total_lidos = len(clientes)
    total_validos = len(clientes_validos)
    total_rejeitados = len(clientes_quarentena)

    # ============================================================
    # 7. GRAVAÇÃO DA QUARENTENA
    # ============================================================

    clientes_quarentena.to_csv(
        "data/clientes_quarentena.csv",
        index=False
    )

    # ============================================================
    # 8. CARGA NO POSTGRESQL
    # ============================================================

    inseridos, atualizados = carregar_clientes(clientes_validos)

    # ============================================================
    # 9. RESULTADOS
    # ============================================================

    print("\nCLIENTES VÁLIDOS:")
    print(clientes_validos)

    print("\nCLIENTES EM QUARENTENA:")
    print(clientes_quarentena)

    print("\nRESUMO DA EXECUÇÃO:")
    print(f"Registros lidos: {total_lidos}")
    print(f"Registros válidos: {total_validos}")
    print(f"Registros rejeitados: {total_rejeitados}")

    print("\nBANCO DE DADOS:")
    print(f"Registros inseridos: {inseridos}")
    print(f"Registros atualizados: {atualizados}")

    fim = time.time()
    tempo_execucao = fim - inicio

    print(f"\nTempo de execução: {tempo_execucao:.2f} segundos")
    print("\nSTATUS: SUCCESS")

except Exception as erro:
    print("\nSTATUS: FAILED")
    print(f"Erro: {erro}")