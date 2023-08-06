from datetime import datetime
from typing import Callable, Dict, Any, Tuple, List, Mapping, Union

from pymongo.cursor import Cursor
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
        use_case_name: name of the use case so it can be used as a collection name in MongoDB (e.g. "Q&A", "Quiz_Generation")
        config: A Config object
        model: The model to use for the completion
        model_params: A dictionary of parameters used to create the GPT-3 completion
    """

    def __init__(self,
                 use_case_name: str,
                 config: Config,
                 model: str = "text-davinci-002",
                 model_params: Dict[str, Any] = None,
                 extra_params: Dict[Any, Any] = None):

        logging.info(f"Initializing Completion object for collection {use_case_name}")
        logging.info(f"GPT-3 Model: {model}")

        self.use_case_name = use_case_name
        self.config = config
        self.mongo_client = config.mongo_client
        self.openai_client = config.openai_client

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
            "logprobs": 5,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "user": "prosus-AI-team",
            "echo": False,
        }
        if model_params is None:
            logging.info(f"No model_params provided. Using default params: {self.model_params}")
        else:
            self.model_params.update(model_params)
            self.model_params["model"] = model
            logging.info(f"Updated default params. Updated params: {self.model_params}")

        self.extra_params = extra_params

    def create(self,
               prompt: str,
               prompt_version: str,
               prompt_version_description: str,
               experiment_metadata: Dict[str, Any] = None,
               project_metadata: Dict[str, Any] = None,
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
            experiment_metadata: A dictionary of metadata about the experiment
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
            "created_at": str(datetime.utcnow()),
            "experiment_metadata": experiment_metadata,
            "project_metadata": project_metadata
        }

        if self.extra_params is not None:
            document.update(self.extra_params)

        mongo_db = self.mongo_client[self.config.mongo_db_name]
        mongo_collection = mongo_db[self.use_case_name]
        mongo_collection.insert_one(document)

        return document

    def get_completions_for_prompt(self, prompt: str, prompt_version: str = None) -> List[Dict[Any, Any]]:
        """
        Get all completions for a given prompt

        Args:
            prompt: The prompt to get completions for
            prompt_version: The version of the prompt (e.g. "1.0")

        Returns:
            A list of completions
        """

        mongo_db = self.mongo_client[self.config.mongo_db_name]
        mongo_collection = mongo_db[self.use_case_name]
        if prompt_version:
            return list(mongo_collection.find({"prompt": prompt, "prompt_version": prompt_version}))
        else:
            return list(mongo_collection.find({"prompt": prompt}))

    def get_completion_by_id(self, completion_id: str) -> Dict[Any, Any]:
        """
        Get a completion by its id

        Args:
            completion_id: The id of the completion to get

        Returns:
            A dictionary containing the completion
        """
        from bson import ObjectId

        mongo_db = self.mongo_client[self.config.mongo_db_name]
        mongo_collection = mongo_db[self.use_case_name]
        return mongo_collection.find_one({"_id": ObjectId(completion_id)})

    def get_completions_using_mongodb_filter(self, filters: Dict[Any, Any]) -> List[Dict[Any, Any]]:
        """
        Get completions by a MongoDB filter

        Args:
            filters: The filter to use to find the completion (e.g. {"prompt": "Hello", "prompt_version": "1.0"}

        Returns:
            A dictionary containing the completion
        """
        mongo_db = self.mongo_client[self.config.mongo_db_name]
        mongo_collection = mongo_db[self.use_case_name]
        return list(mongo_collection.find(filters))
