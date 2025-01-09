import pandas as pd
import string
import nltk
import shutil, os
from nltk.corpus import stopwords

# Download NLTK stopwords if not already present
nltk.download('stopwords')

class agent2:
    def __init__(self, csv_path):
         self.csv_path = csv_path
    
    def clean_text(text):
         # Remove punctuation and special characters
          text = ''.join(char for char in text if char.isalnum() or char.isspace())
          
          # Remove stop words
          stop_words = set(stopwords.words('english'))
          text = ' '.join(word for word in text.split() if word.lower() not in stop_words)
          
          return text


     # Main processing function
    def process_csv(file_path, output_file):
          # Stage 1: Read the CSV file
          df = pd.read_csv(file_path)
          
          # Stage 2: Remove rows with NaN, null, or blank cells
          df.dropna(inplace=True)
          
          # Stage 3: Remove duplicate rows
          df.drop_duplicates(inplace=True)
          
          # Stage 4: Remove punctuation, stop words, and special characters
          # Apply cleaning to all string columns
          for col in df.select_dtypes(include=['object']):
               df[col] = df[col].apply(agent2.clean_text)
          
          # Save the cleaned DataFrame to a new CSV file
          df.to_csv(output_file, index=False)
          print(f"Processed CSV saved as: {output_file}")

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
    
    def agent2(self):
          input_file = "path/to/your_input_file.csv"
          output_file = "path/to/processed_file.csv"
          agent2.process_csv(input_file, output_file)
          agent2.copy_and_delete_file(output_file, input_file)
    

