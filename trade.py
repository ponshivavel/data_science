

import pandas as pd
import json
from tkinter import Tk, filedialog
from ast import literal_eval

def load_csv():
   
    Tk().withdraw()     
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        raise FileNotFoundError("No file selected.")
    return file_path

def process_trade_history(df):
    
    cleaned_data = []

    for idx, entry in enumerate(df['Trade_History']):
        try:
           
            trade_data = literal_eval(entry) if isinstance(entry, str) else entry
            if isinstance(trade_data, list):  
                normalized_data = pd.json_normalize(trade_data)
                normalized_data['row_index'] = idx  
                cleaned_data.append(normalized_data)
        except (ValueError, SyntaxError, json.JSONDecodeError) as e:
            print(f"Error parsing row {idx}: {e}")

   
    if cleaned_data:
        return pd.concat(cleaned_data, ignore_index=True)
    else:
        print("No valid JSON data found in Trade_History column.")
        return pd.DataFrame()

def main():
    try:
       
        file_path = load_csv()
        print(f"File selected: {file_path}")

        
        df = pd.read_csv(file_path)
        print("CSV loaded successfully!")

        
        if 'Trade_History' not in df.columns:
            raise KeyError("The CSV does not contain the 'Trade_History' column.")

       
        normalized_df = process_trade_history(df)

        if not normalized_df.empty:
            print("Trade_History column normalized successfully!")
            print(normalized_df.head()) 

           
            output_file = file_path.replace(".csv", "_normalized.csv")
            normalized_df.to_csv(output_file, index=False)
            print(f"Normalized data saved to: {output_file}")
        else:
            print("No valid data to save.")

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
    except KeyError as key_error:
        print(f"Error: {key_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
