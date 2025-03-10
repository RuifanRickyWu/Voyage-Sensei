from user_intent_processor.user_intent.user_intent import UserIntent
from jinja2 import Environment, FileSystemLoader, Template


class ProvidePreference(UserIntent):
    _template: Template

    def __init__(self, prompt_config):
        super().__init__()
        env = Environment(loader=FileSystemLoader(prompt_config.get("PROMPT_PATH")))
        self._template = env.get_template(prompt_config.get("PROVIDE_PREFERENCE"))

    def get_prompt_for_classification(self, query:str, last_system_response: str, remaining_mandatory_information: str):
        return self._template.render(user_input=query, last_system_response=last_system_response, remaining_mandatory_information=remaining_mandatory_information)
