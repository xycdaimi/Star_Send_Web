import streamlit as st
from streamlit_option_menu import option_menu

from send.detail import display_details
from send.find import find
from send.history import get_history
from send.order import order
from send.paisong import display_paisongs
from send.person import my_person, change_my_person
from send.send import send
from sql import xie
from sql.connect import create_connection, mask_phone_number


def courier():
    if st.session_state.detail != "":
        display_details()
    elif st.session_state.history_list:
        get_history()
    elif st.session_state.user_edit:
        change_my_person()
    elif st.session_state.paisong != "":
        display_paisongs()
    else:
        # 设置导航栏的宽度
        selected0 = option_menu(None, ["快递", "寄件", '订单', '我的'],
                                icons=['envelope', 'send', 'list-task', 'person'],
                                menu_icon="cast", default_index=0, orientation="horizontal")
        if selected0 == '快递':
            find()
        elif selected0 == '寄件':
            send()
        elif selected0 == '订单':
            order()
        elif selected0 == '我的':
            my_person()
    with st.sidebar:
        st.title(st.session_state.username)
        st.header(mask_phone_number(st.session_state.tel))
        user_edit = st.button('修改个人信息', use_container_width=True)
        history = st.button('历史记录', use_container_width=True)
        change_wangdian = st.button('成为网点管理员' if (int(st.session_state.kuaidi) == 2) else '网点管理员资格审核中',
                                    use_container_width=True,
                                    disabled=False if (int(st.session_state.kuaidi) == 2) else True)
        qut = st.button('退出登录', key="quit", use_container_width=True)
        if change_wangdian:
            conn = create_connection()
            res = xie.change(conn, 4, st.session_state.uid)
            conn.close()
            if res['status'] == 1:
                st.session_state.kuaidi = 4
                st.rerun()
            elif res['status'] == 0:
                st.warning(res['message'])
            else:
                st.error(res['message'])
        if history:
            st.session_state.history_list = True
            st.rerun()
        if user_edit:
            st.session_state.user_edit = True
            st.rerun()
        if qut:
            st.session_state.status = False
            st.session_state.login_register = True
            st.session_state.detail = ""
            st.session_state.page1 = 1
            st.session_state.page2 = 1
            st.session_state.page3 = 1
            st.session_state.history_page = 1
            st.session_state.history_list = False
            st.session_state.user_edit = False
            st.session_state.paisong_page = 1
            st.session_state.paisong = ""
            st.rerun()
