import yfinance as yf
import pandas as pd

# Descargar datos
df = yf.download("BZ=F", period="2y", interval="1d")

# Resetear índice para tener la columna 'Date'
df = df.reset_index()

# Si las columnas son complejas (MultiIndex), las aplanamos
if isinstance(df.columns, pd.MultiIndex):
    df.columns = [col[0] for col in df.columns]

# Imprimir columnas para depuración (verás esto en el log de GitHub si falla)
print("Columnas detectadas:", df.columns.tolist())

# Buscar la columna de fecha (suele ser 'Date')
date_col = 'Date' if 'Date' in df.columns else df.columns[0]

# Buscar la columna de precio (preferimos 'Adj Close', si no 'Close')
if 'Adj Close' in df.columns:
    price_col = 'Adj Close'
elif 'Close' in df.columns:
    price_col = 'Close'
else:
    # Si no encuentra ninguna, toma la segunda columna disponible
    price_col = df.columns[1]

# Filtrar solo lo que necesitamos
df_final = df[[date_col, price_col]].copy()
df_final.columns = ['Fecha', 'Precio']

# Limpiar datos
df_final['Precio'] = pd.to_numeric(df_final['Precio'], errors='coerce').round(2)
df_final.dropna(inplace=True)

# Guardar
df_final.to_csv("brent_precios.csv", index=False)
print("Archivo guardado con éxito")
