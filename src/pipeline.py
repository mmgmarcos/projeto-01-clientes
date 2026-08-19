import pandas as pd

from database import engine


arquivo = "data/clientes.csv"

clientes = pd.read_csv(arquivo)

print(clientes)

idade_valida = (clientes["idade"] >=18) & (clientes["idade"] <=100)

clientes_validos = clientes[idade_valida]

clientes_validos.to_sql(
    "clientes",
    con=engine,
    if_exists="append",
    index=False
)

clientes_quarentena = clientes[~idade_valida]

clientes_quarentena.to_csv("data/clientes_quarentena.csv", index=False)

print("\nCLIENTES VÁLIDOS:")
print(clientes_validos)

print("\nCLIENTES EM QUARENTENA:")
print(clientes_quarentena)