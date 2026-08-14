import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Create a Groq client using the API key from environment variables
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

# Generate an answer using the provided context
def generate_answer(
    question: str,
    context: str
):

    # Build the prompt for the LLM
    prompt = f"""
You are a helpful assistant.

Answer only using the provided context.

If the answer is not present,
say you don't know.

Context:
{context}

Question:
{question}
"""

    # Send the prompt to the model
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
       messages=[
        {
            "role":"system",
            "content":"""
            You must answer only from context.
            If answer is absent say:
            'I don't know.'
            """
        },
        {
            "role":"user",
            "content": prompt
        }
        ]
    )

    # Return the generated answer
    return response.choices[0].message.content