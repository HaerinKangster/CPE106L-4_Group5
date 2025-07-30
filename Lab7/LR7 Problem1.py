import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import requests
from io import StringIO

def create_sample_data():
    data = {
        'Year': [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 
                2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        'Average_Price': [1.05, 1.07, 1.20, 1.37, 1.39, 1.37, 1.45, 1.42, 1.40, 1.41, 
                         1.44, 1.37, 1.33, 1.29, 1.31, 1.45, 1.53, 1.73, 1.97, 1.96, 1.91]
    }
    return pd.DataFrame(data)

def load_and_clean_data(filename=None):
    try:
        if filename:
            df = pd.read_csv(filename)
        else:
            print("No file provided, using sample data based on BLS statistics...")
            df = create_sample_data()
            
        print("Original data shape:", df.shape)
        print("\nFirst few rows:")
        print(df.head())
        
        print("\n=== Data Cleaning ===")
        
        print(f"Missing values before cleaning: {df.isnull().sum().sum()}")
        
        df = df.dropna(subset=['Average_Price'])
        
        df = df[df['Average_Price'] > 0]
        
        df['Year'] = df['Year'].astype(int)
        
        df = df.sort_values('Year').reset_index(drop=True)
        
        df = df.drop_duplicates(subset=['Year']).reset_index(drop=True)
        
        print(f"Missing values after cleaning: {df.isnull().sum().sum()}")
        print(f"Final data shape: {df.shape}")
        
        print("\n=== Data Summary ===")
        print(f"Years covered: {df['Year'].min()} to {df['Year'].max()}")
        print(f"Price range: ${df['Average_Price'].min():.2f} to ${df['Average_Price'].max():.2f}")
        print(f"Average price over all years: ${df['Average_Price'].mean():.2f}")
        
        return df
        
    except FileNotFoundError:
        print(f"File {filename} not found. Using sample data instead.")
        return create_sample_data()
    except Exception as e:
        print(f"Error loading data: {e}")
        print("Using sample data instead.")
        return create_sample_data()

def plot_bread_prices(df):
    plt.figure(figsize=(12, 8))
    
    plt.plot(df['Year'], df['Average_Price'], 
             marker='o', linewidth=2, markersize=6, 
             color='steelblue', markerfacecolor='red', markeredgecolor='darkred')
    
    plt.title('Average Price of Bread (White, Pan, per lb.) Over Time\nBased on U.S. Bureau of Labor Statistics Data', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Year', fontsize=12, fontweight='bold')
    plt.ylabel('Average Price (USD)', fontsize=12, fontweight='bold')
    
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.2f}'))
    
    plt.grid(True, alpha=0.3, linestyle='--')
    
    years = df['Year'].values
    if len(years) > 10:
        tick_step = max(1, len(years) // 10)
        plt.xticks(years[::tick_step], rotation=45)
    else:
        plt.xticks(years, rotation=45)
    
    max_price_year = df.loc[df['Average_Price'].idxmax(), 'Year']
    max_price = df['Average_Price'].max()
    min_price_year = df.loc[df['Average_Price'].idxmin(), 'Year']
    min_price = df['Average_Price'].min()
    
    plt.annotate(f'Highest: ${max_price:.2f}\n({max_price_year})', 
                xy=(max_price_year, max_price), 
                xytext=(10, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    plt.annotate(f'Lowest: ${min_price:.2f}\n({min_price_year})', 
                xy=(min_price_year, min_price), 
                xytext=(10, -20), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='lightgreen', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    plt.tight_layout()
    
    plt.show()
    
    print("\n=== Price Analysis ===")
    price_change = df['Average_Price'].iloc[-1] - df['Average_Price'].iloc[0]
    percent_change = (price_change / df['Average_Price'].iloc[0]) * 100
    
    print(f"Price change from {df['Year'].iloc[0]} to {df['Year'].iloc[-1]}: ${price_change:.2f}")
    print(f"Percentage change: {percent_change:.1f}%")
    
    if len(df) >= 10:
        print("\nDecade averages:")
        for decade_start in range(df['Year'].min(), df['Year'].max(), 10):
            decade_data = df[(df['Year'] >= decade_start) & (df['Year'] < decade_start + 10)]
            if not decade_data.empty:
                avg_price = decade_data['Average_Price'].mean()
                print(f"{decade_start}s: ${avg_price:.2f}")

def main():
    """
    Main function to execute the bread price analysis.
    """
    print("=== BLS Bread Price Analysis ===")
    print("Loading and analyzing average bread prices from U.S. Bureau of Labor Statistics\n")
    
    try:
        df = load_and_clean_data('breadprice.csv')
    except:
        df = load_and_clean_data()
    
    print("\n=== Cleaned Data ===")
    print(df)
    
    print("\nGenerating line plot...")
    plot_bread_prices(df)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()