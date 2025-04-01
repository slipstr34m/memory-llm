from openai import AzureOpenAI

# Initialize OpenAI client (assuming you have an existing method for this)
openai_client = AzureOpenAI(
    azure_endpoint="YOUR_AZURE_ENDPOINT",
    api_key="YOUR_API_KEY",
    api_version="2024-10-21"
)

try:
    response = openai_client.chat.completions.create(
        model="gpt-4o", 
        messages=[{"role": "user", "content": "Hello, world!"}],
        temperature=0
    )
    print(response)
except Exception as e:
    print(f"Error: {e}")