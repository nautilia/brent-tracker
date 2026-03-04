import yfinance as yf
import pandas as pd

# Ticker del Brent
data = yf.download("BZ=F", period="2y", interval="1d")

# Limpieza para Flourish
data = data.reset_index()
# Si yfinance devuelve MultiIndex (común en versiones nuevas), aplanamos
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data = data[['Date', 'Adj Close']]
data.columns = ['Fecha', 'Precio']
data['Precio'] = data['Precio'].round(2)
data.dropna(inplace=True)

# Guardar
data.to_csv("brent_precios.csv", index=False)
