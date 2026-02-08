# 🚀 Real Estate AI Workflow: Full Testing Guide

This guide provides a step-by-step plan to verify that all branches of your workflow (Search, Listing, and Support) are functioning correctly after the engine upgrades.

---

## 🛠️ Prerequisites
Before testing, ensure:
1.  **Server is Running**: `python -m uvicorn backend.app.api.main:app --host 0.0.0.0 --port 8000`
2.  **Database is Seeded**: You have run `python seed_data.py` successfully.
3.  **API Keys**: Your OpenAI/LiteLLM key is active.

---

## 🧪 Test Case 1: Tenant Branch (Property Search)
**Goal**: Verify that the AI identifies a search intent, routes to the Search Agent, and finds properties in Supabase.

*   **User Message**: `"I am looking for a studio in Gauthier"` (or `"Je cherche un studio à Maarif"`)
*   **What to look for in Terminal**:
    1.  `[RouterNode] Comparing 'SEARCH_RENTAL' equals 'SEARCH_RENTAL' -> True`
    2.  `[RouterNode] Routing to node: langchainAgent-1770562011651`
    3.  `[Universal Agent] Mode: PLANNER (Executing tools...)`
*   **Expected Response**: The AI should describe the studio near the Twin Center that we seeded earlier.

---

## 🧪 Test Case 2: Owner Branch (Property Listing)
**Goal**: Verify the AI identifies a listing intent, extracts a URL, scrapes data, and triggers a notification.

*   **User Message**: `"I want to list my property. Here is the link: https://www.avito.ma/fr/maarif/appartements/appartement_a_louer_5674312.htm"`
*   **What to look for in Terminal**:
    1.  `[RouterNode] Comparing 'LIST_PROPERTY' equals 'LIST_PROPERTY' -> True`
    2.  `[Web Scraper] Scraped content from avito.ma...`
    3.  `[Lead Formatter] Generated JSON for NocoDB...`
    4.  `[NotificationNode] SUCCESS: Lead alert sent to your email/phone.`
*   **Verification**: Check your NocoDB project to see if the new lead appeared in the table.

---

## 🧪 Test Case 3: Support Branch (General Inquiry)
**Goal**: Verify the AI identifies general questions and routes them to the Customer Support Agent.

*   **User Message**: `"What are your office hours and how can I contact you?"`
*   **What to look for in Terminal**:
    1.  `[RouterNode] Evaluation: GENERAL_INQUIRY -> True`
    2.  `[RouterNode] Routing to node: langchainAgent-1770564530252`
*   **Expected Response**: A polite response from the Customer Support agent explaining the services.

---

## 🔍 How to Read the Debug Logs
I have added high-visibility logs to help you trace the AI's "thought process":

| Log Prefix | Meaning |
| :--- | :--- |
| `[RouterNode]` | The "Brain" choosing which direction the conversation goes. |
| `[NodeFactory]` | Confirms the safe loading of your custom Real Estate nodes. |
| `[Universal Agent]` | Shows whether the agent is just talking (`SIMPLE`) or using tools (`PLANNER`). |

---

## 🛠️ Troubleshooting
*   **"No properties found"**: Ensure the `seed_data.py` script was run and you didn't see any `FAILURE` messages.
*   **"Wrong branch taken"**: Check the `Intent Classifier` node. If it fails to identify English, add more keywords to `intent_classifier.py` in the fallback section.
*   **"Missing Recipient"**: This means the prompt accidentally went to the Notification branch. Double-check your `If-Else` node connections in the Studio.

---
**Happy Testing!** 🏠✨
