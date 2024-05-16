import streamlit as st
from enums import Gender, AgeGroup, SpeechStyle

def transform():
  if not st.session_state.diary_app.get('diary_text'):
    st.error("일기 입력을 먼저 진행해 주세요.")
    return
  if not st.session_state.llmHyperParameters.get('agent'):
    st.error("왼쪽의 페이지 선택에서 LLM 설정을 먼저 진행해 주세요.")
    return
  st.session_state.diary_app['result'] = st.session_state.llmHyperParameters['agent'].inference(st.session_state.diary_app['diary_text'])

def display():
  # Create three tabs
  tab1, tab2, tab3 = st.tabs(["일기 입력", "특성 설정", "결과창"])

  with tab1:
    st.header("일기 입력")
    st.session_state.diary_app['diary_text'] = st.text_area("여기에 일기를 작성하세요:", st.session_state.diary_app['diary_text'])

  with tab2:
    st.header("특성 설정")
    st.session_state.diary_app['gender'] = st.selectbox("성별", Gender.get_values(), index=Gender.get_values().index(st.session_state.diary_app['gender']))
    st.session_state.diary_app['age_group'] = st.selectbox("연령대", AgeGroup.get_values(), index=AgeGroup.get_values().index(st.session_state.diary_app['age_group']))
    st.session_state.diary_app['speech_style'] = st.selectbox("발화스타일", SpeechStyle.get_values(), index=SpeechStyle.get_values().index(st.session_state.diary_app['speech_style']))
    transform_button = st.button("변환", on_click=transform)

  with tab3:
    st.header("결과창")
    st.text_area("변환된 텍스트:", st.session_state.diary_app['result'], height=200)