import pandas as pd
from sqlalchemy import text

from database import engine


def carregar_clientes(clientes):
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


arquivo = "data/clientes.csv"

clientes = pd.read_csv(arquivo)

idade_valida = (
    (clientes["idade"] >= 18)
    & (clientes["idade"] <= 100)
)

clientes_validos = clientes[idade_valida]

clientes_quarentena = clientes[~idade_valida]

clientes_quarentena.to_csv(
    "data/clientes_quarentena.csv",
    index=False
)

carregar_clientes(clientes_validos)

print("\nCLIENTES VÁLIDOS:")
print(clientes_validos)

print("\nCLIENTES EM QUARENTENA:")
print(clientes_quarentena)