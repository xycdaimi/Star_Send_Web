import streamlit as st

from send.find import send_list
from sql.connect import create_connection
from sql import du


def get_history():
    if 'history_page' not in st.session_state:
        st.session_state.history_page = 1
    if st.button("返回"):
        st.session_state.history_list = False
        st.session_state.history_page = 1
        st.rerun()
    conn = create_connection()
    search = st.text_input("", placeholder='请输入订单号')
    res = du.history_lishi(conn, st.session_state.uid, search, st.session_state.history_page)
    conn.close()
    if res['status']:
        send_list(res)
        up_page, yeshu, down_page = st.columns(3)
        with up_page:
            if st.button("上一页", use_container_width=True):
                if st.session_state.history_page > 1:
                    st.session_state.history_page -= 1
                    st.rerun()
        with yeshu:
            # 用st.markdown来显示页数，因为st.text无法居中显示页数
            st.markdown("<p style='text-align: center;'>" + str(st.session_state.history_page) + " / "
                        + str(res['total_pages']) + "</p>", unsafe_allow_html=True)
        with down_page:
            if st.button("下一页", use_container_width=True):
                if st.session_state.history_page < res['total_pages']:
                    st.session_state.history_page += 1
                    st.rerun()
    if search != '':
        if res['status'] == 0:
            st.warning(res['message'])
        elif res['status'] == -1:
            st.error(res['message'])
