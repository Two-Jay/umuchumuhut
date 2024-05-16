from enums import ModelName, get_hyperparameters, get_model_key, list_GPT_models, list_Claude_models
import os
import streamlit as st
from openai import OpenAI
import anthropic


path = os.getcwd() + "/system_prompt"


def validate_inferencer(func):
  def wrapper(self, *args, **kwargs):
    assert self.target_hyperparameters is not None, "hyperparameters is not set"
    assert type(self.target_hyperparameters) == dict, "hyperparameters is not a dictionary"
    return func(self, *args, **kwargs)
  return wrapper

def combine_dairy_with_prompt(prompt : str, diary : str, gender : str, age : str, speech_style : str) -> str:
  password = "{diary}"
  gender_password = "{gender}"
  age_password = "{age_group}"
  speech_style_password = "{speech_style}"
  return prompt.replace(password, diary).replace(gender_password, gender).replace(age_password, age).replace(speech_style_password, speech_style)

class Inferencer:
  def __init__(self, model_name : str, key : str):
    self.model_name = get_model_key(model_name)
    self.model_id = model_name
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
    app = OpenAI(api_key=self.api_key)
    combined = combine_dairy_with_prompt(
      self.system_prompt,
      prompt,
      st.session_state.diary_app["gender"],
      st.session_state.diary_app["age_group"],
      st.session_state.diary_app["speech_style"]
    )
    response = app.chat.completions.create(
      model=self.model_id,
      messages=[
        {"role": "system", "content": combined},
      ],
      **self.target_hyperparameters
    )
    return response.choices[0].message.content
  
class AnthropicApi(Inferencer):
  def __init__(self, model_name : ModelName, key : str):
    super().__init__(model_name, key)

  def load_system_prompt(self, path : str, model_name : str) -> str:
    with open(f"{path}/{model_name}_{self.key}.xml", "r") as f:
      return f.read()

  @validate_inferencer
  def inference(self, prompt : str) -> str:
    app = anthropic.Anthropic(api_key=self.api_key)
    combined = combine_dairy_with_prompt(
      self.system_prompt,
      prompt,
      st.session_state.diary_app["gender"],
      st.session_state.diary_app["age_group"],
      st.session_state.diary_app["speech_style"]
    )
    response = app.messages.create(
        model=self.model_id,
        system=combined,
        messages=[],
        **self.target_hyperparameters
    )
    return response.content[0].text

def create_inferencer(model_name : ModelName, key : str) -> Inferencer:
  if model_name in list_GPT_models:
    print(f"{model_name} is GPT model")
    return OpenAIApi(model_name, key)
  elif model_name in list_Claude_models:
    return AnthropicApi(model_name, key)

