import pandas as pd
import google.generativeai as genai

class Agent5:

    def __init__(self, path):
         self.path = path

    def get_column_suggestions(columns, user_prompt):
          genai.configure(api_key="AIzaSyBdM9NfUa4-BSMyQgdHh5-IKcTMF-K5O3w")
          model = genai.GenerativeModel("gemini-1.5-flash")
          prompt = f"You will now behave as the agent I describe. Below are the labels of the columns of my csv file. {columns}. \nHere is the prompt of the user {user_prompt}. Give me the essential columns related to this prompt from the columns I have. Give me only the columns in format 'Column1, Column2, Column3' etc. Do not say anything else in the message."

          response = model.generate_content(prompt)
          suggestions = response.text.strip().split("\n")
          suggestions_list = suggestions[0].split(',')
          return suggestions_list

    def agent5(self):
        csv_file = self.path
        df = pd.read_csv(csv_file)
        columns = ", ".join(df.columns)

        file_path = "prompts/latest_prompt.txt"  
        with open(file_path, "r") as file:
            file_contents = file.read()
        user_prompt = file_contents

        suggestions = Agent5.get_column_suggestions(columns, user_prompt)

        print("Partial completion of the task by Agent 5:")
        
        # Ensure the suggestions are valid column names in the DataFrame
        valid_suggestions = [col for col in suggestions if col in df.columns]
        
        if valid_suggestions:
            filtered_df = df[valid_suggestions]
            # Save the filtered dataset to a new file
            output_path = "filtered_dataset.csv"
            filtered_df.to_csv(output_path, index=False)
            print(f"Filtered dataset saved to {output_path}")
        else:
            print("No valid columns found based on the prompt.")
