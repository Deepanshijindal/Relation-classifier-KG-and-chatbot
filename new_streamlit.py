import streamlit as st
from streamlit_chat import message
import requests
import openai

openai.api_key_path = "./API_KEY.txt"

chat_history = [ {"role": "system", "content":
              '''given Neo4j graph database is in the format {   "identity": 0,   "labels": [     "Person"   ],   "properties": {     "name": "Samuel Penfield Taylor"   },   "elementId": "0" } 
              {   "identity": 1,   "labels": [     "Location"   ],   "properties": {     "name": "New York"   },   "elementId": "1" } 
 {
  "identity": 24,
  "start": 33,
  "end": 34,
  "type": "NATIONALITY",
  "properties": {

  },
  "elementId": "24",
  "startNodeElementId": "33",
  "endNodeElementId": "34"
}{
  "identity": 33,
  "labels": [
    "Person"
  ],
  "properties": {
    "name": "Thomas Alva Edison"
  },
  "elementId": "33"
}{
  "identity": 35,
  "labels": [
    "Person"
  ],
  "properties": {
    "name": "Heinrich Müller"
  },
  "elementId": "35"
}{
  "identity": 25,
  "start": 35,
  "end": 36,
  "type": "EMPLOYEE_OR_MEMBER_OF",
  "properties": {

  },
  "elementId": "25",
  "startNodeElementId": "35",
  "endNodeElementId": "36"
}{
  "identity": 37,
  "labels": [
    "Person"
  ],
  "properties": {
    "name": "Robert Danisch"
  },
  "elementId": "37"
}{
  "identity": 26,
  "start": 37,
  "end": 38,
  "type": "EDUCATED_AT",
  "properties": {

  },
  "elementId": "26",
  "startNodeElementId": "37",
  "endNodeElementId": "38"
}{
  "identity": 39,
  "labels": [
    "Person"
  ],
  "properties": {
    "name": "Chris"
  },
  "elementId": "39"
}{
  "identity": 27,
  "start": 39,
  "end": 40,
  "type": "DATE_OF_BIRTH",
  "properties": {

  },
  "elementId": "27",
  "startNodeElementId": "39",
  "endNodeElementId": "40"
}{
  "identity": 40,
  "labels": [
    "Date"
  ],
  "properties": {
    "name": "January 23, 1989"
  },
  "elementId": "40"
}{
  "identity": 41,
  "labels": [
    "Person"
  ],
  "properties": {
    "name": "She"
  },
  "elementId": "41"
}{
  "identity": 28,
  "start": 41,
  "end": 42,
  "type": "EDUCATED_AT",
  "properties": {

  },
  "elementId": "28",
  "startNodeElementId": "41",
  "endNodeElementId": "42"
}{
  "identity": 42,
  "labels": [
    "University"
  ],
  "properties": {
    "name": "University of Denver"
  },
  "elementId": "42"
}{
  "identity": 30,
  "start": 45,
  "end": 46,
  "type": "NATIONALITY",
  "properties": {

  },
  "elementId": "30",
  "startNodeElementId": "45",
  "endNodeElementId": "46"
}{
  "identity": 47,
  "labels": [
    "Person"
  ],
  "properties": {
    "name": "Zak Brown"
  },
  "elementId": "47"
}{
  "identity": 50,
  "labels": [
    "Organization"
  ],
  "properties": {
    "name": "UQ"
  },
  "elementId": "50"
}{
  "identity": 52,
  "labels": [
    "Organization"
  ],
  "properties": {
    "name": "Advanced Forming and Railway Mechanics"
  },
  "elementId": "52"
}{
  "identity": 54,
  "labels": [
    "Date"
  ],
  "properties": {
    "name": "February 22, 1960"
  },
  "elementId": "54"
}{
  "identity": 56,
  "labels": [
    "Date"
  ],
  "properties": {
    "name": "1876"
  },
  "elementId": "56"
}{
  "identity": 58,
  "labels": [
    "University"
  ],
  "properties": {
    "name": "University of Hong Kong"
  },
  "elementId": "58"
}{
  "identity": 28,
  "labels": [
    "Country"
  ],
  "properties": {
    "name": "American"
  },
  "elementId": "28"
}
'''} ]

def res_generated_chat(prompt):
    chat_history.append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )
    response = completion.choices[0].message.content
    return response

st.title("NLU Assignment--2")

if 'generated_responses' not in st.session_state:
    st.session_state['generated_responses'] = []
if 'user_inputs' not in st.session_state:
    st.session_state['user_inputs'] = []

user_input = st.text_input("You:", key='input')
if user_input:
    generated_response = res_generated_chat(user_input)
    st.session_state['user_inputs'].append(user_input)
    st.session_state['generated_responses'].append(generated_response)

if st.session_state['generated_responses']:
    for i in range(len(st.session_state['generated_responses'])-1, -1, -1):
        if i % 2 == 0:
            message(st.session_state['generated_responses'][i])
        else:
            message(st.session_state['user_inputs'][i], is_user=True)
