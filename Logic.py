

print("Setting up your Web Dev Environment...")
!curl -fsSL https://ollama.com/install.sh | sh > /dev/null 2>&1
!pip install -qU langchain-ollama langchain-core

import subprocess
import threading
import time
import re
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def run_ollama():
    subprocess.Popen(["ollama", "serve"])

threading.Thread(target=run_ollama).start()
time.sleep(5)
!ollama pull llama3.2:1b > /dev/null 2>&1


llm = ChatOllama(model="llama3.2:1b", temperature=0.7)


system_prompt = (
    "You are an expert web developer. Your task is to generate a complete, "
    "single-file website using HTML, CSS (internal), and JS (internal). "
    "Output ONLY the code inside a single markdown code block. "
    "Do not include any explanations before or after the code."
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Create a modern website for: {user_topic} with html css and js all in a single file "),
])


chain = prompt | llm | StrOutputParser()


topic = input("Enter the website topic (e.g., 'A Pizza Shop' or 'A Space Portfolio'): ")
print(f"Generating website for '{topic}'...")

full_response = chain.invoke({"user_topic": topic})


code_match = re.search(r"```(?:html)?(.*?)```", full_response, re.DOTALL)
if code_match:
    clean_code = code_match.group(1).strip()
else:
    clean_code = full_response.strip()


with open("index.html", "w") as f:
    f.write(clean_code)

print("\n" + "="*30)
print("SUCCESS! File 'index.html' has been created.")
print("Check the folder icon on the left to download it.")
print("="*30)

