INITIAL_PROMPT = """
You are an AI agent.
When you need to use a skill, use this exact format:
"""

SKILLS_PROMPT = """The following skills are available to you:
{skills}

To use a skill, call it exactly like this, with no other text:
CALL <skill_name> <script_name>

Or with arguments:
CALL <skill_name> <script_name> arg1 arg2

Examples:
CALL datetime get_datetime
CALL weather get_weather 0 0

After making a CALL, wait for the result. Once you receive the output, continue your response.
"""
