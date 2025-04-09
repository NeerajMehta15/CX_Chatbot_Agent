CX Agent for Stanza Living
A virtual assistant for Stanza Living residents, powered by LangChain, Groq AI, and Streamlit. This assistant handles user queries, provides answers from the FAQ, creates support tickets, and collects feedback.

Overview
This system is designed to provide support to Stanza Living residents. The agent will classify user queries, retrieve relevant answers from an FAQ database, and create support tickets when necessary.

Core Components
LangChain:

Manages the flow of data and integrates Groq AI for intent classification.

Groq AI (via LangChain):

A language model used to classify queries into different categories such as faq, ticket, payment, user_info, and fallback.

Chroma:

A vector store to handle the storage and retrieval of FAQ data. It ensures that we can efficiently match queries with relevant answers.

Streamlit UI:

Provides an interactive interface for users to interact with the CX Agent, enter queries, and receive responses.

Key Features
Query Classification:

Classifies user queries into categories: faq, ticket, payment, user_info, and fallback.

FAQ: Queries related to general information such as policies, services, etc.

Ticket: Issues that require support or action (e.g., service requests).

Payment: Rent and billing-related inquiries.

User Info: Queries about personal details such as room number, check-in status, etc.

Fallback: Handles undefined or unclear queries.

FAQ Retrieval:

Users can ask questions, and if the query matches a FAQ, the system fetches the appropriate answer.

Ticket Creation:

If the issue is not resolved through the FAQ, a support ticket is created for further assistance.

Feedback Collection:

After resolving a query, the system collects feedback on the resolution (e.g., whether the issue was solved or not).

Implementation Flow
User Query Input: The user enters a query such as "When is my rent due?".

Intent Classification:

The system uses Groq AI via LangChain to classify the query. The classification model checks the query and assigns it a category, such as faq, ticket, etc.

FAQ Retrieval or Ticket Creation:

If the query is classified as faq, the system retrieves an answer from the FAQ database.

If it’s classified as ticket, a support ticket is created, and the user is given a ticket ID.

Feedback Request:

After providing an answer or creating a ticket, the system requests feedback from the user to understand if the issue was resolved.

Reclassification on Feedback:

If the feedback indicates the issue is unresolved, the system reverts to ticketing or escalates the issue accordingly.

Code Flow
app.py:

The main entry point. It runs a CLI interface where users can input their queries and interact with the agent.

The system prompts users for their user ID, collects queries, and handles the feedback.

faq_tool.py:

Contains functions to load and process FAQ data using Chroma for storing vectors and retrieving them when queried.

The initialize_vector_store function loads the FAQ database and stores it in the Chroma vector store.

It then uses the Groq AI model for classifying the intent of each user query.

langgraph_flow.py:

Coordinates the different components using LangChain to control the flow and invoke specific actions based on the classified intent.

Handles the decision-making process, such as deciding between answering an FAQ or creating a support ticket.

Feedback Handling:

After receiving a response (whether from FAQ or ticketing), the system asks the user for feedback. If the user’s issue is unresolved, it triggers the ticket creation flow.

Example Interactions
User Query: "When is my rent due?"

Agent Response: "Your rent is due on the 5th of each month."

User Query: "My Wi-Fi is not working"

Agent Response: "A support ticket has been created for you. Your ticket ID is T1743954970."

Feedback: Was this issue resolved?

User Answer: "Yes"

Agent Response: "Thank you for your feedback! Have a great day!"