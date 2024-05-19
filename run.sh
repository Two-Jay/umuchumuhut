#!/bin/bash

# pyenv 설치
curl https://pyenv.run | bash

# pyenv 초기화
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Python 3.12.0 설치
pyenv install 3.12.0

# 가상환경 생성 및 활성화
pyenv virtualenv 3.12.0 myenv
pyenv activate myenv

# 필요한 패키지 설치
pip install -r requirements.txt

# Streamlit 어플리케이션 실행
streamlit run app.py