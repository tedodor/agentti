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
         
        thoughts = ""

        while True:
            user_input = self.get_user_input()
            if user_input:
                thoughts += user_input + "\n"

            print("Thinking...")
            response = self.infer(thoughts, system_prompt=system_prompt)
            thoughts += response + "\n"
            os.system('clear')
            print(thoughts)


    def parse_skill_call(self, response: str):
        lines = response.splitlines()
        for line in lines:
            if line.startswith("CALL "):
                parts = line.split()
                if len(parts) >= 4:
                    skill_name = parts[1]
                    script_name = parts[2]
                    args = parts[3:]
                    return skill_name, script_name, args
        return None, None, None

if __name__ == "__main__":
    agent = Agent(skills_dir="src/skills")
    agent.initiate_agent(prompts.INITIAL_PROMPT)
