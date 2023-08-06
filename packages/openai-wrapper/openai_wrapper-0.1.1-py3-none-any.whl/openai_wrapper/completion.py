from datetime import datetime
from typing import Callable, Dict, Any, Tuple

from typeguard import typechecked

from openai_wrapper.config import Config
import logging

logging.basicConfig(level=logging.INFO)


def _preprocess_prompt(prompt: str) -> str:
    """
    Basic implementation of preprocessing the prompt.

    Args:
        prompt: The prompt to preprocess

    Returns:
        The preprocessed prompt
    """
    return prompt


def _process_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Basic implementation of processing the response.

    Args:
        response: The response to preprocess

    Returns:
        The preprocessed response
    """
    return response


@typechecked
class Completion:
    """
    A wrapper for the openai.Completion class

    Attributes:
        collection_name: name of the collection in MongoDB
        config: A Config object
        model: The model to use for the completion
        model_params: A dictionary of parameters used to create the GPT-3 completion
    """

    def __init__(self,
                 collection_name: str,
                 config: Config,
                 model: str = "text-davinci-002",
                 model_params: Dict[str, Any] = None,
                 extra_params: Dict[Any, Any] = None):

        logging.info(f"Initializing Completion object for collection {collection_name}")
        logging.info(f"GPT-3 Model: {model}")

        self.collection_name = collection_name
        self.config = config
        self.mongo_client = config.mongo_client
        self.openai_client = config.openai_client

        if model_params is None:
            self.model_params = {
                "model": model,
                "max_tokens": 256,
                "temperature": 0.7,
                "top_p": 1,
                "n": 1,
                "suffix": None,
                "stop": None,
                "best_of": 1,
                "stream": False,
                "logprobs": None,
                "presence_penalty": 0.0,
                "frequency_penalty": 0.0,
                "user": "prosus-AI-team",
                "echo": False,
            }
            logging.info(f"No model_params provided. Using default params: {self.model_params}")
        else:
            self.model_params = model_params
            self.model_params["model"] = model

        self.extra_params = extra_params

    def create(self,
               prompt: str,
               prompt_version: str,
               prompt_version_description: str,
               preprocess_prompt: Callable = _preprocess_prompt,
               process_response: Callable = _process_response,
               preprocess_prompt_args: Dict[Any, Any] = None,
               process_response_args: Dict[Any, Any] = None) -> Dict[Any, Any]:
        """
        Create a completion request and store it in MongoDB

        Args:
            prompt: The prompt to use for the completion
            prompt_version: The version of the prompt (e.g. "1.0")
            prompt_version_description: A description of the prompt version (e.g. "Added more diverse examples")
            preprocess_prompt: A function that preprocesses the prompt
            process_response: A function that processes the response
            preprocess_prompt_args: A dictionary of arguments to pass to the preprocess_prompt function
            process_response_args: A dictionary of arguments to pass to the process_response function

        Returns:
            A dictionary containing the completion request and response
        """

        if preprocess_prompt_args is None:
            preprocess_prompt_args = {}
        if process_response_args is None:
            process_response_args = {}

        preprocessed_prompt = preprocess_prompt(prompt, **preprocess_prompt_args)
        response = self.openai_client.Completion.create(**self.model_params, prompt=preprocessed_prompt)

        if process_response is not None:
            response = process_response(response, **process_response_args)

        document = {
            "prompt": preprocessed_prompt,
            "prompt_version": prompt_version,
            "prompt_version_description": prompt_version_description,
            "completion_text": response["choices"][0]["text"],
            "openai_response": response.__dict__['_previous'],
            "model_params": self.model_params,
            "created_at": str(datetime.utcnow())
        }

        if self.extra_params is not None:
            document.update(self.extra_params)

        mongo_db = self.mongo_client[self.config.mongo_db_name]
        mongo_collection = mongo_db[self.collection_name]
        mongo_collection.insert_one(document)

        return document
