import yfinance as yf
from datetime import datetime, timedelta
import os

def download_hist_252(tickers, out_dir="data"):
    """
    Scarica gli historical data (ultimi 252 giorni di borsa) da Yahoo Finance
    per ogni ticker in `tickers` e salva un CSV per ciascuno.
    """
    # 252 giorni di trading ~ 1 anno borsistico
    end = datetime.today()
    start = end - timedelta(days=365)  # finestra calendario sufficiente a coprire 252 giorni di trading

    os.makedirs(out_dir, exist_ok=True)

    for t in tickers:
        print(f"Scarico dati per {t}...")
        # interval giornaliero, periodo definito da start/end
        df = yf.download(
            t,
            start=start.strftime("%Y-%m-%d"),
            end=end.strftime("%Y-%m-%d"),
            interval="1d",
            auto_adjust=False,
            progress=False,
        )

        if df.empty:
            print(f"Nessun dato trovato per {t}, salto.")
            continue

        # Tieni solo gli ultimi 252 record e fai una copia esplicita
        df = df.tail(252).copy()

        # Calcola rendimenti giornalieri e il relativo percentile
        df['Daily_Return'] = df['Close'].pct_change()
        df['Return_Percentile'] = df['Daily_Return'].rank(pct=True)

        # Salva XLSX
        out_path = os.path.join(out_dir, f"{t}_hist_252d.xlsx")
        df.to_excel(out_path, engine='openpyxl')
        print(f"Salvato: {out_path} ({len(df)} righe)")

if __name__ == "__main__":
    # Inserisci qui i ticker che ti interessano
    tickers = ["IBM", "GLD"]  
    download_hist_252(tickers)