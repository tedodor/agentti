from llm import LocalLLM, RemoteLLM
import prompts
from pathlib import Path
import logging
import os

from skills.skills import SkillsList

log = logging.getLogger(__name__)

class Agent:
    def __init__(self, skills_dir: str, local_mode=True):
        self.skills = SkillsList(Path(skills_dir))
        self.llm = LocalLLM() if local_mode else RemoteLLM()
        self.infer = self.llm.inference

    def get_user_input(self):
        return input()
        
    def initiate_agent(self, initial_prompt=None):
        system_prompt = initial_prompt if initial_prompt else prompts.INITIAL_PROMPT
        skills_prompt = prompts.SKILLS_PROMPT.format(skills=self.skills.get_skill_descriptions())        
        system_prompt += "\n" + skills_prompt

        thoughts = ""
        print(system_prompt)
        while True:
            user_input = self.get_user_input()
            if user_input:
                thoughts += user_input + "\n"

            print("Thinking...")
            response = self.infer(thoughts, system_prompt=system_prompt)

            response = self.parse_response(response)

            while response.startswith("CALL "):
                thoughts += f"{results}\n"
                results = self.parse_skill_call(response)
                thoughts += f"Skill call result: {results}\n"
                response = self.infer(thoughts, system_prompt=system_prompt)                

            thoughts += response + "\n"
            os.system('clear')
            print(thoughts)
            
    def parse_skill_call(self, response: str):
        parts = response.split()
        if len(parts) >= 4:
            skill_name = parts[1]
            script_name = parts[2]
            args = parts[3:]
            return self.skills.run_skill_script(skill_name, script_name, *args)
        else:
            return "Error: Invalid CALL format. Expected: CALL <skill_name> <script_name> [args]"

if __name__ == "__main__":
    agent = Agent(skills_dir="src/skills")
    agent.initiate_agent(prompts.INITIAL_PROMPT)
