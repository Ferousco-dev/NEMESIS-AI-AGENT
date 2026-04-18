"""
Cached Demo Mode - Shows NEMESIS functionality without API calls
Useful when rate limits are hit or for demonstrations.
"""

import asyncio
from core.memory import Memory
from utils.ui import NemesisUI


# Pre-computed cached results (from previous successful runs)
CACHED_SHADOW_RESULT = """The subject (Emeka) exhibits pronounced avoidance patterns around financial commitments, 
despite recurring declarations of intent. Time-stamped evidence: Journal entries show 5 mentions of "starting 
a budget" (Jan 3, Feb 14, Mar 8, Mar 22, Apr 1) but zero follow-through. Calendar shows pattern of 
rescheduling money-related tasks. Email frequency suggests high responsiveness in social contexts but 
minimal engagement with financial communications. The subject's decision-making deteriorates under stress, 
with emotional triggers centered around family conflict. Primary defense mechanism: deflection through 
workaholic patterns. When anxious about money, subject increases work hours rather than addressing the issue."""

CACHED_PROFILER_RESULT = {
    "core_traits": ["High conscientiousness (in work)", "Anxiety-prone", "Avoidant (financial)"],
    "core_wounds": ["Shame around money", "Fear of parental judgment", "Perfectionism"],
    "defense_mechanisms": ["Workaholism", "Deflection", "Compartmentalization"],
    "blind_spots": ["Cannot see that avoidance increases anxiety", "Believes willpower > systems"],
    "strengths": ["High intelligence", "Strong work ethic", "Empathetic to others"],
    "triggers": ["Family conversations", "Financial institutions", "Accountability"],
    "relationship_style": "Gives easily to others, struggles to receive/prioritize self",
    "decision_pattern": "Logical planning followed by emotional abandonment under stress"
}

CACHED_ORACLE_RESULT = {
    "overall_risk": "HIGH",
    "scenarios": [
        {
            "situation": "Tax deadline approaches in 2 weeks",
            "probability": "95%",
            "pattern": "Subject will declare intent then avoid",
            "warning": "Unresolved taxes compound anxiety exponentially",
            "outcome_bad": "Penalty fees + IRS communication + shame cascade",
            "outcome_good": "File on time → relief → momentum for financial growth"
        },
        {
            "situation": "Parent asks about finances in family call",
            "probability": "80%",
            "pattern": "Subject freezes, aggressive response, withdraws",
            "warning": "Each avoidance deepens shame and fantasy of catastrophe",
            "outcome_bad": "Family conflict → isolation → increased workaholism",
            "outcome_good": "Honest conversation → support received → pattern broke"
        },
        {
            "situation": "Credit card debt reaches critical point",
            "probability": "60%",
            "pattern": "Denial followed by panic",
            "warning": "Inevitable collision with reality will trigger crisis",
            "outcome_bad": "Forced conversation with partner → relationship damage",
            "outcome_good": "Proactive disclosure → shared problem-solving → trust increase"
        }
    ],
    "verdict": "NEMESIS ASSESSMENT: Emeka's financial avoidance is not about money. It's about shame and perfectionism. The pattern is: avoid → anxiety increases → work harder → avoid more. To break this: ONE phone call (to accountant or parent) in the next 48 hours. Discomfort is the signal, not the problem."
}

CACHED_VOICE_INTERVENTION = """[PATTERN DETECTED]
You deploy workaholism to avoid financial anxiety. You've said "I'll start a budget" five times since January.

[THE TRUTH]
Your avoidance isn't character weakness — it's a learned response to shame. Every time you reschedule that financial conversation, your anxiety doesn't decrease. It compounds. You work harder to prove your worth instead of facing the numbers. The irony: you're one of the most disciplined people in your field, but you can't apply that discipline where it matters most.

[TWO FUTURES]
If you follow your pattern: Tax deadline hits. You panic. You either blow it off (consequences compound) or white-knuckle through it. Either way, the shame loop doesn't break. Next financial milestone, same panic.

If you break it now: You make ONE phone call today. Not to solve the problem. Just to start. To an accountant, a financial advisor, or even your parent. Discomfort for 20 minutes. Then you know what you're actually dealing with. Then you can actually plan.

[YOUR MOVE]
Call ONE person about money today. Not tomorrow. Not when you're ready. Today. You have the discipline. You're choosing the wrong target."""


