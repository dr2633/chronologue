# streamlit_tempo_suggester.py

import streamlit as st
from datetime import datetime
from ics import Calendar
from pathlib import Path
import re
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Helper: Generate tempo tokens from an event
def generate_tempo_tokens(event):
    tokens = []
    start = event.begin.datetime
    end = event.end.datetime

    tokens.append(f"<tempo:{start.strftime('%Y-%m-%dT%H:%MZ')}>")
    tokens.append(f"<tempo:{start.strftime('%A')}>")

    hour = start.hour
    if hour < 12:
        tokens.append("<tempo:Morning>")
    elif hour < 17:
        tokens.append("<tempo:Afternoon>")
    else:
        tokens.append("<tempo:Evening>")

    duration = end - start
    minutes = int(duration.total_seconds() / 60)
    tokens.append(f"<tempo:duration-{minutes}min>")

    if re.search(r'meeting|sync', event.name, re.IGNORECASE):
        tokens.append("<tempo:meeting>")
    if event.location:
        loc_token = event.location.replace(" ", "").replace(",", "")
        tokens.append(f"<tempo:location-{loc_token}>")

    return tokens

# Helper: Convert .ics file to structured prompt blocks
def extract_events_and_tokens(ics_path):
    with open(ics_path, "r") as f:
        c = Calendar(f.read())

    events = []
    for e in c.events:
        tokens = generate_tempo_tokens(e)
        summary = e.description.strip() if e.description else "No description."
        event_block = {
            "title": e.name,
            "timestamp": e.begin.datetime.strftime("%I:%M %p"),
            "tokens": tokens,
            "summary": summary
        }
        events.append(event_block)
    return events

# Build Streamlit UI
st.title("Chronologue: Haircut Scheduling Suggestion")

ics_file = st.file_uploader("Upload your calendar (.ics)", type=["ics"])

if ics_file:
    with open("temp_calendar.ics", "wb") as f:
        f.write(ics_file.getbuffer())
    events = extract_events_and_tokens("temp_calendar.ics")

    st.markdown("### Your Events on Tuesday, May 13th")
    context_blocks = []
    for e in events:
        if "2025-05-13" in e["tokens"][0]:
            block = f"- {e['title']} at {e['timestamp']} {' '.join(e['tokens'])}"
            st.markdown(block)
            context_blocks.append(block)

    user_query = st.text_input("What would you like to ask the calendar agent?", "What time should I schedule a haircut next Tuesday?")

    if st.button("Suggest Time"):
        prompt = "You are a calendar-aware assistant. Consider the following context:\n"
        prompt += "\n".join(context_blocks)
        prompt += "\n\nThe barbershop is open from 10:00 AM to 6:30 PM.\n"
        prompt += f"\nUser query: {user_query}"

        with st.spinner("Thinking..."):
            res = openai.ChatCompletion.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_query}
                ]
            )
            reply = res["choices"][0]["message"]["content"].strip()
            st.success("Suggested Time:")
            st.markdown(reply)
