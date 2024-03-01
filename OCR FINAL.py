import streamlit as st
from PIL import Image
import pytesseract
from langchain_community.llms import Ollama

llm = Ollama(model="Medical")

# Function to truncate text at the last full stop within a character limit
def truncate_at_full_stop(text, limit=390):
    if len(text) <= limit:
        return text
    end = text.rfind('.', 0, limit)
    if end == -1:
        return text[:limit] + "..."
    return text[:end + 1]

def main():
    st.title("Medical Report Analysis and Query Generation")
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

if __name__ == "__main__":
    main()