import pandas as pd
import google.generativeai as genai
import os as os
import shutil as shutil



class Agent3:   
    def __init__(self, path):
         self.path = path

    def calculate_new_columns(df, operations):
          for operation in operations:
               parts = operation.split(", ")
               if len(parts) == 3:
                    new_col, tool, col = parts
                    if tool == "mean":
                         df[new_col] = df[col].mean()
                    elif tool == "median":
                         df[new_col] = df[col].median()
                    elif tool == "standard deviation":
                         df[new_col] = df[col].std()
               elif len(parts) == 4:
                    new_col, tool, col1, col2 = parts
                    if tool == "difference":
                         df[new_col] = df[col1] - df[col2]
                    elif tool == "product":
                         df[new_col] = df[col1] * df[col2]
          return df
    
    def get_column_suggestions(columns, user_prompt):
          genai.configure(api_key="AIzaSyBdM9NfUa4-BSMyQgdHh5-IKcTMF-K5O3w")
          model = genai.GenerativeModel("gemini-1.5-flash")
          prompt = f"You will now behave as the agent I describe. Below are the labels of the columns of my csv file. {columns}. \nHere is the prompt of the user {user_prompt}. Here are mathematical tools at your displosal : mean, median, standard deviation, difference, product\nBased on the prompt, give me applicable (if any) operations of mathematical tools on one or more columns which would aid in data analysis. I will be adding them to the csv file so suggest column names too.\nRespond in the format \"NewColumnName, MathematicalTool, ColumnName(s)\". If the operation requires 2 columns, use the format \"NewColumnName, MathematicalTool, Column1, Column2\". Do not say anything else in the message."

          response = model.generate_content(prompt)
          suggestions = response.text.strip().split("\n")
          return suggestions
    def copy_and_delete_file(source_path, destination_path):
         try:
               # Copy the contents of the source file to the destination file
               shutil.copyfile(source_path, destination_path)
               print(f"Contents copied from {source_path} to {destination_path}")

               # Delete the original file
               os.remove(source_path)
               print(f"Deleted the original file: {source_path}")
         except FileNotFoundError:
               print(f"File not found: {source_path}")
         except Exception as e:
               print(f"An error occurred: {e}")
    def agent3(self):
          csv_file = self.path
          if not os.path.exists(csv_file):
            print(f"File not found: {csv_file}")
            return
          df = pd.read_csv(csv_file)

          # Columns and user prompt
          columns = ", ".join(df.columns)

          file_path = "prompts/latest_prompt.txt"  
          with open(file_path, "r") as file:
               file_contents = file.read()
          user_prompt = file_contents

          # Get suggestions
          suggestions = Agent3.get_column_suggestions(columns, user_prompt)

          # Add new columns
          updated_df = Agent3.calculate_new_columns(df, suggestions)

          # Save updated CSV
          updated_csv_file = "updated_file.csv"
          updated_df.to_csv(updated_csv_file, index=False)

          Agent3.copy_and_delete_file(updated_csv_file, csv_file)

          print(f"Updated the csv file [Agent 3 Completion]")

