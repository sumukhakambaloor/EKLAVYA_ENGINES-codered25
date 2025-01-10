import pandas as pd
import google.generativeai as genai

class Agent6:

    def __init__(self, path):
         self.path = path

    def get_query_suggestions(columns, user_prompt):
          genai.configure(api_key="AIzaSyBdM9NfUa4-BSMyQgdHh5-IKcTMF-K5O3w")
          model = genai.GenerativeModel("gemini-1.5-flash")
          prompt = f"You will now behave as the agent I describe. Below are the labels of the columns of my csv file. {columns}. \nHere is the prompt of the user {user_prompt}. Give me the best SQL query to filter the data based on the user prompt. Respond with the SQL query only. Do not say anything else in the message."

          response = model.generate_content(prompt)
          suggestions = response.text.strip().split("\n")
          return suggestions

    def agent6(self):
        csv_file = self.path
        df = pd.read_csv(csv_file)
        columns = ", ".join(df.columns)

        file_path = "prompts/latest_prompt.txt"  
        with open(file_path, "r") as file:
            file_contents = file.read()
        user_prompt = file_contents

        suggestions = Agent6.get_query_suggestions(columns, user_prompt)

        print(suggestions)