import os
import openai
import pandas as pd
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Set it as an environment variable or in a .env file.")

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/recommend_steps', methods=['POST'])
def recommend_steps():
    try:
        file = request.files.get('file')
        user_instructions = request.form.get('instructions')

        logger.info(f"File received: {file}")
        logger.info(f"Instructions received: {user_instructions}")

        if not file:
            logger.error("File not received")
            return jsonify({"error": "File is required"}), 400

        # Read the file into a DataFrame
        df = pd.read_csv(file)

        # Prepare the data sample, description, and info
        data_head = df.head(5).to_string()  # Limit to first 5 rows
        data_description = df.describe().to_string()
        data_info = str(df.info(buf=None))

        # Prepare the prompt
        prompt = f"""
        You are a Data Cleaning Expert. Given the following information about the data, 
        recommend a series of numbered steps to take to clean and preprocess it. 
        The steps should be tailored to the data characteristics and should be helpful 
        for a data cleaning agent that will be implemented.
        
        General Steps:
        * Removing columns if more than 40 percent of the data is missing
        * Imputing missing values with the mean of the column if the column is numeric
        * Imputing missing values with the mode of the column if the column is categorical
        * Converting columns to the correct data type
        * Removing duplicate rows
        * Removing rows with missing values
        * Removing rows with extreme outliers (3X the interquartile range)
        
        Custom Steps:
        * Analyze the data to determine if any additional data cleaning steps are needed.
        * Recommend steps that are specific to the data provided. Include why these steps are necessary or beneficial.
        * If no additional steps are needed, simply state that no additional steps are required.
        """

        if user_instructions:
            prompt += f"\n\nUser instructions:\n{user_instructions}"

        prompt += f"\n\nData Sample (first 5 rows):\n{data_head}\n\nData Description (summary):\n{data_description}\n\nData Info (summary):\n{data_info}\n\nReturn the steps as a bullet point list (no code, just the steps)."

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a data cleaning assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0
        )

        recommended_steps = response.choices[0].message['content']
        return jsonify({"steps": recommended_steps})
    except Exception as e:
        logger.error("Error generating cleaning steps: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)