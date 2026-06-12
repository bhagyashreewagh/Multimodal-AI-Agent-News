# AI News Agent

Type a topic, get a curated news feed with AI summaries and sentiment scores in seconds.

Fetches live headlines via Google News RSS, summarizes each article with Claude Haiku, and classifies sentiment with VADER — all in one Streamlit app.

---

## Quick Start

```bash
pip install -r requirements.txt

export ANTHROPIC_API_KEY=your_key_here
streamlit run app.py
```

Open http://localhost:8501, type a topic (e.g. "Machine Learning"), choose how many articles, and click **Fetch & Analyze**.

---

## How it works

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

## Repo Structure

```
app.py            Streamlit UI and full pipeline
agent-Copy1.py    Original Python script (no UI)
requirements.txt
render.yaml       Render deployment config
```

---

## Design Choices

**Claude Haiku for summaries.** Produces clean, readable two-sentence summaries at low latency and cost. Handles domain-specific language (ML, finance, healthcare) without hallucinating key facts from the article.

**VADER for sentiment.** A rule-based lexicon model that runs locally with no API call and near-zero latency. It handles news headlines well. Using an LLM for sentiment would add cost and round-trip time for no meaningful accuracy gain.

**Google News RSS over NewsAPI.** No registration, no rate limits, always fresh. The RSS feed includes everything needed: headline, description, source, and link.

---

## Tech Stack

- Python
- Streamlit (UI)
- Claude Haiku via Anthropic API (summarization)
- VADER / NLTK (sentiment analysis)
- Google News RSS (live news feed)
