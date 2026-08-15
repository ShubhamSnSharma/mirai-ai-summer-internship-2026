import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="how to be rich in graw a garden2[roblox]"
)

print(response.text)

'''
ai vs llm 
cloud computing 
token and tokenization 
'''
