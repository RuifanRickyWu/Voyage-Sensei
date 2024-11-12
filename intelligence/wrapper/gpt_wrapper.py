from intelligence.wrapper.llm_wrapper import LLMWrapper
from openai import OpenAI


class GPTWrapper(LLMWrapper):
    _model_name: str
    _max_tokens: int
    _temperature: float
    _client: OpenAI

    def __init__(self, api_key: str):
        super().__init__()
        self._model_name = "gpt-4"
        self._client = OpenAI(api_key=api_key)
        self._max_tokens = 4000
        self._temperature = 0.0

    def make_request(self, message: str) -> str:
        try:
            response = self._client.chat.completions.create(
                model= self._model_name,
                messages=[{"role": "user", "content": message}],
                max_tokens=self._max_tokens,
                temperature= self._temperature
            )
        except Exception as e:
            print(e)
            return "Error"
        return response.choices[0].message.content