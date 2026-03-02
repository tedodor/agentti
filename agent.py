from llm.local import LLM
import prompts
import signal
import sys
import time

class Agent:
    def __init__(self, local_mode=True):
        self.llm = LLM()
        self.infer = self.llm.inference

    def timeout_handler(self, signum, frame):
        raise TimeoutError("User input timed out")

    def get_user_input(self):
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
        prompt = initial_prompt if initial_prompt else prompts.INITIAL_PROMPT
        while True:
            response = self.infer(prompt)
            print(response)
            user_input = self.get_user_input()
            if user_input:
                prompt = f"{response}\nUser: {user_input}\nAgent:"
            else:
                prompt = f"{response}\nAgent: (No user input received, continuing...)"
            # sleep to not overwhelm the model with requests
            time.sleep(1)


if __name__ == "__main__":
    agent = Agent()
    agent.initiate_agent(prompts.INITIAL_PROMPT)