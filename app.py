import streamlit as st
from enums import Gender, AgeGroup, SpeechStyle
import testPage
import llmSettingPage
  
# Initialize session state object
if 'diary_app' not in st.session_state:
	st.session_state.diary_app = {
		'diary_text': "",
		'gender': "남성",
		'age_group': "유년층",
		'speech_style': "구연체",
		'result': "여기에 변환된 텍스트가 표시됩니다.",
	}

if 'llmHyperParameters' not in st.session_state:
	st.session_state.llmHyperParameters = {
		'temperature': 0.7,
		'max_tokens': 256,
		'top_p': 1,
		'frequency_penalty': 0,
		'presence_penalty': 0,
		'agent': None
	}



# Create a sidebar
st.sidebar.header("사이드바")
# Create two pages in the sidebar
page = st.sidebar.selectbox("페이지 선택", ["테스트 페이지", "LLM 설정 페이지"])

if page == "테스트 페이지":
  testPage.display()
elif page == "LLM 설정 페이지":
  llmSettingPage.display()
else:
  st.write("")
