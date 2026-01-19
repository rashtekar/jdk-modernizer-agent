import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

print(f"Current Working Directory: {os.getcwd()}")
env_path = Path(__file__).parent.parent / ".env"
print(f"Checking for .env file: {env_path.exists()}")
if env_path.exists():
    # check for the api key
    load_dotenv(dotenv_path=env_path)
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        print("GROQ_API_KEY found in .env file.")
    else:
        print("GROQ_API_KEY not found in .env file.")
else:
    print(f".env file not found at: {env_path}")


class JDKModernizerModel:
    def __init__(self):
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables.")
        else:
            self.client = Groq(api_key=groq_api_key)
            self.model_name = "llama-3.3-70b-versatile"

    def get_modernization_suggestion(self, file_name: str, source_code: str):
        """
        Sends the source code to the Groq model and retrieves modernization suggestions.
        """
        system_prompt = (
            "You are a Java 25 refactoring engine. Modernize legacy code with these strict constraints:\n"
            "1. CONVERSIONS: Use Records for POJOs, 'var' for local variables, and enhanced switch expressions."
            "2. COMPLIANCE: Use only standard Java 25. Switch statements MUST be exhaustive (include 'default' or 'case null, default')."
            "3. SCOPE: Refactor only. Do not add new methods, factory logic, or redefined peer classes. Assume external dependencies exist."
            "4. ACCESSORS: If a class becomes a Record, ensure all internal calls to getters (e.g., getId()) are updated to accessor style (e.g., id())."
            "5. IDEMPOTENCY: If code is already modern, return the original text unchanged."
            "6. OUTPUT: Return ONLY raw source code. No markdown, no backticks, no explanations."
            "CRITICAL: 1. If the existing object is of type Object, do not change/rewrite/refactor it. 2. Output start with 'package' and end with '}'. Do not include ANY characters before or after the code block. 3. LOCAL VARIABLES: Use 'var' for local variables ONLY when the initializer is specific (e.g., 'new ArrayList<>()' or '\"string\"').\n"
        )

        user_prompt = f"Modernize this file with latest JDK 25 features: {file_name}\n\nJava Code:\n{source_code}"

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
        )
        return response.choices[0].message.content
