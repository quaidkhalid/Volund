import time
import openai
import streamlit as st
from googleapiclient.discovery import build

# This is the default and can be omitted
openai.api_key = "sk-proj-wn0LnGqTWHe0aS0TOJq8T3BlbkFJMfAkVcDYpgI6gHs46Wwy"

# YouTube Data API key
youtube_api_key = "AIzaSyBmgntY15pAsEPiCBfurPv-mpgra_wu_Io"  # Replace with your YouTube Data API key

def initial_message():
    return "Hi, I am Volund. Your AI Partner to help brainstorm ideas tailored to your interests and goals. Let's get started!"

def gather_user_information(goals, interests, challenges):
    user_input = f"Goals: {goals}, Interests: {interests}, Challenges: {challenges}"

    prompt = [
        {"role": "system",
         "content": "You are a creative brainstorming assistant helping users generate ideas based on their goals, interests, and challenges. Provide a list of personalized suggestions and strategies that can help them achieve their objectives."},
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=prompt
    )

    chatgpt_response = response["choices"][0]["message"]["content"]
    return chatgpt_response

def search_youtube(query):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=1
    ).execute()

    video_id = search_response['items'][0]['id']['videoId']
    video_title = search_response['items'][0]['snippet']['title']
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    return video_url, video_title

# Function to generate prompt
def generate_prompt(goals, interests, challenges):
    prompt = f"Your AI Optimized Prompt is:\n\n"
    prompt += f"You are a creative brainstorming assistant helping users generate ideas based on their goals, interests, and challenges. Provide a list of personalized suggestions and strategies that can help them achieve their objectives.\n\n"
    prompt += f"User Input:\nGoals: {goals}\nInterests: {interests}\nChallenges: {challenges}\n\n"
    prompt += f"AI Response:"
    return prompt

# Streamlit UI components
st.markdown("""
<div style="background-color: black; text-align: center; padding: 10px;">
    <h1 style="color: white; font-size: 70px; margin-bottom: -40px;">Volund</h1>
    <h2 style="color: white; font-size: 14px; margin-top: 0;"> </h2>
</div>
""", unsafe_allow_html=True)

# Display the initial message
st.markdown(initial_message())
time.sleep(1)  # Wait for 1 second

# Input fields
goals = st.text_input("What is your goal?")
interests = st.text_input("What are your interests?")
challenges = st.text_input("What challenges are you facing?")

if st.button("Generate Ideas"):
    if goals.strip() and interests.strip() and challenges.strip():
        # Generate and display the prompt
        st.markdown("### User Prompt:")
        prompt_text = f"You are a creative brainstorming assistant helping users generate ideas based on their {goals}, {interests}, and {challenges}. Provide a list of personalized suggestions and strategies that can help them achieve their objectives."
        st.markdown(prompt_text)
        
        # Get AI response

        response = gather_user_information(goals, interests, challenges)
        
        # Display the response
        st.markdown("### Volund's Response:")
        st.markdown(response)
        
        # Search for a relevant YouTube video
        search_query = f"{goals} {interests} {challenges}"
        video_url, video_title = search_youtube(search_query)
        
        st.markdown(f"### Relevant Video: [{video_title}]({video_url})")
        st.video(video_url)
    else:
        st.error("Please fill in all the fields")
