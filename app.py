import streamlit as st
import pandas as pd
from gtts import gTTS
import datetime
import os

# Load the CSV file
df = pd.read_csv('pregnancy_tests_schedule.csv')

# Generate voice instructions and save the file if it doesn't exist
def generate_voice_instructions():
    instructions = (
        "Welcome to the Pregnancy Blood Test Recommender. "
        "Please enter the current week of your pregnancy, ranging from 1 to 40. "
        "Then select your trimester from the dropdown: First Trimester, Second Trimester, or Third Trimester. "
        "Finally, enter your expected delivery date to generate a schedule for your tests."
    )
    if not os.path.exists("voice_instructions.mp3"):
        tts = gTTS(instructions)
        tts.save("voice_instructions.mp3")

# Call to generate the audio instructions file
generate_voice_instructions()

# Display the voice instructions audio
st.audio("voice_instructions.mp3", format="audio/mp3")

# Function to suggest tests based on user input
def suggest_tests(week, trimester):
    filtered_data = df[(df['Week'] == week) & (df['Trimester'].str.lower() == trimester.lower())]
    if not filtered_data.empty:
        return filtered_data['Recommended Tests / Check-ups'].values[0]
    else:
        return "No specific tests are recommended for this week in the given trimester."

# Function to generate schedule
def generate_schedule(delivery_date):
    delivery_date = datetime.datetime.strptime(delivery_date, "%Y-%m-%d").date()
    start_date = delivery_date - datetime.timedelta(weeks=40)
    schedule = []
    for _, row in df.iterrows():
        week_start = start_date + datetime.timedelta(weeks=row['Week'] - 1)
        schedule.append({"Week": row['Week'], "Date": week_start, "Test": row['Recommended Tests / Check-ups']})
    return pd.DataFrame(schedule)

# Streamlit UI
st.title("Pregnancy Blood Test Recommender with Schedule Generator")
week = st.number_input("Enter Week of Pregnancy (1-40)", min_value=1, max_value=40, step=1)
trimester = st.selectbox("Select Trimester", ["First Trimester", "Second Trimester", "Third Trimester"])
delivery_date = st.text_input("Enter Expected Delivery Date (YYYY-MM-DD)")

if st.button("Get Recommended Test"):
    result = suggest_tests(week, trimester)
    st.write(result)

if st.button("Generate Schedule"):
    if delivery_date:
        schedule_df = generate_schedule(delivery_date)
        st.write(schedule_df)
    else:
        st.write("Please enter a valid delivery date.")
