import streamlit as st

from sql import du
from sql.connect import create_connection

def send_list(res):
    for send in res['data']:
        with st.form(send[0]):
            st.subheader("运单号：" + send[0])
            tel, send_time = st.columns(2)
            with tel:
                st.write("收件人手机号：" + send[9])
            with send_time:
                st.write("派件时间：" + str(send[14] if send[14] else "未派送"))
            if st.form_submit_button("订单详情", use_container_width=True):
                st.session_state.paisong = send
                st.rerun()
def order():
    if 'paisong_page' not in st.session_state:
        st.session_state.paisong_page = 1
    conn = create_connection()
    search = st.text_input("", placeholder='请输入订单号')
    res = du.paisong(conn, st.session_state.uid, search, st.session_state.paisong_page)
    conn.close()
    if res['status'] == 1:
        send_list(res)
        up_page, yeshu, down_page = st.columns(3)
        with up_page:
            if st.button("上一页", use_container_width=True):
                if st.session_state.paisong_page > 1:
                    st.session_state.paisong_page -= 1
                    st.rerun()
        with yeshu:
            # 用st.markdown来显示页数，因为st.text无法居中显示页数
            st.markdown("<p style='text-align: center;'>" + str(st.session_state.paisong_page) + " / "
                        + str(res['total_pages']) + "</p>", unsafe_allow_html=True)
        with down_page:
            if st.button("下一页", use_container_width=True):
                if st.session_state.paisong_page < res['total_pages']:
                    st.session_state.paisong_page += 1
                    st.rerun()
    elif res['status'] == 0:
        st.warning(res['message'])
    else:
        st.error(res['message'])
