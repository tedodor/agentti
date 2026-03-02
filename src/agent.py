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

    def timeout_handler(self, signum, frame):
        ## Throw error for timeout
        raise TimeoutError("User input timed out")

    def get_user_input(self):
        """
        Get user input with a timeout. If the user takes too long, return None.
        """

        signal.signal(signal.SIGALRM, self.timeout_handler)
        signal.alarm(10)  # 10 second timeout
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                sys.exit(0)
            return user_input
        except TimeoutError:
            return None
        finally:
            signal.alarm(0)  # Always cancel the alarm

    def initiate_agent(self, initial_prompt=None):
        initial_prompt = initial_prompt if initial_prompt else prompts.INITIAL_PROMPT
        thoughts = ""
        log.info("Starting agent")

        while True:
            response = self.infer(initial_prompt + thoughts)
            print(response)
            user_input = self.get_user_input()

            if user_input:
                thoughts += f"{response}\nUser: <<{user_input}>>\nTHOUGHTS:"
            else:
                thoughts += response
                log.info("No user input received, continuing with model response")

            os.system('clear')
            print(thoughts)


if __name__ == "__main__":
    agent = Agent()
    agent.initiate_agent(prompts.INITIAL_PROMPT)
