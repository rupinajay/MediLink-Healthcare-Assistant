import streamlit as st
from langchain_community.llms import Ollama

# Initialize Ollama model
llm = Ollama(model="Medical")

# Create or get session state
session_state = st.session_state

# Initialize empty lists for prompts and results
if 'prompt_history' not in session_state:
    session_state.prompt_history = []
if 'result_history' not in session_state:
    session_state.result_history = []

# Streamlit app
st.title("Ollama Medical Model")

# User input for prompt
user_prompt = st.text_area("Write your prompt here")

# Check if user has entered a prompt
if st.button("Submit"):
    # Append prompt to history
    session_state.prompt_history.append(user_prompt)
    
    # Invoke Ollama model with the prompt
    result = llm.invoke(user_prompt + "Give short reply")
    
    # Append result to history
    session_state.result_history.append(result)

# Display history with prompts aligned to the left and results to the right
for i in range(len(session_state.prompt_history)):
    left_col, right_col = st.columns(2)
    left_col.write(f"Prompt: {session_state.prompt_history[i]}")
    right_col.write(f"Result: {session_state.result_history[i]}")
    st.write("-" * 40)  # Add a separator line between entries
