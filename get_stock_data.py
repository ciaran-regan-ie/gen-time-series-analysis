import sys
import os
import pandas as pd
import yfinance as yf
from datetime import datetime

# Define the directory path
dir_path = 'src/data/'

# Check if the directory exists
if not os.path.exists(dir_path):
    # If the directory doesn't exist, create it
    os.makedirs(dir_path)

# Function to download stock data
def download_stock_data(ticker_symbol):
    start_date = datetime(2021, 1, 1)  # Adjust start date as needed
    end_date = datetime.today()  # Today's date

    try:
        # Fetch the data from Yahoo Finance
        df = yf.download(ticker_symbol, period="5d", interval="1m")

        if df.empty:
            raise ValueError("Ticker unrecognized or no data available")

        # Select only the 'Adj Close' column and reset the index to get the datetime as a column
        df_final = df[['Adj Close']].reset_index()

        # Rename the columns to 'datetime' and 'price'
        df_final.columns = ['datetime', 'price']

        # Convert datetime to Unix timestamp (seconds since epoch)
        df_final['datetime'] = df_final['datetime'].apply(lambda x: int(x.timestamp()))

        # Save the DataFrame to a CSV file without headers
        csv_filename = f'{dir_path}{ticker_symbol.lower()}.csv'
        df_final.to_csv(csv_filename, index=False, header=False)

        print(f'Stock data saved to {csv_filename}')
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py <TICKER_SYMBOL>")
    else:
        ticker_symbol = sys.argv[1]
        download_stock_data(ticker_symbol)
