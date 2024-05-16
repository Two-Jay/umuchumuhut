from enums import ModelName, get_hyperparameters, get_model_key, list_GPT_models, list_Claude_models
import os

path = os.getcwd() + "/system_prompt"


def validate_inferencer(func):
  def wrapper(self, *args, **kwargs):
    assert self.target_hyperparameters is not None, "hyperparameters is not set"
    assert type(self.target_hyperparameters) == dict, "hyperparameters is not a dictionary"
    return func(self, *args, **kwargs)
  return wrapper

class Inferencer:
  def __init__(self, model_name : str, key : str):
    self.model_name = get_model_key(model_name)
    self.key = key
    self.system_prompt = self.load_system_prompt(path, self.model_name)
    self.target_hyperparameters = None
    
  def load_system_prompt(self, path : str, model_name : str) -> str:
    with open(f"{path}/{model_name}_{self.key}.md", "r") as f:
      return f.read()

  def inference(self, prompt : str) -> str:
    pass
  
  def set_hyperparameters(self, hyperparameters : dict):
    self.target_hyperparameters = hyperparameters
    print(self.target_hyperparameters)
    
  def set_api_key(self, api_key : str):
    self.api_key = api_key

class OpenAIApi(Inferencer):
  def __init__(self, model_name : ModelName, key : str):
    super().__init__(model_name, key)
    
  @validate_inferencer
  def inference(self, prompt : str) -> str:
    print(f'{self.model_name} inference called')
    return "GPT"
  
class AnthropicApi(Inferencer):
  def __init__(self, model_name : ModelName, key : str):
    super().__init__(model_name, key)

  def load_system_prompt(self, path : str, model_name : str) -> str:
    with open(f"{path}/{model_name}_{self.key}.xml", "r") as f:
      return f.read()

  @validate_inferencer
  def inference(self, prompt : str) -> str:
    print(f'{self.model_name} inference called')
    return "Claude"

def create_inferencer(model_name : ModelName, key : str) -> Inferencer:
  if model_name in list_GPT_models:
    return OpenAIApi(model_name, key)
  elif model_name in list_Claude_models:
    return AnthropicApi(model_name, key)

