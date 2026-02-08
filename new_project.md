

Technical & Logic Documentation (English Version)
1. System Overview

Project Name: EasySpace AI Real Estate Automation.
Core Objective: A fully automated AI agency that manages property rentals in Casablanca. It handles lead qualification, property matching, data extraction, and CRM updates without human intervention.

2. Technical Stack

Orchestration: n8n (Workflow Automation).

LLM Gateway: LiteLLM (unified API for GPT-4o-mini).

Database (CRM): NocoDB (Structured leads and property inventory).

Vector Database: Supabase (PGVector) for semantic property search.

Memory: Redis (Session persistence and context retention).

Transcription: OpenAI Whisper (via API) for voice-to-text messages.

Scraping: Firecrawl & Gradio API (for extracting data from Avito/Mubawab links).

3. Architecture & Logical Flow

The system follows a Modular Agentic Architecture split into four main tiers:

A. The Intelligent Router (Main Gateway)

Input Handling: Receives Webhook data (Text, Audio, or Links).

Pre-processing: If audio is detected, it triggers a transcription sub-flow.

Classification: An AI Agent analyzes the intent and classifies the user into:

Tenant: Looking to rent.

Owner: Looking to list a property.

Partner: Agent/Broker seeking collaboration.

B. Tenant Module (Matching & RAG)

Logic: Uses Retrieval-Augmented Generation (RAG).

Search: Queries Supabase using vector embeddings to find the top 2 properties matching the user's budget and neighborhood.

Output: Generates a "Carousel" JSON structure to display images and details interactively on the frontend.

Tools: Includes a "Scheduling Tool" (RDV) to book physical visits.

C. Owner Module (Onboarding & OCR)

Logic: Conversational form filling.

Data Extraction: If an owner sends a link (Mubawab/Avito), the system scrapes the listing details (Price, Rooms, Square footage) automatically.

CRM Integration: Directly creates and updates rows in NocoDB to keep the inventory live.

D. Partner Module (Lead Generation)

Logic: Simple B2B lead capture.

Storage: Saves agent credentials to a specialized NocoDB table for manual follow-up.

