# chatbot_travel_rasa

This project was developed as part of a university assignment on dialog systems. The goal was to build a task-oriented chatbot using Rasa Open Source that could actually be useful for travel planning through natural conversation.

---

## 1. Chatbot Domain and Motivation

### Domain

I chose to build a travel assistance chatbot - basically a digital travel companion that helps with trip planning by providing:

- travel destination suggestions
- current weather conditions
- local time in different cities
- upcoming events and activities 

### Motivation

Honestly, I've always found trip planning a bit tedious. You end up with like 10 browser tabs open - one for weather, one for events, another for time zones, etc. So the idea of having a chatbot that consolidates all this information in one conversational interface seemed both practical and interesting to build.
From a technical perspective, the travel domain turned out to be a great choice because it let me work with multiple external APIs, handle different types of user intents, and experiment with both rule-based and machine learning approaches to dialog management. Plus, travel-related conversations feel natural and intuitive, which made testing the bot actually enjoyable.

---

## 2. Implemented Scenarios and Chatbot Functionalities

### 2.1 Destination Recommendation Scenario

Users can ask the chatbot for destination ideas.

**Example:**
```
User: destinations  
Bot: Here are some destinations in Europe: Paris, Rome, Barcelona, London, Athens, Berlin, Amsterdam
```

This was the simplest scenario - mostly to demonstrate basic intent recognition and static responses.

---

### 2.2 Weather Information Scenario

Users can check real-time weather for any city.

**Example:**
```
User: weather in Athens  
Bot: The weather in Athens is 6°C with broken clouds.
```

This scenario was more interesting because it involved:

extracting the city name from the user's message
storing it in a slot
calling the OpenWeather API
generating a response with live data

---

### 2.3 Local Time Scenario

Users can ask what time it is in different cities.

**Example:**
```
User: time in Berlin  
Bot: Local time in Berlin is 21:34.
```

This scenario demonstrates:

- city-to-timezone mapping
- REST API usage
- real-time data processing

---

### 2.4 Events Information Scenario

Users can discover what's happening(events) in a city.

**Example:**
```
User: events in London  
Bot: Upcoming events in London:
• Gladiators Live  
• London Dungeon - Standard Entry
```

This was probably the trickiest scenario because the Ticketmaster API doesn't always have data for every city, so I had to add fallback messages for when nothing shows up.

---

## 3. Integrated Data Sources and Rationale

The chatbot pulls data from three different APIs:

### OpenWeather API
What it does: Provides real-time weather data
Why I picked it: It's reliable, well-documented, and has a generous free tier. Pretty much the go-to for weather data.

### WorldTimeAPI
What it does: Returns local time based on timezone
Why I picked it: Super simple to use, no authentication needed, and it just works.

### Ticketmaster Discovery API
What it does: Lists upcoming events by location
Why I picked it: Good global coverage and relevant for travel planning. Who doesn't want to know what's happening in the city they're visiting?

All APIs are accessed via REST requests using the Python `requests` library.

---

## 4. Challenges and Solutions

### Challenge 1: Entity ambiguity between cities

Turns out there's a Rome in Italy AND a Rome in New York. When I first tested the events API, it kept returning results for the wrong Rome!
Solution:
I created a predefined mapping of cities to their countries (e.g., Rome → Italy, Paris → France) to filter out the wrong results. Not the most scalable solution, but it works for the cities I'm supporting.

---

### Challenge 2: Inconsistent API coverage

The Ticketmaster API sometimes returns zero events for certain cities, which initially caused the bot to give weird empty responses.
Solution:
Added proper checks and fallback messages like "Sorry, I couldn't find any upcoming events in [city]." Better to admit you don't have data than to fail silently.

---

### Challenge 3: Dialog flow conflicts

Early on, I ran into this frustrating issue where my rules and stories were conflicting, causing the bot to make contradictory predictions about what to do next.
Solution:
After some trial and error (and reading through Rasa docs), I simplified my rules and made sure there was a clear separation between rule-based flows and story-based ones. Lesson learned: don't over-complicate your dialog policies.

---

### Challenge 4: GitHub repository size

The trained models Rasa generates are huge, and I initially pushed them to GitHub which made the repo unnecessarily bloated.
Solution:
Added models/, .rasa/, and .venv/ to .gitignore. Much cleaner now.

---

## 5. API Keys and Configuration Instructions

To run the chatbot locally, the following API keys are required:

### Required API Keys

- OpenWeather API key  
- Ticketmaster Discovery API key  

### Configuration

API keys must be inserted in `actions/actions.py`:

No environment variables are required for this project.

---

## 6. Example Runs

```
User: destinations  
Bot: Paris, Rome, Barcelona, London, Athens, Berlin, Amsterdam
```

```
User: weather in Rome  
Bot: The weather in Rome is 8°C with scattered clouds.
```

```
User: time in Paris  
Bot: Local time in Paris is 20:45.
```

```
User: events in Barcelona  
Bot: Upcoming events in Barcelona...
```

---

## 7. Dialog Policy Experimentation (Optional – Bonus)

What I tried
I stuck mostly with Rasa's default configuration but experimented with the balance between RulePolicy and TEDPolicy.

DIETClassifier handles intent recognition and entity extraction
RulePolicy for predictable, deterministic flows (like greetings)
TEDPolicy for more complex multi-turn conversations

Why this approach?
I wanted predictable behavior for simple commands (like "destinations") while still maintaining flexibility for actual conversations. Pure rule-based felt too rigid, but pure ML sometimes gave inconsistent results.
What I learned

Rules make responses more consistent, but too many rules kill the conversational flow
TEDPolicy is surprisingly good at generalizing from training stories
Finding the right balance took more iteration than I expected
When rules and stories conflict, things get messy fast

The sweet spot seems to be using rules for well-defined interactions and letting TEDPolicy handle everything else.

---

## 8. Technologies Used

- Python 3
- Rasa Open Source
- Rasa SDK
- REST APIs (OpenWeather, WorldTimeAPI, Ticketmaster)

---

## 9. Author

**Nikos Vasilopoulos**

University project developed for academic purposes.
