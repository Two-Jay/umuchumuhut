import streamlit as st
from enums import ModelName, get_hyperparameters
from inference import create_inferencer

def get_default_hyperparameters() -> dict:
  return {
		'temperature': 0.7,
		'max_tokens': 256,
		'top_p': 1,
		'frequency_penalty': 0,
		'presence_penalty': 0,
	}

def reset_hyperparameters():
	st.session_state.llmHyperParameters = get_default_hyperparameters()

def set_api_key():
	if st.session_state.llmHyperParameters['agent'].model_name == 'GPT':
		if not st.session_state.gpt_api_key:
			st.error("GPT API 키가 입력되지 않았습니다.")
			return
		st.session_state.llmHyperParameters['agent'].set_api_key(st.session_state.gpt_api_key)
	elif st.session_state.llmHyperParameters['agent'].model_name == 'Claude':
		if not st.session_state.claude_api_key:
			st.error("Claude API 키가 입력되지 않았습니다.")
			return
		st.session_state.llmHyperParameters['agent'].set_api_key(st.session_state.claude_api_key)

def display():
	st.write("LLM 설정 페이지")

	model_options = ModelName.get_values()
	selected_model = st.selectbox("모델 선택", model_options)
	print(selected_model)
	hyperparameters = get_hyperparameters(selected_model)
	st.session_state.llmHyperParameters['agent'] = create_inferencer(selected_model, 'transform')
	print(hyperparameters)
	
	st.session_state.gpt_api_key = st.text_input('OpenAI API 키', value=st.session_state.get('gpt_api_key', ''))
	st.session_state.claude_api_key = st.text_input('Claude API 키', value=st.session_state.get('claude_api_key', ''))
	st.session_state.api_key = set_api_key()

	for p in hyperparameters:
		if p == 'max_tokens':
			st.session_state.llmHyperParameters[p] = st.number_input(p, min_value=0, max_value=1000, step=1, value=256)
		elif p in ['frequency_penalty', 'presence_penalty']:
			st.session_state.llmHyperParameters[p] = st.slider(p, min_value=0.0, max_value=1.0, step=0.01, value=0.0)
		else:
			st.session_state.llmHyperParameters[p] = st.slider(p, min_value=0.0, max_value=1.0, step=0.01, value=0.7)
	st.session_state.llmHyperParameters['agent'].set_hyperparameters({k: v for k, v in st.session_state.llmHyperParameters.items() if k in hyperparameters})
	st.button('기본값으로 초기화', on_click=reset_hyperparameters)

	st.warning("이 페이지는 실험 중입니다. 예상치 못한 동작이 발생할 수 있습니다.")

