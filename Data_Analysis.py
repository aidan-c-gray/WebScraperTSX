import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_data(folder_path, symbol):
    file_path = os.path.join(folder_path, f'filtered_{symbol}_historical_data.csv')
    df = pd.read_csv(file_path, parse_dates=['Date'])
    df.bfill()
    return df

def calculate_daily_percentage_change(df):    
    df['Daily_Return'] = df['Close*'].pct_change(-1, fill_method=None) * 100  # Calculate daily percentage change
    return df

def main():
    folder_path = 'processed_data'  # Update with your actual folder path
    reference_symbol = 'WTI.TO'
    
    # Load data for the reference symbol
    reference_data = load_data(folder_path, reference_symbol)
    reference_data = calculate_daily_percentage_change(reference_data)
    
    # Ensure correlation_results is explicitly a DataFrame
    correlation_results_list = []
    
    reference_data.loc[reference_data["Daily_Return"] >= 0, "Daily_Return"] = 1
    print(reference_data)
    reference_data.loc[reference_data["Daily_Return"] <= 0, "Daily_Return"] = 0

    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv') and filename != f'filtered_{reference_symbol}_historical_data.csv':
            symbol = filename.split('_')[1]  # Extract symbol from the filename
            data = load_data(folder_path, symbol)
            data = calculate_daily_percentage_change(data)
            print(data)
            data.loc[data["Daily_Return"] >= 0, "Daily_Return"] = 1
            print(data)
            data.loc[data["Daily_Return"] <= 0, "Daily_Return"] = 0
            print(data)
            print(reference_data)

            # Merge data with the reference symbol on the 'Date' column
            merged_data = pd.merge(reference_data[['Date', 'Daily_Return']], data[['Date', 'Daily_Return']], on='Date', suffixes=('_Reference', '_Current'))

            merged_data = merged_data.dropna(subset=['Daily_Return_Reference', 'Daily_Return_Current'])
            # Calculate correlation between the daily percentage changes
            correlation = merged_data['Daily_Return_Reference'].corr(merged_data['Daily_Return_Current'])

            # Store the results in the DataFrame
            correlation_results_list.append({'Symbol': symbol, 'Correlation': correlation})
    
    correlation_results = pd.DataFrame(correlation_results_list)

    correlation_results.bfill()
    # Plot the correlation results
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Symbol', y='Correlation', data=correlation_results)
    plt.title('Correlation of Daily Percentage Change with WTI.TO')
    plt.xlabel('Stock Symbol')
    plt.ylabel('Correlation')
    plt.show()
    print(correlation_results.sort_values(by='Correlation', ascending=False))

if __name__ == "__main__":
    main()
