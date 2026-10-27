# RAN-NEETI — Sports × Anime Intelligence Dashboard

A dark neon Streamlit dashboard with two separate workspaces:
- **Real Sports Lab** — choose a sport, compare Side A vs Side B, and request source-grounded AI research.
- **Anime & Fictional Battles** — compare two characters/fighters; portrait lookup is attempted automatically.
- **Recent Reports** — session report history and Markdown downloads.
- Major moves, counters, risks, turning points, win conditions, uncertainty, and sources are requested in every AI report.

## Run online (no Python needed on your device)
1. Create a GitHub repository and upload all files in this folder.
2. Deploy it on [Streamlit Community Cloud](https://share.streamlit.io/) with `app.py` as the main file.
3. In app settings → Secrets, add `GEMINI_API_KEY = "your_key"` (get a key from Google AI Studio).
4. Redeploy and try both dashboards.

## Local run (optional)
```bash
pip install -r requirements.txt
streamlit run app.py
```

## What is automatic?
- Character portraits are searched using Jikan's public anime character API.
- General sports/team/athlete image and short-description lookup uses Wikipedia's public API.
- With a valid Gemini API key and available quota, the AI requests Google Search grounding for matchup research and includes source links returned by the service.
- The user supplies the two comparison names and chooses a sport in the sports dashboard; there is no preloaded list of all teams.

## Important limitations
- Public APIs can be rate-limited, unavailable, or return a wrong image/result. Always check the resolved identity.
- Gemini/Search access depends on current model availability, key permissions, quota and Google terms. The app does not scrape Google's AI Overview UI.
- AI percentages are estimates. Unless a sport-specific model has been separately trained and evaluated on historical data, do not present these percentages as validated statistical forecasts.
- Fictional matchup probabilities are subjective interpretations of source-backed feats and declared assumptions.
- Check source licences, attribution and API terms before academic or public deployment.
- No live deployment is created by this ZIP. Deploy it to receive a public URL.

## Visual assets
`static/neon_sports_anime_background.png` is an original generated sports/anime-inspired banner asset used in the dashboard. The app also attempts to retrieve relevant portraits from public character/article data sources at query time.
