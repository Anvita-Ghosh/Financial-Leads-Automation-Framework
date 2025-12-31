**Overview**

This project is an end-to-end pipeline that automates grant discovery and matches funding opportunities to institutional projects. It is designed to reduce the manual effort involved in searching, filtering, and identifying relevant grants for startups and research organisations.

The system scrapes real grant descriptions from funding portals, builds semantic understanding of both grants and project requirements, and then computes similarity scores to recommend the most relevant funding options.


**What the System Does**

Scrapes grant opportunities from reliable funding sources

Cleans and structures grant descriptions into usable data

Extracts meaningful keywords from grants using AI models (Ollama / Mistral)

Extracts representative keywords from institutional project briefs (KeyBERT)

Uses TF-IDF and cosine similarity to compute relevance

Outputs ranked funding recommendations


**Project Structure**

1_extract_proj.py       Extracts project text and generates project keywords

2_scrape_grants.py      Scrapes grants and stores title + description

3_agentic_ai.py         Generates semantic keywords for grants using AI

4_cosinesim_output.py   Matches projects to grants and ranks results
