import streamlit as st
import pandas as pd

st.set_page_config(
    layout="wide",
)

sql = '''select
receive.batch_code '生产批次',
receive.sku_name '产品',
receive.sku_code '产品代码',
receive_time '日期',
receive.receive_qty '入库数量',
od.order_qty '出库数量'
from
(
    select
        qpb.batch_code,
        sp.name 'sku_name',
        sp.show_code 'sku_code',
        date_format(qs.in_store_time,'%Y/%m/%d') 'receive_time',
        sum(case when qs.status in(1,2,3) then qs.box_num else 0  end)'receive_qty'
    from
        qrs_stack qs
        left join qrs_production_line qpl on qpl.id=qs.production_line_id
        left join qrs_produce_batch qpb on qpb.id=qs.batch_id
        left join sys_product sp on sp.id=qs.product_id
    where
        1=1
        and qs.produce_date>='2025-01-01'
        and qpb.batch_code is not null
        and qs.status in (1,2,3)
        and qs.deleted=0
    group by
        qpb.batch_code,
        sp.name,
        sp.show_code,
        date_format(qs.in_store_time,'%Y/%m/%d')
)receive
left join
    (
        select
            date_format(qo.out_store_time,'%Y/%m/%d') 'order_time',
            qpb.batch_code,
            sp.name 'sku_name',
            sp.show_code 'sku_code',
            sum(qost.send_order_dist)'order_qty'
        from
            qrs_order qo
            join qrs_order_send_detail qosd on qosd.order_id=qo.id and qosd.deleted=0
            join qrs_order_send_stack qost on qost.order_send_detail_id=qosd.id and qost.deleted=0
            join qrs_stack qs on qs.id=qost.stack_id
            left join qrs_production_line qpl on qpl.id=qs.production_line_id
            left join qrs_produce_batch qpb on qpb.id=qs.batch_id
            left join sys_product sp on sp.id=qs.product_id
        where
            1=1
            and qo.out_store_time>='2025-01-01'
        group by
            date_format(qo.out_store_time,'%Y/%m/%d'),
            qpb.batch_code,
            sp.name,
            sp.show_code
    )od on od.order_time=receive.receive_time and od.sku_code=receive.sku_code and od.batch_code=receive.batch_code;
'''


@st.cache_data(ttl="30m")
def get_data(sql_str: str):
    sfa_conn = st.connection("sfa",type='sql')
    return sfa_conn.query(sql_str)




def show_st():
    st.title("一个数据报表")
    st.header("数据结果")
    if st.button("加载数据"):
        data=get_data(sql)
        df = pd.DataFrame(data)
    st.dataframe(data,height=500,use_container_width=False)

show_st()
