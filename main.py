import os
from dotenv import load_dotenv
from google import genai
import time
import asyncio
import sys
from google.genai import types
from config import SYSTEM_PROMPT
from google.genai.types import GenerateContentConfig
from functions.get_info_files import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function

load_dotenv()
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
    )
system_prompt = SYSTEM_PROMPT

async def fetch(): 
    if len(sys.argv) < 2:
        print("we need a prompt")
        sys.exit(1)
    verbose_Flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_Flag = True
    prompt = sys.argv[1]
    print(prompt)

    messages = [
        types.Content(
            role="user", 
            parts=[types.Part(text=prompt)]
        )
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )
    max_iters = 20

    for i in range(max_iters):
        for attempt in range(3):
            try:
                response = await client.aio.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=messages,
                    config=config,
                )
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed:", e)

                if attempt < 2:
                    await asyncio.sleep(2)
                else:
                    raise
        if response is None or response.usage_metadata is None:
            print("response is malformed")
            return
        if response.candidates:
            for candidate in response.candidates:
                if candidate is not None and candidate.content is not None:
                    messages.append(candidate.content)
        if response.function_calls:

            for function_call_part in response.function_calls:
                result = call_function(
                    function_call_part,
                    verbose_Flag
                )
                messages.append(result)
            continue
        print(response.text)
        break

    if verbose_Flag:
        print(f"User prompt:, {prompt}")
        print(f"prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response token: {response.usage_metadata.candidates_token_count}")

asyncio.run(fetch())


            
                    