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

    clientes = pd.read_csv(arquivo)

    idade_valida = (
        (clientes["idade"] >= 18)
        & (clientes["idade"] <= 100)
    )

    clientes_validos = clientes[idade_valida]

    clientes_quarentena = clientes[~idade_valida]

    total_lidos = len(clientes)
    total_validos = len(clientes_validos)
    total_rejeitados = len(clientes_quarentena)

    clientes_quarentena.to_csv(
        "data/clientes_quarentena.csv",
        index=False
    )

    inseridos, atualizados = carregar_clientes(clientes_validos)

    print("\nCLIENTES VÁLIDOS:")
    print(clientes_validos)

    print("\nCLIENTES EM QUARENTENA:")
    print(clientes_quarentena)

    fim = time.time()

    print("\nRESUMO DA EXECUÇÃO:")
    print(f"Registros lidos: {total_lidos}")
    print(f"Registros válidos: {total_validos}")
    print(f"Registros rejeitados: {total_rejeitados}")
    print("\nBANCO DE DADOS:")
    print(f"Registros inseridos: {inseridos}")
    print(f"Registros atualizados: {atualizados}")


    tempo_execucao = fim - inicio
    print(f"\nTempo de execução: {tempo_execucao:.2f} segundos")
    print("\nSTATUS: SUCCESS")

except Exception as erro:
    print("\nSTATUS: FAILED")
    print(f"Erro: {erro}")
