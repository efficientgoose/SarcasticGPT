import openai
import streamlit as st
from streamlit_chat import message



# This function uses the OpenAI Completion API to generate a 
# response based on the given prompt. The temperature parameter controls 
# the randomness of the generated response. A higher temperature will result 
# in more random responses, 
# while a lower temperature will result in more predictable responses.
def generate_response(prompt):
    response = openai.ChatCompletion.create (
        model='gpt-3.5-turbo',
        messages=[
        {"role": "user", "content": "You are SarcasticGPT and tries to answer all questions with a humorous joke. You are sarcastic and difficult to talk to. Your jokes are always short and snarky."},
        {"role": "system", "content": prompt},
        ],
        temperature=1,
    )

    message = response['choices'][0]['message']['content']
    return message

# Building the UI for the app
st.title("SarcasticGPT 🤖💬😂")

st.caption("This witty bot is sure to crack you up! If you are having a bad day, or are just bored, interact with this chatbot and you'll have a lot of fun, I promise!")

st.markdown("Get your OpenAI API Key [here](https://platform.openai.com/account/api-keys) ")

apikey = st.text_input("Please enter the OpenAI API Key: ")



openai.api_key = apikey

if apikey:
    
    if len(apikey) == 51:
        st.success("Successfully entered the key! Now you are free to interact with the bot",icon="✅")
        
    else:  
        st.error("The entered key is incorrect. Please enter a correct one", icon="❌")
        
    

    # If generated and past do not exist, go ahead and create them.
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    # Let the user ask a prompt, and store it in some variable
    user_input = st.text_input("You: ", placeholder="Ask the bot anything you want!")

    # If the user has asked a prompted, send it to the generate_response func
    if user_input:
        output = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)


    if st.session_state['generated']:

        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            
            
else:
    st.error("Please enter the OpenAI API Key to interact with the bot.")



# st.write("Made with ❤️ by [Ajinkya Kale](https://www.linkedin.com/in/ajinkode/)")


# Add the footer text
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgb(42, 42, 43);
        color: white;
        text-align: center;
        padding: 10px;
    }
    
    .small{
        padding-top: 5px;
        font-size: 0.9rem;
    }
    
    a{
        color: yellow;
        text-decoration: none;
    }
    
    </style>
    <div class="footer">
        <p> Made with ❤️by <a href="https://www.linkedin.com/in/ajinkode/">Ajinkya Kale</a><p>
        <p class="small">Heya! If for whatever reason your API Key is not working, just reach out to me on <a href="https://www.linkedin.com/in/ajinkode/">LinkedIn</a> and I'll provide you with one.</p>
    </div>
    """,
    unsafe_allow_html=True
)




