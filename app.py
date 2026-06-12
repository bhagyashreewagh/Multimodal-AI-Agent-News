import streamlit as st
import requests
import xml.etree.ElementTree as ET
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import anthropic
import os

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

nltk.download("vader_lexicon", quiet=True)
sia = SentimentIntensityAnalyzer()

def fetch_news_rss(query: str, max_articles: int = 6):
    url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"
    resp = requests.get(url, timeout=10)
    root = ET.fromstring(resp.content)
    articles = []
    for item in root.iter("item"):
        title = item.findtext("title", "")
        description = item.findtext("description", "") or ""
        link = item.findtext("link", "")
        source_el = item.find("source")
        source = source_el.text if source_el is not None else "Unknown"
        text = description.replace("<![CDATA[", "").replace("]]>", "").strip()
        if title:
            articles.append({"title": title, "text": text or title, "url": link, "source": source})
        if len(articles) >= max_articles:
            break
    return articles

def summarize(text: str) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=120,
        messages=[{"role": "user", "content": f"Summarize this news snippet in 2 sentences:\n\n{text}"}],
    )
    return msg.content[0].text.strip()

def sentiment_label(scores):
    c = scores["compound"]
    if c >= 0.05:
        return "Positive", "#22c55e"
    elif c <= -0.05:
        return "Negative", "#ef4444"
    return "Neutral", "#94a3b8"

st.set_page_config(page_title="AI News Agent", page_icon="📰", layout="wide")

st.markdown("""
<style>
  .card{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1rem}
  .badge{display:inline-block;padding:.2rem .7rem;border-radius:999px;font-size:.75rem;font-weight:600;color:#fff}
  .source{font-size:.8rem;color:#6b7280}
</style>
""", unsafe_allow_html=True)

st.title("📰 AI News Agent")
st.markdown("Fetches live headlines, summarizes with Claude AI, and analyzes sentiment.")

col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("Topic", value="Artificial Intelligence", placeholder="e.g. Machine Learning, Climate")
with col2:
    n = st.selectbox("Articles", [4, 6, 8, 10], index=1)

if st.button("Fetch & Analyze", type="primary"):
    with st.spinner("Fetching news..."):
        articles = fetch_news_rss(query, n)

    if not articles:
        st.warning("No articles found. Try a different topic.")
    else:
        st.markdown(f"### Results for **{query}**")
        for art in articles:
            with st.spinner(f"Summarizing: {art['title'][:60]}..."):
                summary = summarize(art["text"])
            scores = sia.polarity_scores(art["text"])
            label, color = sentiment_label(scores)

            st.markdown(f"""
<div class="card">
  <p class="source">{art['source']}</p>
  <b><a href="{art['url']}" target="_blank" style="color:#1d4ed8;text-decoration:none">{art['title']}</a></b>
  <p style="margin:.6rem 0;color:#374151">{summary}</p>
  <span class="badge" style="background:{color}">{label}</span>
  <span style="font-size:.78rem;color:#9ca3af;margin-left:.5rem">compound: {scores['compound']:.2f}</span>
</div>
""", unsafe_allow_html=True)
