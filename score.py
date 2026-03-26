#!/usr/bin/env python3
"""
score.py — LLM-based AI exposure scoring for occupations.

Uses OpenAI GPT-4 to rate each occupation's exposure to AI disruption
on a 0-10 scale, considering Singapore's specific economic context.

Outputs:
- scores.json: AI exposure scores with rationales (incremental checkpointing)
"""

from openai import OpenAI
import json
import time
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OCCUPATIONS_JSON = Path("occupations.json")
SCORES_JSON = Path("scores.json")

SYSTEM_PROMPT = """
You are an expert analyst evaluating how exposed different occupations are to AI in the Singapore economy.

Rate the occupation's overall **AI Exposure** on a scale from 0 to 10.

AI Exposure measures: how much will AI reshape this occupation? Consider both direct effects
(AI automating tasks currently done by humans) and indirect effects (AI making each worker
so productive that fewer are needed).

A key signal is whether the job's work product is fundamentally digital. If the job can be
done entirely from a computer — writing, coding, analyzing, communicating — AI exposure is
inherently high (7+). Physical presence, manual skill, and real-time human interaction in
unpredictable environments are natural barriers to AI.

Consider Singapore's specific context: the city-state's highly digitised economy, strong
service sector orientation, and concentration of high-skill PME (Professional, Manager,
Executive) roles may mean higher average AI exposure than the US.

Calibration anchors (0–10):
- 0–1: Minimal — almost entirely physical/hands-on (roofers, cleaners, construction laborers)
- 2–3: Low — mostly physical with minor digital tasks (electricians, nurses, mechanics)
- 4–5: Moderate — significant mix of physical and knowledge work (nurses, police, pilots)
- 6–7: High — predominantly knowledge work with some human judgment (teachers, managers, accountants)
- 8–9: Very high — almost entirely digital (software developers, analysts, designers, paralegals)
- 10: Maximum — routine digital information processing (data entry, telemarketers)

Respond with ONLY a JSON object, no other text:
{"exposure": <0-10>, "rationale": "<2-3 sentences>"}
"""


def score_occupation(client, occupation: dict) -> dict:
    """Score a single occupation using OpenAI GPT-4."""
    text = f"""
Occupation: {occupation['title']}
SSOC Code: {occupation['ssoc_code']}
Major Group: {occupation['major_group_label']}
Description: {occupation['description']}
"""
    
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=300,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    )
    
    content = response.choices[0].message.content.strip()
    
    # Strip markdown fences if present
    if content.startswith("```"):
        lines = content.split("\n")
        # Remove first line (```json or ```)
        if lines[0].strip() in ["```json", "```"]:
            lines = lines[1:]
        # Remove last line (```)
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines).strip()
    
    return json.loads(content)


def main():
    print("AI Exposure Scoring Pipeline")
    print("=" * 60)
    
    # Check API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("✗ Error: OPENAI_API_KEY not set")
        print("  Set it in .env or export OPENAI_API_KEY=your_key")
        return
    
    client = OpenAI(api_key=api_key)
    
    # Load occupations
    if not OCCUPATIONS_JSON.exists():
        print(f"✗ Error: {OCCUPATIONS_JSON} not found")
        print("  Run: uv run python parse_ssoc.py")
        return
    
    with open(OCCUPATIONS_JSON) as f:
        occupations = json.load(f)
    
    print(f"✓ Loaded {len(occupations)} occupations")
    
    # Load existing scores (incremental checkpoint)
    scores = {}
    if SCORES_JSON.exists():
        with open(SCORES_JSON) as f:
            for s in json.load(f):
                scores[s["ssoc_code"]] = s
    
    already_scored = len(scores)
    remaining = len(occupations) - already_scored
    
    print(f"✓ Already scored: {already_scored}")
    print(f"  Remaining: {remaining}")
    
    if remaining == 0:
        print("\n✓ All occupations already scored!")
        return
    
    # Estimate cost and time
    cost_per_call = 0.005  # ~$0.005 per call (GPT-4o)
    estimated_cost = remaining * cost_per_call
    estimated_time_min = remaining * 0.4 / 60  # ~0.4s per call including rate limit
    
    print(f"\nEstimated:")
    print(f"  API calls: {remaining}")
    print(f"  Cost: ${estimated_cost:.2f}")
    print(f"  Time: ~{estimated_time_min:.1f} minutes")
    
    input("\nPress Enter to continue (Ctrl+C to cancel)...")
    
    print(f"\nScoring {remaining} occupations...")
    print("(Progress saved after each occupation)\n")
    
    start_time = time.time()
    scored_count = 0
    
    for i, occ in enumerate(occupations):
        code = occ["ssoc_code"]
        if code in scores:
            continue
        
        print(f"[{i+1}/{len(occupations)}] {occ['title']}...", end=" ", flush=True)
        
        try:
            result = score_occupation(client, occ)
            scores[code] = {
                "ssoc_code": code,
                "title": occ["title"],
                "exposure": result["exposure"],
                "rationale": result["rationale"],
            }
            print(f"exposure={result['exposure']}")
            scored_count += 1
        except Exception as e:
            print(f"ERROR: {e}")
            continue
        
        # Save checkpoint after each occupation
        with open(SCORES_JSON, "w") as f:
            json.dump(list(scores.values()), f, indent=2, ensure_ascii=False)
        
        # Rate limit
        time.sleep(0.3)
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 60)
    print(f"✓ Scoring complete!")
    print(f"  Scored: {scored_count} new occupations")
    print(f"  Total: {len(scores)} occupations")
    print(f"  Time: {elapsed / 60:.1f} minutes")
    print(f"  Saved to: {SCORES_JSON}")
    
    # Statistics
    exposures = [s["exposure"] for s in scores.values()]
    avg_exposure = sum(exposures) / len(exposures) if exposures else 0
    
    print(f"\nExposure statistics:")
    print(f"  Average: {avg_exposure:.1f}")
    print(f"  Min: {min(exposures) if exposures else 0}")
    print(f"  Max: {max(exposures) if exposures else 0}")
    
    # Distribution
    print(f"\nExposure distribution:")
    from collections import Counter
    dist = Counter(exposures)
    for score in range(11):
        count = dist.get(score, 0)
        bar = "█" * (count // 10 or (1 if count > 0 else 0))
        print(f"  {score:2d}: {bar} {count}")


if __name__ == "__main__":
    main()
