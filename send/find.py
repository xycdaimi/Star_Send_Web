import streamlit as st
from streamlit_option_menu import option_menu
from sql.connect import create_connection
from sql import du


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
                st.session_state.detail = send
                st.rerun()


def find():
    if 'page1' not in st.session_state:
        st.session_state.page1 = 1
    if 'page2' not in st.session_state:
        st.session_state.page2 = 1
    if 'page3' not in st.session_state:
        st.session_state.page3 = 1
    search = st.text_input("", placeholder='请输入订单号')
    if search != "":
        conn = create_connection()
        res = du.search(conn, search, st.session_state.page3)
        conn.close()
        if res['status']:
            send_list(res)
            up_page, yeshu, down_page = st.columns(3)
            with up_page:
                if st.button("上一页", use_container_width=True):
                    if st.session_state.page3 > 1:
                        st.session_state.page3 -= 1
                        st.rerun()
            with yeshu:
                # 用st.markdown来显示页数，因为st.text无法居中显示页数
                st.markdown("<p style='text-align: center;'>" + str(st.session_state.page3) + " / "
                            + str(res['total_pages']) + "</p>", unsafe_allow_html=True)
            with down_page:
                if st.button("下一页", use_container_width=True):
                    if st.session_state.page3 < res['total_pages']:
                        st.session_state.page3 += 1
                        st.rerun()
        elif res['status'] == 0:
            st.warning(res['message'])
        else:
            st.error(res['message'])
    else:
        selected1 = option_menu(None, ["我的寄件", "我的收件"],
                                menu_icon="cast", default_index=0, orientation="horizontal")
        if selected1 == "我的寄件":
            conn = create_connection()
            res = du.jifenye(conn, st.session_state.uid, st.session_state.page1)
            conn.close()
            if res['status']:
                send_list(res)
                up_page, yeshu, down_page = st.columns(3)
                with up_page:
                    if st.button("上一页", use_container_width=True):
                        if st.session_state.page1 > 1:
                            st.session_state.page1 -= 1
                            st.rerun()
                with yeshu:
                    st.markdown("<p style='text-align: center;'>" + str(st.session_state.page1) + " / "
                                + str(res['total_pages']) + "</p>", unsafe_allow_html=True)
                with down_page:
                    if st.button("下一页", use_container_width=True):
                        if st.session_state.page1 < res['total_pages']:
                            st.session_state.page1 += 1
                            st.rerun()
            elif res['status'] == 0:
                st.warning(res['message'])
            else:
                st.error(res['message'])
        elif selected1 == "我的收件":
            conn = create_connection()
            res = du.shoufenye(conn, st.session_state.uid, st.session_state.page2)
            conn.close()
            if res['status']:
                send_list(res)
                up_page, yeshu, down_page = st.columns(3)
                with up_page:
                    if st.button("上一页", use_container_width=True):
                        if st.session_state.page2 > 1:
                            st.session_state.page2 -= 1
                            st.rerun()
                with yeshu:
                    st.markdown("<p style='text-align: center;'>" + str(st.session_state.page2) + " / "
                                + str(res['total_pages']) + "</p>", unsafe_allow_html=True)
                with down_page:
                    if st.button("下一页", use_container_width=True):
                        if st.session_state.page2 < res['total_pages']:
                            st.session_state.page2 += 1
                            st.rerun()
            elif res['status'] == 0:
                st.warning(res['message'])
            else:
                st.error(res['message'])
