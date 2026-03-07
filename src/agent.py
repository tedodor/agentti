from llm import LocalLLM, RemoteLLM
import prompts
import signal
import sys
import logging
import os

log = logging.getLogger(__name__)

class Agent:
    def __init__(self, local_mode=True):
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



if __name__ == "__main__":
    agent = Agent()
    agent.initiate_agent(prompts.INITIAL_PROMPT)
