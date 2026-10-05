"""FastAPI app exposing the skin clinic campaign analysis."""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

from analysis import load_data, run_analysis

app = FastAPI(title="Skin Clinic Campaign Analysis", version="1.0")

DF = load_data()
RESULTS = run_analysis(DF)

STYLE = """
<style>
  body { font-family: -apple-system, Segoe UI, Roboto, sans-serif; max-width: 860px;
         margin: 40px auto; padding: 0 16px; color: #222; background: #fafafa; }
  h1 { color: #7a3e6b; } h2 { margin-top: 36px; font-size: 1.1rem; color: #444; }
  table { border-collapse: collapse; width: 100%; background: #fff;
          box-shadow: 0 1px 3px rgba(0,0,0,.08); }
  th, td { padding: 10px 14px; text-align: left; border-bottom: 1px solid #eee; }
  th { background: #7a3e6b; color: #fff; font-weight: 600; }
  tr:hover td { background: #f6eef4; }
  .note { color: #666; font-size: .9rem; }
</style>
"""


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/campaign-analysis")


@app.get("/campaign-analysis", response_class=HTMLResponse)
def campaign_analysis():
    """Response-rate tables rendered as HTML."""
    sections = "".join(
        f"<h2>{name}</h2>{table.to_html(index=False, border=0)}"
        for name, table in RESULTS.items()
    )
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Campaign Analysis</title>{STYLE}</head><body>
<h1>Skin Clinic Campaign Response Analysis</h1>
<p class="note">Based on {len(DF):,} customers. Response rate = responders / customers in segment.
JSON version: <a href="/campaign-analysis/json">/campaign-analysis/json</a></p>
{sections}</body></html>"""


@app.get("/campaign-analysis/json")
def campaign_analysis_json():
    """Same results as JSON."""
    return {name: table.to_dict(orient="records") for name, table in RESULTS.items()}


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}
