import yaml
from intelligence.llm_agent import LLMAgent
from api_key import OPENAI_API_KEY, GOOGLE_API_KEY

with open("../config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    config.update({"OPENAI_API_KEY": OPENAI_API_KEY})
    config.update({"GOOGLE_API_KEY": GOOGLE_API_KEY})

llm_agent = LLMAgent(config, "GPT")


print(llm_agent.make_request("why in web's form of chat-gpt you can use web search"))