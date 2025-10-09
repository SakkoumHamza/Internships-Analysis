import json
from processing.llm import structure_offer
import os

raw_path = "/Users/mac/Documents/Projects/internship_analysis/data/raw/stages.json"
structured_path = "/Users/mac/Documents/Projects/internship_analysis/data/structured/stages_structured.jl"

print(f"Reading from: {raw_path}")
print(f"Writing to: {structured_path}")

with open(raw_path, "r", encoding="utf-8") as f_raw, open(structured_path, "a", encoding="utf-8") as f_structured:
    try:
        raw_offres = json.load(f_raw)  # load entire JSON array
    except json.JSONDecodeError as e:
        print("❌ Failed to read JSON:", e)
        raw_offres = []

    for raw_offre in raw_offres:
        structured = structure_offer(raw_offre)
        print(" ✅ The function structure_offer called")
        f_structured.write(json.dumps(structured, ensure_ascii=False) + "\n")


print(f"\n✅ Successfully processed and appended jobs to {structured_path}")