import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

api = os.getenv('GOOGLE_GEMINI_API_KEY')
genai.configure(api_key=api)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Lets create the UI
st.title(':orange[HEALTHIFY] :blue[AI Powered personel health assistant]')
st.markdown('''##### This application will assist you to have a better and healthy life. You can ask your health related questions and get personalised guidance.''')
tips = '''Follow the steps
* Enter your details in the side bar.
* Enter your Gender, Age, Height (cms), Weight (Kgs).
* Select the number on the fitness scale (0-5). 5-Fittest and 0-No fittness at all.
* After filling the details write your query here and get customised response.'''
st.write(tips)

# Lets configure sidebar
st.sidebar.header(':red[ENTER YOUR DETAILS]')
name = st.sidebar.text_input('Enter your name')
gender = st.sidebar.selectbox('Select your gender',['Male','Female'])
age = st.sidebar.text_input('Enter your age in yrs')
weight = st.sidebar.text_input('Enter your weight in Kgs')
height = st.sidebar.text_input('Enter your height in cms')
bmi = pd.to_numeric(weight)/(pd.to_numeric(height)/100)**2
fittness = st.sidebar.slider('Rate your fittness between 0-5',0,5,step=1)
st.sidebar.write(f'{name} your BMI is: {round(bmi,2)} Kg/m^2')

# Lets use genai model to get the output
user_query = st.text_input('Enter your question here')
prompt = f'''Assume you are a health expert. You are required to
answer the question asked by the user. Use the following details provided by 
the user.
name of user is {name}
gender is {gender}
age is {age}
weight is {weight} kgs
height is {height} cms
bmi is {bmi} kg/m^2
and user rates his/her fittness as {fittness} out of 5

Your output should be in the following format
* It should start by giving one two line comment on the details that have been provided.
* It should explain what the real problem is based on the query asked by user.
* What could be the possible reason for the problem.
* What are the possible solutions for the problem.
* You can also mention what doctor to see (specialization) if required.
* Striclty do not recommend or advise any medicine.
* output should be in bullet points and use tables wherever required.
* In the end give 5-7 line of summary of every thing that has been discussed.

here is the query from the user {user_query}'''

if user_query:
    response = model.generate_content(prompt)
    st.write(response.text)