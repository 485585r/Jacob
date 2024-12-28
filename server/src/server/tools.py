from langchain_core.tools import tool

from langchain_community.tools import TavilySearchResults



import subprocess
@tool
def add(a: int, b: int):
    """Add two numbers. Please let the user know that you're adding the numbers BEFORE you call the tool"""
    return a + b


@tool
def write_script(script: str):
    """Write and save the python script for generating the manim animation. The script must be in proper python syntax for it to work"""
    file_name = "C:\\matematica_voice\\react-voice-agent\\server\\sSrc\\server\\example.py"

    # Save the string as a .py file
    with open(file_name, "w") as file:
        file.write(script)

    return f"File saved as filename {file_name}"

@tool
def run_script(file_name: str, script_class: str):
    """run the manim script you just made. To use this tool, input the file name the write_script tool just made and nothing else. You also need to input the main class that runs the whole scene"""

    command = [
    "manim", "-pql", f"{file_name}", f"{script_class}"
    ]

    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
    except Exception as e:
        return {"status": "error", "message": str(e)}


tavily_tool = TavilySearchResults(
    max_results=5,
    include_answer=True,
    description=(
        "This is a search tool for accessing the internet.\n\n"
        "Let the user know you're asking your friend Tavily for help before you call the tool."
    ),
)

TOOLS = [add, tavily_tool, write_script, run_script]
