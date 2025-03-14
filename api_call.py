import json
from django.http import JsonResponse
from google import genai

client = genai.Client(api_key="AIzaSyBrjNAMQdMztUGfXTDTtDEF78nSLkfvE9I")

def optimize_code(code_snippet: str,optimisation_parameter) -> str:
    if(optimisation_parameter == "All"):
        prompt = f"Optimize the following code for readability , memory and speed. Return the result as a JSON object with 'text' for explanation and 'code' for the optimized code:\n\n{code_snippet}"
    else:
        prompt = f"Optimize the following code for {optimisation_parameter}. Return the result as a JSON object with 'text' for explanation and 'code' for the optimized code:\n\n{code_snippet}"
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    json_string = response.text 
    json_string = json_string[7:][:-4]
    json_data = json.loads(json_string)
    print(json_data)
    return json_data

# Example Usage
code = """
def inefficient_function(arr):
    new_arr = []
    for i in range(len(arr)):
        new_arr.append(arr[i] * 2)
    return new_arr
"""





