import os
import pandas as pd
import time

start_time = time.time() 

data_folder = 'data'  # Replace with the path to your data folder
symbols = []

# Get a list of stock symbols from the file names
file_names = [f for f in os.listdir(data_folder) if f.endswith('_historical_data.csv')]
symbols = [f.split('_')[0] for f in file_names]

def load_stock_data(folder_path, symbol):
    file_path = os.path.join(folder_path, f'{symbol}_historical_data.csv')
    df = pd.read_csv(file_path)#, parse_dates=['Date'], thousands=',', na_values='Dividend'
    
    print(f"Original shape of {symbol}: {df.shape}")
    
    # Filter out rows containing "Dividend" in the 'Open' column
    # df = df[~df['Open'].astype(str).str.contains('Dividend', na=False, case=False)]

    for column in df.columns:
        df = df[~df[column].astype(str).str.contains('Dividend', na=False, case=False)]
    
    # df = df[~df['Open'].astype(str).str.contains('-', na=False, case=False)]

    for column in df.columns:
        df = df[~df[column].astype(str).str.contains('-', na=False, case=False)]

    for column in df.columns:
        df = df[~df[column].astype(str).str.contains('splits', na=False, case=False)]

    print(f"Shape of {symbol} after filtering: {df.shape}")
    
    # Add a 'Symbol' column to the DataFrame
    df['Symbol'] = symbol
    
    # Save the filtered DataFrame to a new CSV file
    df.to_csv(f'processed_data/filtered_{symbol}_historical_data.csv', index=False)
    
    return df

# Load and preprocess data for each stock
dataframes = [load_stock_data(data_folder, symbol) for symbol in symbols]
print(dataframes[0])



print('--- %s seconds ---' % (time.time() - start_time))