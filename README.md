# AI News Agent

A personalized news aggregator that fetches live headlines, summarizes each article with Claude AI, and classifies sentiment using VADER. Type a topic, get a curated feed with summaries and sentiment scores in seconds.

---

## What it does

Staying current on a topic like AI or data engineering means reading a lot, and most of it is noise. This agent cuts through: it fetches real headlines, tells you what each article actually says in two sentences, and flags whether the tone is positive, negative, or neutral before you click.

```
Topic input
    |
    v
Google News RSS (live headlines, no API key needed)
    |
    v
Claude Haiku (2-sentence summary per article)
    |
    v
VADER (sentiment: Positive / Negative / Neutral + compound score)
    |
    v
Streamlit feed (source, summary, badge, link)
```

---

## Running the App

```bash
pip install -r requirements.txt

export ANTHROPIC_API_KEY=your_key_here
streamlit run app.py
```

Open http://localhost:8501, type a topic (e.g. "Machine Learning"), choose how many articles, and click **Fetch & Analyze**.

---

## Repo Structure

```
app.py              Streamlit UI and full pipeline
agent-Copy1.py      Original Python script (no UI)
requirements.txt
render.yaml         Render deployment config
```

---

## Design Choices

**Claude over GPT for summarization:** Claude Haiku produces clean, readable two-sentence summaries at low latency and cost. The model handles domain-specific language (ML, finance, healthcare) without hallucinating key facts.

**VADER for sentiment:** VADER is a rule-based lexicon model that runs locally with no API call and no latency. It handles news headlines well. Using an LLM for sentiment would add cost and latency with no meaningful accuracy gain for this use case.

**Google News RSS over NewsAPI:** No registration, no rate limits, always fresh. The RSS feed provides everything needed: headline, description, source, and link.

---

## Tech Stack

- Python
- Streamlit (UI)
- Claude Haiku via Anthropic API (summarization)
- VADER / NLTK (sentiment analysis)
- Google News RSS (live news feed)
