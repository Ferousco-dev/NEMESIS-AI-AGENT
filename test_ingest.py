#!/usr/bin/env python3
"""Quick test of ingest functionality"""

import asyncio
from core.orchestrator import Orchestrator
from core.memory import Memory
from utils.ui import NemesisUI

async def test_ingest():
    memory = Memory()
    orchestrator = Orchestrator(memory)
    
    test_data = """I've been avoiding my finances for months. 
Every time money comes up I get anxious.
My partner asks about bills and I just shut down.
I started a budget 3 times but never finished.
When stressed at work, I avoid money handling even more.
I know I have patterns but I can't break them."""
    
    NemesisUI.print_banner()
    NemesisUI.info("Testing data ingestion...")
    
    # Store test data
    memory.add_raw_entry(test_data, "test")
    NemesisUI.success("✓ Data stored successfully")
    
    # Run shadow
    NemesisUI.status("[The Shadow] Extracting signals...", "🔄")
    result = await orchestrator.shadow.process(test_data)
    
    if result and result != "No data to process.":
        NemesisUI.agent_speaking("shadow", result)
        NemesisUI.success("✓ Ingestion works! Next: python3 main.py analyze")
    else:
        NemesisUI.error("No signals extracted")

if __name__ == "__main__":
    asyncio.run(test_ingest())
