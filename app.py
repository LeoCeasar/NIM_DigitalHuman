from openai import OpenAI
import fastapi


"""
1. <HTML>js
callurl
text

fastapi urlapi (convert incoming data to back end)

web text -> server fastapi -> NIM -> return text 2 web

2. tts text 2 speach
Microsoft ID (Rong)

3. speech 2 OV 
Omniverse Kit (audio2face)

"""

def call_llama3_70b_byNIM(q: str, ...):
  pass

def 



def send_audio2OV():
  pass


client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

completion = client.chat.completions.create(
  model="meta/llama3-70b-instruct",
  messages=[{"role":"user","content":"Write an article about machine learning."}],
  temperature=0.5,
  top_p=1,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")

