import streamlit as st # type: ignore
import pandas as pd # type: ignore

st.set_page_config(
    page_title="数据看板",
    layout="wide",
)

sql2='''select id,show_code,name,d2s
from sys_product
limit 500;'''

# 数据缓存30分钟
# @st.cache_data(ttl=1800)
def query_data(sql_str: str) -> pd.DataFrame:
    conn = st.connection("mysql", type="sql")
    return conn.query(sql_str)


def show_st():
    st.title("一个数据报表")
    st.header("数据结果")
    try:
        if st.button("加载数据"):
            data=query_data(sql2)
            st.dataframe(data,height=500,use_container_width=False)
    except Exception as e:
        st.error(f"❌ 数据库连接失败: {e}")

if __name__ == "__main__":
    show_st()
