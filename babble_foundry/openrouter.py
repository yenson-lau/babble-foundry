import json
import os
import requests
from typing import Generator, Literal, Optional, overload


class OpenRouter:
    def __init__(
        self,
        api_key: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ["OPENROUTER_API_KEY"]

    @overload
    def chat(self, stream: Literal[False] = False, **data) -> dict:
        ...

    @overload
    def chat(self, stream: Literal[True], **data) -> Generator[dict, None, None]:
        ...

    def chat(self, stream: bool = False, **data):
        data = data | {"stream": stream}
        args = dict(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=data,
            stream=stream
        )
        return _post_stream(**args) if stream else _post_nostream(**args)

    @staticmethod
    def print_response(response: dict):
        return print_response(response)

    @staticmethod
    def print_streaming_response(stream: Generator[dict, None, None]) -> list[dict]:
        return print_streaming_response(stream)


def _post_nostream(**args) -> dict:
    r = requests.post(**args)
    if r.status_code != 200:
        raise RuntimeError(
            f"Unexpected response ({r.status_code}): {r.text}"
        )
    return r.json()


def _post_stream(**args) -> Generator[dict, None, None]:
    with requests.post(**args) as r:
        for line in r.iter_lines(decode_unicode=True):
            if not line.startswith('data: '):
                continue
            data = line[6:]
            if data == '[DONE]':
                break
            try:
                yield json.loads(data)
            except (json.JSONDecodeError, KeyError):
                continue


def print_response(response: dict):
    if (reasoning := response["choices"][0]["message"]["reasoning"]):
        print("===== REASONING =====")
        print(reasoning.strip())
        print("===== END OF REASONING =====\n")

    print(response["choices"][0]["message"]["content"])


def print_streaming_response(stream: Generator[dict, None, None]) -> list[dict]:
    chunks = []
    in_reasoning = False
    for chunk in stream:
        chunks.append(chunk)
        if (reasoning := chunk["choices"][0]["delta"].get("reasoning")):
            if not in_reasoning:
                in_reasoning = True
                print("===== REASONING =====")
            print(reasoning, end="")

        else:
            if in_reasoning:
                in_reasoning = False
                print("\n===== END OF REASONING =====\n")

            print(chunk["choices"][0]["delta"]["content"], end="")
    return chunks
