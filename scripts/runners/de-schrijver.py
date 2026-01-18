#!/usr/bin/env python3
"""
De Schrijver — Agent Runner
Produces accessible, flowing prose that clarifies existing concepts.

Capability boundary:
  Produceren van toegankelijke, vloeiende boektekst die bestaande concepten 
  helder maakt zonder deze te analyseren, beargumenteren of normatief in te vullen.

Role: governance/rolbeschrijvingen/de-schrijver.md
Prompt: .github/prompts/de-schrijver.prompt.md
"""

import sys
import os

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

def main():
    """Main entry point for De Schrijver agent."""
    print("De Schrijver agent initialized.")
    print("Capability boundary: Produce accessible, flowing prose.")
    # Placeholder for actual agent logic
    pass

if __name__ == "__main__":
    main()
