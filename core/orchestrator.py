"""
Orchestrator — The brain that coordinates all 4 NEMESIS agents.

Flow:
  Shadow (ingests) → Profiler (analyzes) → Oracle (predicts) → Voice (intervenes)
"""

import asyncio
from core.memory import Memory
from agents.shadow import ShadowAgent
from agents.profiler import ProfilerAgent
from agents.oracle import OracleAgent
from agents.voice import VoiceAgent
from utils.logger import logger
from utils.ui import NemesisUI
from data.samples.demo_data import DEMO_DATA


class Orchestrator:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.shadow = ShadowAgent(memory)
        self.profiler = ProfilerAgent(memory)
        self.oracle = OracleAgent(memory)
        self.voice = VoiceAgent(memory)

    async def run_ingestion(self, data_file: str = None):
        if data_file:
            try:
                with open(data_file, "r") as f:
                    raw = f.read()
                NemesisUI.info(f"Loading data from {data_file}...")
            except FileNotFoundError:
                NemesisUI.error(f"File not found: {data_file}. Using manual input.")
                raw = self._collect_manual_input()
        else:
            raw = self._collect_manual_input()

        NemesisUI.status("[The Shadow] Processing your data silently...", "🔄")
        result = await self.shadow.process(raw)
        NemesisUI.agent_speaking("shadow", result)
        NemesisUI.success("Data ingested. Run: python main.py analyze")

    def _collect_manual_input(self) -> str:
        NemesisUI.panel_info("Data Input", "Paste your data below (journal entries, events, thoughts).\nPress ENTER twice when done.")
        lines = []
        blank_count = 0
        while blank_count < 2:
            line = input()
            if line == "":
                blank_count += 1
            else:
                blank_count = 0
                lines.append(line)
        return "\n".join(lines)

    async def run_analysis(self):
        if not self.memory.has_data():
            NemesisUI.error("No data found. Run: python main.py ingest first.")
            return

        NemesisUI.status("[The Profiler] Building your psychological model...", "🔮")
        profile = await self.profiler.analyze()

        NemesisUI.section("YOUR PSYCHOLOGICAL PROFILE")

        if isinstance(profile, dict):
            NemesisUI.print_dict_as_table(profile, "Profile Data")
        else:
            NemesisUI.panel_info("Profile", str(profile))

        NemesisUI.success("Profile saved. Run: python main.py predict")

    async def run_prediction(self):
        if not self.memory.has_profile():
            NemesisUI.error("No profile found. Run: python main.py analyze first.")
            return

        NemesisUI.status("[The Oracle] Simulating your next 30 days...", "🔮")
        prediction = await self.oracle.simulate()

        NemesisUI.section("YOUR NEXT 30 DAYS — ORACLE SIMULATION")

        if isinstance(prediction, dict):
            risk_level = prediction.get('overall_risk', 'Unknown')
            NemesisUI.panel_warning("Overall Risk Level", risk_level)

            scenarios = prediction.get("scenarios", [])
            scenario_data = []
            for i, s in enumerate(scenarios, 1):
                scenario_data.append({
                    "Scenario": f"#{i}: {s.get('situation', '')}",
                    "Probability": f"{s.get('probability', '')}%",
                    "Pattern": s.get('pattern', ''),
                    "If Nothing Changes": s.get('outcome_bad', ''),
                    "If You Act Now": s.get('outcome_good', '')
                })
            NemesisUI.print_list_as_table(scenario_data, "Risk Scenarios")

            NemesisUI.panel_emphasis(prediction.get('verdict', ''), "NEMESIS Verdict", "cyan")
        else:
            NemesisUI.panel_info("Prediction", str(prediction))

        NemesisUI.success("Prediction saved. Run: python main.py talk")

    async def run_intervention(self):
        NemesisUI.panel_header("[The Voice] I'm watching. Tell me what's happening.", "Type 'quit' to exit")

        while True:
            user_input = NemesisUI.user_input_prompt("You")
            if user_input.lower() in ["quit", "exit", "q"]:
                NemesisUI.agent_speaking("voice", "Remember what we discussed.")
                break
            if not user_input:
                continue

            self.memory.add_conversation_turn("user", user_input)
            NemesisUI.status("Processing...", "🔄")

            response = await self.voice.intervene(user_input)
            NemesisUI.agent_speaking("voice", response)
            self.memory.add_conversation_turn("assistant", response)

    async def run_demo(self):
        NemesisUI.info("Loading demo data — a fictional person named Emeka...")
        await asyncio.sleep(0.5)

        # Stage 1: Ingest demo data
        NemesisUI.status("[The Shadow] Ingesting Emeka's last 3 months of data...", "🔄")
        for entry in DEMO_DATA["entries"]:
            self.memory.add_raw_entry(entry["text"], entry["source"])
        result = await self.shadow.process("\n".join(e["text"] for e in DEMO_DATA["entries"]))
        NemesisUI.agent_speaking("shadow", result)
        await asyncio.sleep(1)

        # Stage 2: Build profile
        NemesisUI.status("[The Profiler] Building Emeka's psychological model...", "🔄")
        profile = await self.profiler.analyze()
        NemesisUI.success("Profile complete.")
        await asyncio.sleep(1)

        # Stage 3: Oracle prediction
        NemesisUI.status("[The Oracle] Simulating Emeka's next 30 days...", "🔮")
        prediction = await self.oracle.simulate()
        NemesisUI.success("Simulation done.")
        await asyncio.sleep(1)

        # Stage 4: Live intervention demo
        NemesisUI.panel_header("[The Voice] Live Intervention Demo", "Watch NEMESIS stop Emeka from his biggest mistake")
        NemesisUI.divider()
        demo_situation = DEMO_DATA["demo_situation"]
        NemesisUI.panel_info("Emeka's Statement", demo_situation)
        NemesisUI.status("Processing intervention...", "🔄")
        await asyncio.sleep(1.5)

        response = await self.voice.intervene(demo_situation)
        NemesisUI.agent_speaking("voice", response)
        NemesisUI.divider()
        NemesisUI.success("Demo complete. This is NEMESIS.")
