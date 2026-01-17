import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict, List

load_dotenv()

def run_smoke_test():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("GROQ_API_KEY not found in environment variables.")
        return
    
    try:
        llm = ChatGroq(
            temperature=0,
            model_name="llama-3.3-70b-versatile",
            groq_api_key=os.getenv("GROQ_API_KEY"),
        )

        # model is old and trained on data up to 2024 only
        jdk_25_context="""
            JDK 25 (LTS) is released in September 2025
            New features in JDK 25 include:
            1. Pattern Matching for switch
            2. Virtual Threads
            3. Foreign Function & Memory API
            4. Structured Concurrency
            5. Improved Garbage Collection with ZGC enhancements
            6. New APIs for Vector Computation
            7. Enhanced Security Features
            8. Performance Improvements and Optimizations
            """

        # overcoming temporary hallucination by providing today's date
        user_query = "Since today is January 2026. What are new features in JDK 25?"
        full_query = f"{jdk_25_context}\n\nUser Query: {user_query}"

        # using prompt based knowledge injection to provide context to the old model
        response = llm.invoke(full_query)
        print("Complete Groq Response:", response)
        print("Response Content from Groq LLM:", response.content)

    except Exception as e:
        print(f"Error occurred: {e}")
        print("Please ensure that the GROQ_API_KEY is valid and has sufficient quota.")
        print("Smoke test failed.")

if __name__ == "__main__":
    run_smoke_test()