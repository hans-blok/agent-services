#!/usr/bin/env python3
"""
De Artikelschrijver — Agent Runner
Writes self-contained, accessible articles that clearly convey a single bounded topic.

Capability boundary:
  Schrijven van zelfstandige, toegankelijke artikelen die één afgebakend onderwerp 
  helder overbrengen met duidelijke focus en herkenbare opbouw, zonder nieuwe normen 
  te formuleren.

Role: governance/rolbeschrijvingen/artikel-schrijver.md
Prompt: .github/prompts/artikel-schrijver.prompt.md
"""

import sys
import os

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

def main():
    """Main entry point for De Artikelschrijver agent."""
    print("De Artikelschrijver agent initialized.")
    print("Capability boundary: Write self-contained articles.")
    # Placeholder for actual agent logic
    pass

if __name__ == "__main__":
    main()
