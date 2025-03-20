import streamlit as st
import pandas as pd
data = pd.DataFrame({"列1": [1, 2, 3], "列2": ["A", "B", "C"]})

st.dataframe(data)      # 交互式表格
st.table(data)          # 静态表格
st.json({"key": "value"})  # 显示 JSON

name = st.text_input("请输入你的名字")
num=st.slider("选择一个数字", 0, 130,25)
color=st.selectbox("选择一个颜色", ["红色", "绿色", "蓝色"])
st.multiselect("选择多个选项", data["列1"].unique())
like=st.checkbox("喜欢吗")

uploaded_file = st.file_uploader("上传 CSV 文件", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.dataframe(data)

with st.sidebar:
    st.header("设置")
    option = st.radio("选项", ["A", "B"])

    if option == "A":
        st.write("你选择了选项 A")
    else:
        st.write("你选择了选项 B")

col1, col2 = st.columns(2)
with col1:
    st.write("左侧内容")
with col2:
    st.write("右侧内容")


with st.expander("点击展开详情"):
    st.write("隐藏的详细信息")


import time
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.1)
    progress_bar.progress(i + 1)