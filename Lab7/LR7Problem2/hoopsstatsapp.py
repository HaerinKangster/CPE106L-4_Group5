"""
File: hoopstatsapp.py

The application for analyzing basketball stats with data cleaning.
"""

import pandas as pd
from hoopstatsview import HoopStatsView

def cleanStats(frame):
    """
    Cleans the basketball statistics data frame by processing FG, 3PT, and FT columns.
    
    For each of these columns:
    - Removes the original column from the data frame
    - Creates two new columns from the original data (makes and attempts)
    - Inserts the new columns at the appropriate positions
    
    Args:
        frame: pandas DataFrame containing basketball statistics
        
    Returns:
        pandas DataFrame with cleaned statistics
    """
    # Make a copy of the frame to avoid modifying the original
    cleaned_frame = frame.copy()
    
    # Define the columns to process and their new column names
    columns_to_process = [
        ('FG', 'FGM', 'FGA'),      # Field Goals: Makes, Attempts
        ('3PT', '3PM', '3PA'),     # 3-Pointers: Makes, Attempts  
        ('FT', 'FTM', 'FTA')       # Free Throws: Makes, Attempts
    ]
    
    # Process each column
    for original_col, makes_col, attempts_col in columns_to_process:
        if original_col in cleaned_frame.columns:
            # Get the position of the original column
            col_position = cleaned_frame.columns.get_loc(original_col)
            
            # Split the data (format is "makes-attempts")
            split_data = cleaned_frame[original_col].str.split('-', expand=True)
            makes = split_data[0].astype(int)      # Convert makes to integer
            attempts = split_data[1].astype(int)   # Convert attempts to integer
            
            # Remove the original column
            cleaned_frame = cleaned_frame.drop(columns=[original_col])
            
            # Insert the new columns at the original position
            cleaned_frame.insert(col_position, makes_col, makes)
            cleaned_frame.insert(col_position + 1, attempts_col, attempts)
    
    return cleaned_frame


# Example usage and testing
def main():
    """Creates the data frame, cleans it, and starts the app."""
    # Load the raw data
    raw_frame = pd.read_csv("rawbrogdonstats.csv")
    
    # Clean the data
    cleaned_frame = cleanStats(raw_frame)
    
    # Save the cleaned data (this creates the cleanbrogdonstats.csv file)
    cleaned_frame.to_csv("cleanbrogdonstats.csv", index=False)
    
    # Print confirmation that cleaning worked
    print("Data cleaned successfully!")
    print("Original columns:", list(raw_frame.columns))
    print("Cleaned columns:", list(cleaned_frame.columns))
    print("\nFirst few rows of cleaned data:")
    print(cleaned_frame.head())
    
    # Start the HoopStatsView with cleaned data
    HoopStatsView(cleaned_frame)

if __name__ == "__main__":
    main()