from zhipuai import ZhipuAI
from datetime import datetime

# Initialize the ZhipuAI client
client = ZhipuAI(api_key="your api_key")

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Define tools (enable web search)
tools = [{
    "type": "web_search",
    "web_search": {
        "enable": True  # Enable web search
        # "search_result": True  # Optional: include raw search results
    }
}]

# System prompt template, including the current date
system_prompt = f"""You are an intelligent assistant with web access. When appropriate, prioritize using up-to-date information from the web (reference information) to ensure accurate and timely responses. """

# User input query
user_input = "Lady Gaga - - Me and The Horse I Rode In On ( PHOTO ) -"

# Construct the dynamic user prompt
user_question = f"Based on the latest available information, provide a response to the user's input: Return the top 3 web pages related to the following text: '{user_input}'. Extract all named entities present in the text and classify them into categories [PER, LOC, ORG, MISC]. Summarize the content of the retrieved web pages. Respond in English."

# Example alternative input (commented out):
# user_input = "@ LouisVuitton @ mrkimjones he is living up to his title as louis vuitton ' s \" best dressed man \" !"
# user_question = f"Based on the latest available information, provide a response to the user's input: Return the top 3 web pages related to the following text: '{user_input}'. Extract all named entities present in the text and classify them into categories [PER, LOC, ORG, MISC]. Summarize the content of the retrieved web pages. Respond in English."

# Build the message history
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_question}
]

# Generate the response
response = client.chat.completions.create(
    model="GLM-4-Flash-250414",
    messages=messages,
    tools=tools
)

# Print the result
print(response.choices[0].message)