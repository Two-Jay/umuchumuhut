from enum import Enum

class BaseEnum(Enum):
	@classmethod
	def get_values(cls):
		return [e.value for e in cls]

class Gender(BaseEnum):
	남성 = "남성"
	여성 = "여성"

class AgeGroup(BaseEnum):
	유년층 = "유년층"
	청소년층 = "청소년층"
	성인층 = "성인층"
	노년층 = "노년층"

class SpeechStyle(BaseEnum):
	구연체 = "구연체"
	낭독체 = "낭독체"
	대화체 = "대화체"
	독백체 = "독백체"
	애니체 = "애니체"
	중계체 = "중계체"
	친절체 = "친절체"
	
class ModelName(BaseEnum):
	gpt_4_o = "gpt-4o"
	Claude_3_opus = "claude-3-opus-20240229"
	Claude_3_sonnet = "claude-3-sonnet-20240229"

def get_hyperparameters(model_value : str) -> list:
	if model_value in list_GPT_models:
		return [
			'temperature',
			'max_tokens',
			'top_p',
			'frequency_penalty',
			'presence_penalty'
		]
	elif model_value in list_Claude_models:
		return [
			'temperature',
			'max_tokens',
			'top_p',
		]
	else:
		raise ValueError(f"Invalid model name: {model_value}")

def get_model_key(model_value : str) -> str:
	if model_value in list_GPT_models:
		return "GPT"
	elif model_value in list_Claude_models:
		return "Claude"
	else:
		raise ValueError(f"Invalid model name: {model_value}")

list_Claude_models = [ModelName.Claude_3_opus.value, ModelName.Claude_3_sonnet.value]
list_GPT_models = [ModelName.gpt_4_o.value]

