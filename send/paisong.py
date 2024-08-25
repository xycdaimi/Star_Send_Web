import streamlit as st

from sql import xie
from sql.connect import create_connection


def display_paisongs():
    order_data = ['快递未接单', '快递未揽件', '快递已揽件', '正在派件中', '快递已送达', '快递已签收']
    set_type = ['揽件', '派送', '送达']
    color = ['#CCCCCC', '#3EB489', '#FFD700', '#FFA500', '#FF5555', '#800080']
    data = st.session_state.paisong
    back = st.button("返回")
    if back:
        st.session_state.paisong = ""
        st.rerun()
    st.title("快递详情")
    # 显示基本信息
    col1, col2 = st.columns(2)
    with col1:
        st.header("📜 快递基本信息")
        st.markdown(f"快递单号：**{data[0]}**")
        st.markdown(f"寄件人地址：**{data[3]}**")
        st.markdown(f"收件人地址：**{data[8]}**")
    with col2:
        st.header("👤 快递员信息")
        st.markdown(f"编号：**{data[18] if data[18] else '暂无快递员'}**")
        st.markdown(f"电话：**{data[19] if data[19] else '暂无'}**")

    st.header("📬 快递进度")
    # 显示总进度条
    st.markdown(f"总进度: {int(data[13]) * 20}%")
    total_progress_style = f"""
                <div style='width:100%;background-color:#0000FF;padding:3px;border-radius:5px;'>
                    <div style='width:{int(data[13]) * 20}%;background-color:{color[int(data[13])]};
                    height:20px;border-radius:3px;'></div>
                </div>
                """
    st.markdown(total_progress_style, unsafe_allow_html=True)
    # 写一个for循环order_data，根据索引判断
    st.markdown(f"当前状态：{order_data[int(data[13])]}")
    if 0 < int(data[13]) < 4:
        sign_button = st.button("📋 "+set_type[int(data[13])-1])
        if sign_button:
            conn = create_connection()
            res = xie.qianshou(conn, data[0], int(data[13]) + 1)
            conn.close()
            if res['status']:
                chan = list(data)
                chan[13] = int(data[13]) + 1
                st.session_state.paisong = chan
                st.rerun()
            elif res['status'] == 0:
                st.warning(res['message'])
            else:
                st.error(res['message'])