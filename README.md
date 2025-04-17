## Chronologue: Personal Memory with Calendar API integration 🗓️

> *Memory of user context conditions the future distribution of responses that a language model will sample from.*

> *We make ourselves intelligent by designing environments that contain relevant information and make them accessible to our future selves.*  
> — [Donald Norman](https://jnd.org/)

> *Time is a core substrate for intelligent behavior.* 


### Introduction 

As we develop environments for agents, agents will design environments for us. Enabling this feedback loop between user behavior, interface design, and agent orchestration and scheduling is one of the defining challenges and promises of the next phase of model development. 

We aim to build agents that not only plan and act on our behalf but also structure and store information that are accessible and steerable for developers. That is, we need to focus on designing environments that human users trust and readily interact with. 

Calendars are a familiar interface for storing event information, planning, and externalizing memory for individuals and organization. 

<img src="figures/calendar-example.png" width="400">

This repository converts structured memory traces (stored as `.json`) into `.ics` calendar files, enabling users to visualize and revisit key events — particularly conversation history with language models — within their preferred calendar tools (Apple Calendar, Google Calendar, Outlook).


##### Key Features and Workflow 

- Parses memory trace JSON files from the `data/conversation/raw` folder  
- Validates trace structure against a custom schema  
- Formats `.ics` events with standardized UID, timestamp, and metadata  
- Embeds a summary and direct URL link to the original chat in the event `DESCRIPTION`  
- Outputs `.ics` files compatible with calendar APIs  

<img src="figures/json-ics.png" width="300">

---

### Getting Started 

1. **Clone the Repository** 

```bash 
git clone https://github.com/dr2633/Chronologue.git
cd Chronologue
```

2. **Set your API Keys**

In .env file: 

```
OPENAI_API_KEY=your-openai-key
CLAUDE_API_KEY=your-anthropic-key
GEMINI_API_KEY=your-gemini-key
LLAMA_API_KEY=your-meta-key

GOOGLE_CLIENT_CREDENTIALS=calendar/credentials.json
GOOGLE_TOKEN_FILE=calendar/token.json
```

Set your Calendar API for Integration by following the [Google Calendar API setup](https://developers.google.com/calendar/api/quickstart/python). 


3. **Convert from JSON Chat History to ICS Format for Calendar** 

Run the following script to transform sample `.json` data to `.ics`: 

```bash 
python modules/export_ics.py
```

Optional: Generate embeddings for conversation history

```bash
python modules/embeddings.py
```

4. **Convert Calendar Data to Model Input** 

Run the following script to transform sample `.ics` files to `.json`: 

```bash
python modules/import_ics.py
```

In the CLI, you can:
- Load a synthetic user trace
- Build embeddings
- Run a planning query
- (Optionally) schedule a reminder in your Google Calendar

### System Overview

This system is organized into modular components for:

- **Memory**: storage and structuring of timestamped user traces
- **Calendar**: importing and scheduling events with the Google Calendar API
- **Retrieval**: embedding and FAISS-based similarity search
- **Reasoning**: ReAct-style prompt generation using memory + calendar context
- **Evaluation**: manifold analysis (MMCR) and memory trace logging


See [dataset guide](../data/dataset-guide.md) for more details and description of fields included as part of standardized `.ics` format. 

---

### JSON and Calendar ICS Interoperability 

While this repository enables exporting `.json` memory traces into `.ics` calendar files for visualization and archival, the integration can also work in reverse.


By ingesting `.ics` files from tools like Google Calendar or Apple Calendar, agents can:

- Ground responses in the user’s actual schedule and past events  
- Retrieve relevant context by aligning timestamps and event metadata  
- Prioritize upcoming tasks or recall prior interactions based on calendar entries  

This workflow allows for persistent, time-aware context grounding, enabling language models to condition outputs based on a user’s routines, workflows, and past conversations.

--- 

### Example: Model Output Converted to iCalendar Format
Suppose a model generates the following JSON:
```json
{
  "title": "Project Sync: Inference Pipeline",
  "description": "Check progress on GPU inference benchmarks.",
  "start": "2025-04-11T14:00:00Z",
  "end": "2025-04-11T14:30:00Z",
  "location": "https://zoom.us/my/benchmark-sync",
  "organizer_email": "agent@memorysystem.ai"
}
```
You would translate this to:
```ics
BEGIN:VEVENT
DTSTART:20250411T140000Z
DTEND:20250411T143000Z
SUMMARY:Project Sync: Inference Pipeline
DESCRIPTION:Check progress on GPU inference benchmarks.
LOCATION:https://zoom.us/my/benchmark-sync
UID:project-sync-20250411@memorysystem.ai
DTSTAMP:20250410T230000Z
ORGANIZER;CN=Memory Agent:mailto:agent@memorysystem.ai
STATUS:CONFIRMED
TRANSP:OPAQUE
END:VEVENT
```






