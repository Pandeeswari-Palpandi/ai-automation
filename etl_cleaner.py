import os
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def clean_student_data_with_llm(df):
    """
    Sends the student data dataframe to gpt-4o-mini to clean according to specific rules.
    """
    # Convert dataframe to a JSON string to pass into the prompt
    data_json = df.to_json(orient="records")

    prompt = f"""
    You are an expert data cleaning assistant. Clean the following JSON array of student records based strictly on these rules:

    RULES:
    1. Name: Convert to Title Case (e.g., "Pandeeswari P").
    2. Email: If the email format is invalid or missing, set it to "INVALID_EMAIL".
    3. Phone: If the phone number has fewer than 10 digits (or is invalid/missing), set it to "MISSING".
    4. Course: Must be strictly one of these three values: "Python", "Machine Learning", or "Data Science". Map closest matches.
    5. Fee_Paid: Convert "yes"/"YES" to true (boolean), and "no"/"No" to false (boolean).
    6. City: Convert to Title Case. If empty, missing, or null, set it to "UNKNOWN".
    7. Enrolled_Date: Standardize the date format to "YYYY-MM-DD".

    Input Data:
    {data_json}

    Output Requirements:
    - Return ONLY a valid JSON array containing the cleaned records.
    - Do not include markdown formatting tags like ```json or any conversational text. Just raw JSON string.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise data cleaning utility that outputs only valid JSON arrays."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )

        cleaned_text = response.choices[0].message.content.strip()

        # Clean up any accidental markdown wrappers if present
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.split("```")[1]
            if cleaned_text.startswith("json"):
                cleaned_text = cleaned_text[4:]
        cleaned_text = cleaned_text.strip()

        cleaned_data = json.loads(cleaned_text)
        return pd.DataFrame(cleaned_data)

    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        return None


def run_etl_pipeline(input_path: str, output_path: str):
    print("--- Step 1 & 2: Loading and Reading the CSV file ---")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at: {input_path}")

    df_raw = pd.read_csv(input_path)
    print(f"Successfully loaded {len(df_raw)} rows from {input_path}.")

    print("\n--- Step 3: Cleaning data using OpenAI gpt-4o-mini ---")
    # For 50 rows, we can process them all in a single prompt.
    # (If scaling up to thousands, you would loop through chunks of 50-100 rows).
    df_cleaned = clean_student_data_with_llm(df_raw)

    if df_cleaned is not None:
        print("\n--- Step 4: Creating the final CSV file ---")
        df_cleaned.to_csv(output_path, index=False)
        print(f"Final cleaned CSV successfully saved to: {output_path}")

        # Preview first few rows
        print("\nPreview of Cleaned Data:")
        print(df_cleaned.head())
    else:
        print("ETL pipeline failed during the cleaning stage.")


if __name__ == "__main__":
    INPUT_CSV = "student_enrollment_raw.csv"     # Replace with your input file path
    OUTPUT_CSV = "students_cleaned.csv"  # Desired output file path

    run_etl_pipeline(INPUT_CSV, OUTPUT_CSV)
