# CX Agent for Stanza Living

A virtual assistant for Stanza Living residents, powered by **LangChain**, **Groq AI**, and **Streamlit**. This assistant handles user queries, provides answers from FAQs, creates support tickets, and collects feedback.

---

## Overview

The CX Agent is designed to provide real-time support to Stanza Living residents. It classifies incoming queries, retrieves relevant answers from a FAQ database, and creates support tickets when needed.

---

## Core Components

- **LangGraph**  
  Manages the data flow and integrates Groq AI for intent classification.

- **Groq AI (via LangChain)**  
  Classifies queries into categories: `faq`, `ticket`, `payment`, `user_info`, and `fallback`.

- **Chroma**  
  A vector store for storing and retrieving FAQ data via semantic search.

- **Streamlit UI**  
  Provides an intuitive and interactive user interface for residents.

---

## Key Features

- **Query Classification**
  - `faq`: General questions (e.g., policies, services)
  - `ticket`: Support issues
  - `payment`: Rent or billing queries
  - `user_info`: Room number, check-in status, etc.
  - `fallback`: Unclear or uncategorized queries

- **FAQ Retrieval**  
  Matches user queries with existing FAQ responses using Chroma vector search.

- **Ticket Creation**  
  Automatically raises a support ticket if the issue cannot be resolved via FAQ.

- **Feedback Collection**  
  After each interaction, the user is asked if their query was resolved.

- **Reclassification on Feedback**  
  If unresolved, the issue is escalated or converted into a ticket.

---

## Implementation Flow

1. **User Query Input**  
   Example: _"When is my rent due?"_

2. **Intent Classification**  
   Groq AI classifies the query using LangChain routing logic.

3. **Response Handling**  
   - `faq`: Retrieve answer from FAQ
   - `ticket`: Create a support ticket
   - `payment` / `user_info`: Fetch specific user or billing details

4. **Feedback Request**  
   The system asks the user if the response resolved their issue.

5. **Escalation Flow**  
   If the feedback is negative, a ticket is generated or escalated further.

---

## 📁 Code Structure

### `app.py`
- Main CLI interface
- Prompts for user ID and query
- Handles query classification and feedback loop

### `faq_tool.py`
- Loads FAQs
- Uses Chroma for vector storage and retrieval
- Contains `initialize_vector_store()` for FAQ DB setup
- Integrates Groq AI for classification

### `langgraph_flow.py`
- Central routing logic with LangGraph
- Manages query flow based on classification
- Controls whether to return FAQ, trigger ticketing, or request feedback

---

## Example Interactions

```plaintext
User: When is my rent due?
Agent: Your rent is due on the 5th of each month.

User: My Wi-Fi is not working
Agent: A support ticket has been created for you. Your ticket ID is T1743954970.

Agent: Was this issue resolved?
User: Yes
Agent: Thank you for your feedback! Have a great day!
