import streamlit as st
from sql import connect, du

def fenpei(res):
    for send in res['data']:
        with st.form(send[0]):
            st.subheader("运单号：" + send[0])
            tel, send_time = st.columns(2)
            with tel:
                st.write("收件人手机号：" + send[9])
            with send_time:
                st.write("派件时间：" + str(send[14] if send[14] else "未派送"))
            if st.form_submit_button("点击分配", use_container_width=True):
                st.session_state.distribute = send
                st.rerun()
def assign():
    if 'distribute_page' not in st.session_state:
        st.session_state.distribute_page = 1
    search = st.text_input("", placeholder='请输入订单号')
    conn = connect.create_connection()
    res = du.jiedan(conn, search, st.session_state.distribute_page)
    conn.close()
    if res['status'] == 1:
        fenpei(res)
        up_page, yeshu, down_page = st.columns(3)
        with up_page:
            if st.button("上一页", use_container_width=True):
                if st.session_state.distribute_page > 1:
                    st.session_state.distribute_page -= 1
                    st.rerun()
        with yeshu:
            # 用st.markdown来显示页数，因为st.text无法居中显示页数
            st.markdown("<p style='text-align: center;'>" + str(st.session_state.distribute_page) + " / "
                        + str(res['total_pages']) + "</p>", unsafe_allow_html=True)
        with down_page:
            if st.button("下一页", use_container_width=True):
                if st.session_state.distribute_page < res['total_pages']:
                    st.session_state.distribute_page += 1
                    st.rerun()
    elif res['status'] == 0:
        st.warning(res['message'])
    else:
        st.error(res['message'])
