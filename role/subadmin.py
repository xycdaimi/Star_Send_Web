import streamlit as st
from streamlit_option_menu import option_menu

from send.check import check_page
from send.detail import display_details
from send.distribute import assign
from send.find import find
from send.history import get_history
from send.manage import manage
from send.person import my_person, change_my_person
from send.send import send
from sql import xie
from sql.connect import create_connection, mask_phone_number


def sub_admin():
    if st.session_state.detail != "":
        display_details()
    elif st.session_state.history_list:
        get_history()
    elif st.session_state.user_edit:
        change_my_person()
    elif st.session_state.distribute != "":
        manage()
    else:
        # 设置导航栏的宽度
        selected0 = option_menu(None, ["快递", "寄件", '审核', '分配', '我的'],
                                icons=['envelope', 'send', 'check', 'list-task', 'person'],
                                menu_icon="cast", default_index=0, orientation="horizontal")
        if selected0 == '快递':
            find()
        elif selected0 == '寄件':
            send()
        elif selected0 == '审核':
            check_page()
        elif selected0 == '分配':
            assign()
        elif selected0 == '我的':
            my_person()
    with st.sidebar:
        st.title(st.session_state.username)
        st.header(mask_phone_number(st.session_state.tel))
        user_edit = st.button('修改个人信息', use_container_width=True)
        history = st.button('历史记录', use_container_width=True)
        qut = st.button('退出登录', key="quit", use_container_width=True)
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
            st.session_state.check_page = 1
            st.session_state.distribute_page = 1
            st.session_state.distribute = ""
            st.session_state.manage_page = 1
            st.rerun()