async def run_cached_demo():
    """Run demo with pre-computed results (no API calls)."""
    
    NemesisUI.print_banner()
    NemesisUI.info("Running CACHED DEMO MODE (no API calls - shows system architecture)")
    await asyncio.sleep(0.5)

    memory = Memory()
    
    # Stage 1: Show Shadow results
    NemesisUI.status("[The Shadow] Ingesting Emeka's last 3 months of data...", "🔄")
    await asyncio.sleep(0.5)
    NemesisUI.agent_speaking("shadow", CACHED_SHADOW_RESULT)
    NemesisUI.success("Behavioral signals extracted and stored.")
    await asyncio.sleep(1)

    # Stage 2: Show Profiler results
    NemesisUI.status("[The Profiler] Building Emeka's psychological model...", "🔄")
    await asyncio.sleep(0.5)
    NemesisUI.section("PSYCHOLOGICAL PROFILE")
    NemesisUI.print_dict_as_table(CACHED_PROFILER_RESULT, "Emeka's Profile")
    NemesisUI.success("Profile complete.")
    await asyncio.sleep(1)

    # Stage 3: Show Oracle results
    NemesisUI.status("[The Oracle] Simulating Emeka's next 30 days...", "🔮")
    await asyncio.sleep(0.5)
    NemesisUI.section("YOUR NEXT 30 DAYS — ORACLE SIMULATION")
    risk_level = CACHED_ORACLE_RESULT.get('overall_risk', 'Unknown')
    NemesisUI.panel_warning("Overall Risk Level", risk_level)
    
    scenarios = CACHED_ORACLE_RESULT.get("scenarios", [])
    scenario_data = []
    for i, s in enumerate(scenarios, 1):
        scenario_data.append({
            "Scenario": f"#{i}: {s.get('situation', '')}",
            "Probability": f"{s.get('probability', '')}",
            "Pattern": s.get('pattern', ''),
            "If Nothing Changes": s.get('outcome_bad', ''),
            "If You Act Now": s.get('outcome_good', '')
        })
    NemesisUI.print_list_as_table(scenario_data, "Risk Scenarios")
    
    NemesisUI.panel_emphasis(CACHED_ORACLE_RESULT.get('verdict', ''), "NEMESIS Verdict", "cyan")
    NemesisUI.success("Simulation complete.")
    await asyncio.sleep(1)

    # Stage 4: Show Voice intervention
    NemesisUI.panel_header("[The Voice] Live Intervention Demo", "Watch NEMESIS stop Emeka from his biggest mistake")
    NemesisUI.divider()
    demo_situation = "I know I should deal with my finances but honestly I've been so busy with work. I'll start a budget next month when things calm down."
    NemesisUI.panel_info("Emeka's Statement", f'"{demo_situation}"')
    NemesisUI.status("Processing intervention...", "🔄")
    await asyncio.sleep(1)

    NemesisUI.agent_speaking("voice", CACHED_VOICE_INTERVENTION)
    NemesisUI.divider()
    
    # Show system info
    NemesisUI.panel_info("Demo Mode Info", 
        "[yellow]⚠️  This demo used cached/pre-computed results.[/yellow]\n\n"
        "[cyan]Why?[/cyan] Both Groq and Gemini are rate-limited today.\n\n"
        "[cyan]Each agent normally would:[/cyan]\n"
        "  • Shadow: Call LLM to extract signals (~500 tokens lite)\n"
        "  • Profiler: Build psychological model (~400 tokens lite)\n"
        "  • Oracle: Simulate 30 days (~300 tokens lite)\n"
        "  • Voice: Deliver intervention (~200 tokens lite)\n\n"
        "[cyan]Total daily tokens needed:[/cyan] ~1,500 (lite mode)\n\n"
        "[green]✓ Rate limits reset at midnight UTC[/green]\n"
        "[green]✓ Come back tomorrow for live demo[/green]\n"
        "[green]✓ Or upgrade Groq tier for more tokens[/green]")
    
    NemesisUI.success("Cached demo complete. This is what NEMESIS can do!")


if __name__ == "__main__":
    asyncio.run(run_cached_demo())
