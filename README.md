Jacob
-----------

This is a "math tutor" which you can converse with in real time! 

Steps to execute:

1. Make sure you have installed all dependencies
2. Edit the /environ file and add your personal API keys. You will need an OPENAI_API_KEY, and a TAVILLY_KEY.
3. Ensure that you're in the current directory C://YOUR PATH/Jacob/Server

Execute with
-----------------
*flask run*
-----------

Design information:

We leverage GPT4.o alongside the Manim Library and LangGraph to create an agent capable of generating informational mathematical videos. An example is provided in the videos folder.

**Rough outline of execution**

1. The LangGraph agent utilizes the "run_script" tool in order to create a new python file in generated_video_code.py.
2. The agent then uses the "write_script" tool, to execute the previous code using the Manim Library. If the code returns an error, the error is passed back to the agent and we return to state 1.
3. The base video should be successfully created in the previous step. We then  generate the audio for the video using pyttsx3.
4. We then append the generated audio to the generated video.
5. Once we have created the video, we post this to the Flask frontend, where it is displayed.



