import streamlit as st
from PIL import Image
import pytesseract
from langchain_community.llms import Ollama
from firebase import firebase
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np

# Function to truncate text at the last full stop within a character limit
def truncate_at_full_stop(text, limit=390):
    if len(text) <= limit:
        return text
    end = text.rfind('.', 0, limit)
    if end == -1:
        return text[:limit] + "..."
    return text[:end + 1]

def main():
    st.set_page_config(
        page_title="MediLink",
        page_icon="💊",
        layout="wide"
    )

    # Main content
    st.title("MediLink")
    st.write("Your path to a healthier you")

    st.markdown("---")
    
    options = ["Homepage", "User Prompt for Symptoms", "Skin Disease Diagnosis", "Upload Health Reports", "Heart Data Insights"]
    selected_option = st.sidebar.selectbox("Select a service:", options)

    if selected_option == "Homepage":
        st.subheader("Services We Deliver")
        st.write("At MediLink, we provide a range of services to help you manage your health and wellness. Choose from the following options to learn more:")

        st.write("##### **1. User Prompt for Symptoms**", unsafe_allow_html=True)
        st.write("Our user prompt for symptoms service allows you to describe your symptoms in your own words and receive personalized recommendations for managing your condition.")

        st.write("##### **2. Skin Disease Diagnosis**", unsafe_allow_html=True)
        st.write("Our skin disease diagnosis service uses advanced computer vision algorithms to analyze images of skin lesions and provide a diagnosis based on the results.")

        st.write("##### **3. Upload Health Reports**", unsafe_allow_html=True)
        st.write("Our health report analysis service allows you to upload medical reports in various formats, including images and PDFs, and extract relevant information from them.")

        st.write("##### **4. Heart Data Insights**", unsafe_allow_html=True)
        st.write("Our heart data insights service allows you to upload data from your wearable devices or other sources and get insights into your heart health. Our system uses advanced machine learning algorithms to analyze the data and provide personalized recommendations for improving your heart health.")

    elif selected_option == "User Prompt for Symptoms":
        st.markdown("---")
        st.subheader("User Prompt for Symptoms")
        
        # Initialize Ollama model
        llm = Ollama(model="Medical")
        
        # Create or get session state
        session_state = st.session_state
        
        # Initialize empty lists for prompts and results
        if 'prompt_history' not in session_state:
            session_state.prompt_history = []
        if 'result_history' not in session_state:
            session_state.result_history = []
        
        user_prompt = st.text_area("Write your symptom description here")
        
        if st.button("Submit"):
            
                # Append prompt to history
                session_state.prompt_history.append(user_prompt)
                
                # Invoke Ollama model with the prompt
                result = llm.invoke(user_prompt + " Give short reply")
                
                # Append result to history
                session_state.result_history.append(result)
        
        # Display history with prompts aligned to the left and results to the right
        for i in range(len(session_state.prompt_history)):
            st.markdown("---")
            st.write(f"Prompt: {session_state.prompt_history[i]}", unsafe_allow_html=True)
            
            if i < len(session_state.result_history):  # Check if the index is valid
                st.write(f"Result: {session_state.result_history[i]}", unsafe_allow_html=True)
            else:
                st.write("Result: N/A", unsafe_allow_html=True)  # Display a message if the index is out of bounds
            
            st.markdown("<hr>", unsafe_allow_html=True)  # Add a separator line between entries

    elif selected_option == "Skin Disease Diagnosis":
        st.markdown("---")
        st.subheader("Skin Disease Diagnosis")
        st.write("We provide a skin disease diagnosis service that uses advanced computer vision algorithms to analyze images of skin lesions and provide a diagnosis based on the results. Simply upload an image of the affected area and let our system do the rest.")

    elif selected_option == "Upload Health Reports":
        st.markdown("---")
        st.subheader("Upload Health Reports")
        st.write("Our health report analysis service allows you to upload medical reports in various formats, including images and PDFs, and extract relevant information from them. Our system uses advanced natural language processing techniques to analyze the text and generate a summary of the report, along with any relevant insights or recommendations.")

        # Initialize Ollama model
        llm = Ollama(model="Medical")
        
        # Upload image
        image_file = st.file_uploader("Upload Medical Report Image", type=["jpg", "jpeg", "png"])

        if image_file is not None:
            # Display the uploaded image
            st.image(image_file, caption='Uploaded Medical Report', use_column_width=True)
            try:
                # Convert the file to an image
                image = Image.open(image_file)
                # Extract text from image
                report_text = pytesseract.image_to_string(image)

                # Display extracted text
                st.text_area("Extracted Text", report_text, height=250)
                final = llm.invoke(report_text)
                st.write(final)
            except Exception as e:
                st.error(f"Error processing the image: {e}")

    elif selected_option == "Heart Data Insights":
        st.markdown("---")
        st.subheader("Heart Data Insights")
        st.write("Our heart data insights service allows you to upload data from your wearable devices or other sources and get insights into your heart health. Our system uses advanced machine learning algorithms to analyze the data and provide personalized recommendations for improving your heart health.")

        # Initialize Firebase application
        from firebase import firebase
        import numpy as np
        firebase = firebase.FirebaseApplication('https://medilink-96dd6-default-rtdb.asia-southeast1.firebasedatabase.app/py/users')
        result = firebase.get('https://medilink-96dd6-default-rtdb.asia-southeast1.firebasedatabase.app/py/users', None)
        import matplotlib.pyplot as plt
        import time
        import numpy as np
        i=1
        j=[]
        p=[]
        st.write("Processing:")
        while(1):
            result = firebase.get('https://medilink-96dd6-default-rtdb.asia-southeast1.firebasedatabase.app/py/users', None)
            time.sleep(1)
            p.append(result[0]["Heart_Rate"])
            j.append(i)
            i+=1
            if(i%10==0):
                plt.plot(j,p)
                plt.show()
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()
                mean_hr = np.mean(p)
                max_hr = np.max(p)
                min_hr = np.min(p)
                std_hr = np.std(p)
                median_hr = np.median(p)
                st.write("Analysis and Insights:")
                st.write("Mean Heart Rate:", mean_hr, "bpm")
                st.write("Maximum Heart Rate:", max_hr, "bpm")
                st.write("Minimum Heart Rate:", min_hr, "bpm")
                st.write("Standard Deviation of Heart Rate:", std_hr, "bpm")
                st.write("Median Heart Rate:", median_hr, "bpm")
                break
           # st.pyplot()
            # Calculate heart rate statistics

        # Wait for 1 second before retrieving the next heart rate data
if __name__ == "__main__":
    main()
