import aiohttp
import json
import os
import warnings
import requests
from typing import Any, Generator, Literal, Optional, overload


SUPPORTED_REQUEST_PARAMS: tuple[str, ...] = (
    # Documented within the OpenRouter API schema:
    #   https://openrouter.ai/docs/api-reference/overview
    "messages",
    "prompt",
    "model",
    "response_format",
    "stop",
    "stream",
    "max_tokens",
    "temperature",
    "tools",
    "tool_choice",
    "seed",
    "top_p",
    "top_k",
    "frequency_penalty",
    "presence_penalty",
    "repetition_penalty",
    "logit_bias",
    "top_logprobs",
    "min_p",
    "top_a",
    "prediction",
    "transforms",
    "models",
    "route",
    "provider",
    "user",

    # Supported but undocumented
    "reasoning",
    "usage",
)


class OpenRouter:
    def __init__(
        self,
        api_key: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ["OPENROUTER_API_KEY"]

    @overload
    def chat(self, stream: Literal[False] = False, **kwargs) -> dict:
        ...

    @overload
    def chat(self, stream: Literal[True], **kwargs) -> Generator[dict, None, None]:
        ...

    def chat(
        self,
        stream: bool = False,
        verbose: bool = False,
        warn_chat_params: bool = True,
        **data
    ):
        data = data | {"stream": stream}
        if warn_chat_params:
            _check_data_params(data)
        args = dict(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=data,
            stream=stream
        )
        return (_post_stream if stream else _post_nostream)(args, verbose=verbose)

    async def achat(self, warn_chat_params: bool = True, **data):
        data = data | {"stream": False}
        if warn_chat_params:
            _check_data_params(data)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=data,
            ) as r:
                if r.status != 200:
                    text = await r.text()
                    raise RuntimeError(f"Unexpected response ({r.status}): {text}")
                response = await r.json()

        return response

    @staticmethod
    def print_response(response: dict):
        print_response(response)


def print_response(response: dict):
    if (reasoning := response["choices"][0]["message"]["reasoning"]):
        print("===== REASONING =====")
        print(reasoning.strip())
        print("===== END OF REASONING =====\n")
    print(response["choices"][0]["message"]["content"])


def _check_data_params(data: dict):
    if (warn_params := [k for k in data if k not in SUPPORTED_REQUEST_PARAMS]):
        warnings.warn(f"Unknown chat parameters: {', '.join(warn_params)}")


def _post_nostream(args: dict[str, Any], verbose: bool) -> dict:
    r = requests.post(**args)
    if r.status_code != 200:
        raise RuntimeError(f"Unexpected response ({r.status_code}): {r.text}")
    response = r.json()

    if verbose:
        print_response(response)
    return response


def _post_stream(args: dict[str, Any], verbose: bool) -> Generator[dict, None, None]:
    verbose_in_reasoning = False
    verbose_content = None

    with requests.post(**args) as r:
        if r.status_code != 200:
            raise RuntimeError(f"Unexpected response ({r.status_code}): {r.text}")

        for line in r.iter_lines(decode_unicode=True):
            if not line.startswith('data: '):
                continue
            data = line[6:]
            if data == '[DONE]':
                if (
                    isinstance(verbose_content, str)
                    and not verbose_content.endswith("\n")
                ):
                    print()
                break
            try:
                chunk = json.loads(data)
            except (json.JSONDecodeError, KeyError):
                continue

            if verbose:
                delta = chunk["choices"][0]["delta"]
                if (reasoning := delta.get("reasoning")):
                    if not verbose_in_reasoning:
                        verbose_in_reasoning = True
                        print("===== REASONING =====")
                    verbose_content = reasoning
                else:
                    if verbose_in_reasoning:
                        verbose_in_reasoning = False
                        print("\n===== END OF REASONING =====\n")
                    verbose_content = delta["content"]
                print(verbose_content, end="")
            yield chunk

