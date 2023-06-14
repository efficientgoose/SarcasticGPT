import databutton as db
import streamlit as st
import openai
from db_chat import check_for_openai_key, Chat


# Check for OpenAI key. If you want your users to bring
# their own key, you will need to rewrite this part.
# check_for_openai_key()
OPENAI_API_KEY = "sk-N8RiSqg8PTXeo4gmdQ8bT3BlbkFJgi"
openai.api_key = OPENAI_API_KEY

# Set a personality to the
prompt_template = "You are SarcasticGPT and tries to answer all questions with a humorous joke. You are sarcastic and difficult to talk to. Your jokes are always short and snarky. "



# When calling ChatGPT, we   need to send the entire chat history together
# with the instructions. You see, ChatGPT doesn't know anything about
# your previous conversations so you need to supply that yourself.
# Since Streamlit re-runs the whole script all the time we need to load and
# store our past conversations in what they call session state.
prompt = st.session_state.get("prompt", None)
if prompt is None:
    # This is the format OpenAI expects
    prompt = [{"role": "system", "content": prompt_template}]


# This is the beginning of our UI
st.title("SarcasticGPT")


form = st.form("Input box", clear_on_submit=True)
question = form.text_input("Send message", placeholder="Your prompt goes here...")
submit_button = form.form_submit_button("Send")

chat = Chat(prompt)

if question:  # Someone have asked a question
    # First we add the question to our message history
    prompt.append({"role": "user", "content": question})
    chat.update_question(question)
    response = []
    result = ""
    for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=prompt, stream=True
    ):
        text = chunk.choices[0].get("delta", {}).get("content")
        if text is not None:
            response.append(text)
            result = "".join(response).strip()
            chat.update_answer(result)

    # When we get an answer back we add that to the message history
    prompt.append({"role": "assistant", "content": result})

    # Finally, we store it in the session state
    st.session_state["prompt"] = prompt
