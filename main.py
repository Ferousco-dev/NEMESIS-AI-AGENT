import warnings
warnings.simplefilter("ignore")  # Suppress all warnings immediately

import importlib.metadata
import urllib3

# Shim for Python 3.9 compatibility
if not hasattr(importlib.metadata, 'packages_distributions'):
    importlib.metadata.packages_distributions = lambda: {}

# Extra suppression just to be sure
warnings.filterwarnings("ignore")
try:
    urllib3.disable_warnings()
except:
    pass

import os
import sys
import asyncio
from dotenv import load_dotenv
from core.orchestrator import Orchestrator
from core.memory import Memory
from utils.logger import logger

# Load environment variables from .env file
load_dotenv()

from utils.ui import NemesisUI


async def main():
    NemesisUI.print_banner()

    if len(sys.argv) < 2:
        NemesisUI.error("Usage: python main.py [command]")
        NemesisUI.bullet_list(["ingest", "analyze", "predict", "talk", "demo"], "Commands")
        sys.exit(1)

    command = sys.argv[1]
    memory = Memory()
    orchestrator = Orchestrator(memory)

    if command == "ingest":
        NemesisUI.info("Feeding your data to The Shadow...")
        data_file = sys.argv[2] if len(sys.argv) > 2 else None
        await orchestrator.run_ingestion(data_file)

    elif command == "analyze":
        NemesisUI.info("The Profiler is building your psychological model...")
        await orchestrator.run_analysis()

    elif command == "predict":
        NemesisUI.info("The Oracle is simulating your next 30 days...")
        await orchestrator.run_prediction()

    elif command == "talk":
        NemesisUI.info("Connecting you to The Voice...")
        NemesisUI.status("Type your situation. NEMESIS will tell you the truth.", "")
        await orchestrator.run_intervention()

    elif command == "demo":
        NemesisUI.info("Running full demo with sample data...")
        await orchestrator.run_demo()

    else:
        NemesisUI.error(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        from utils.error_handler import APIErrorHandler, RateLimitHandler
        
        is_rate_limit, message = APIErrorHandler.handle(e)
        
        if is_rate_limit:
            RateLimitHandler.handle_rate_limit(e, "API")
            NemesisUI.info("💡 Try running: python3 cached_demo.py")
        else:
            NemesisUI.panel_error("Error", message)
            NemesisUI.info(f"Debug info: {str(e)[:200]}")
        
        sys.exit(1)
