#!/bin/sh
cd /root/Jack/streamlit || exit
git pull
. /root/.pyenv/versions/3.12.7/envs/streamlit_py3127/bin/activate
python -V
python -m streamlit run main.py
deactivate
