import io
import os
from errno import ECHILD


from langchain_core.messages import AIMessage
import speech_recognition as sr
from flask import Flask, render_template, request, jsonify, send_from_directory, abort
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from pydub import AudioSegment
from prompt import INSTRUCTIONS
from typing import Annotated, TypedDict
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import tools_condition

os.environ['TAVILY_API_KEY'] = "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"
os.environ['OPENAI_API_KEY'] = "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"

from tools import TOOLS


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: MessagesState, config: RunnableConfig):

        while True:

            state = {**state}
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                    not result.content
                    or isinstance(result.content, list)
                    and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}



tool_node = ToolNode(TOOLS)


llm = ChatOpenAI(model="gpt-4o", temperature=.7, api_key = os.environ["OPENAI_API_KEY"])

model = INSTRUCTIONS | llm.bind_tools(TOOLS)

workflow = StateGraph(MessagesState)
workflow.add_node("agent", Assistant(model))
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")

workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    tools_condition,
)
workflow.add_edge("tools", "agent")

agent = workflow.compile()
printed_messages = set()


def create_app():
    app = Flask(__name__)

    # Base directory for video files
    VIDEO_FOLDER = r"C:/JacobTest"

    @app.route('/get_video', methods=['POST'])
    def get_video():
        # Get the filename from the POST request
        filename = request.json.get('filename')
        print(filename)
        if not filename:
            return jsonify({"error": "Filename is required"}), 400

        # Construct the full path to the file
        file_path = os.path.join(VIDEO_FOLDER, filename)

        # Validate file existence
        if not os.path.exists(file_path):
            abort(404, description="File not found")

        # Serve the video file
        return send_from_directory(VIDEO_FOLDER, filename)


    @app.route("/")
    def index():
        return render_template("index.html")

    messages = []

    @app.route("/transcribe", methods=["POST"])
    def transcribe():
        file = request.files["audio"]
        audio = AudioSegment.from_file(io.BytesIO(file.read()), format="webm")
        wav_data = io.BytesIO()
        audio.export(wav_data, format="wav")
        wav_data.seek(0)

        recognizer = sr.Recognizer()

        # Convert to AudioFile that speech_recognition can use
        # Note: speech_recognition supports wav, aiff, aif, flac
        with sr.AudioFile(wav_data) as source:
            # Read the audio data
            audio_data = recognizer.record(source)

            # Perform the transcription
            text = recognizer.recognize_google(audio_data)

            print(text)

            try:
                user_message = text
                messages.append({"role": "user", "content": user_message})

                # Invoke the model
                final_state = agent.invoke({"messages": messages})

                # Extract the assistant's response from final_state
                assistant_response = final_state.get("messages")

                if assistant_response:
                    # Get the latest AI message
                    if isinstance(assistant_response, list):
                        assistant_response = assistant_response[-1]  # Get the last message

                    # Check if the response is an AIMessage
                    if isinstance(assistant_response, AIMessage):
                        msg_repr = assistant_response.content  # Access the content of the AIMessage
                        # Append only the content to the session state
                        messages.append({"role": "assistant", "content": msg_repr})
                    else:
                        msg_repr = "No valid AI message found."
                else:
                    msg_repr = "No messages received."


                return {"input": user_message, "output": msg_repr}



            except Exception as e:

                return (f"Error invoking the model: {e}")

    return app