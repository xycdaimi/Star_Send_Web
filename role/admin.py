import streamlit as st
from streamlit_option_menu import option_menu

from send.detail import display_details
from send.edit import change_edit_user
from sql import connect, du
from send import check_wangdain
from sql import xie


def send_list(res):
    for send in res['data']:
        with st.form(send[0]):
            st.subheader("运单号：" + send[0])
            tel, sendTime = st.columns(2)
            with tel:
                st.write("收件人手机号：" + send[9])
            with sendTime:
                st.write("派件时间：" + str(send[14] if send[14] else "未派送"))
            if st.form_submit_button("订单详情", use_container_width=True):
                st.session_state.detail = send
                st.rerun()
            if st.form_submit_button("删除", use_container_width=True):
                con = connect.create_connection()
                xie.shanchu(con, send[0])
                st.rerun()


def usr_list(res):
    types = {
        0: "普通用户",
        1: "快递员待审批",
        2: "快递员",
        3: "网点管理员待审批",
        4: "网点管理员待审批",
        5: "网点管理员",
        6: "超级管理员"
    }
    for usr in res['data']:
        with st.form(usr[0]):
            name, type, sub = st.columns(3)
            with name:
                st.write("用户名：" + (usr[1] if usr[1] else ""))
                st.write("用户地址：" + (usr[5] if usr[5] else ""))
            with type:
                st.write("用户类型：" + types[usr[6]])
                st.write("用户手机号：" + (usr[4] if usr[4] else ""))
            with sub:
                if st.form_submit_button("编辑", use_container_width=True):
                    st.session_state.edit = usr
                    st.rerun()
                if st.form_submit_button("删除", use_container_width=True):
                    con = connect.create_connection()
                    xie.shan(con, usr[0])
                    con.close()
                    st.rerun()


def admin():
    if 'user_page1' not in st.session_state:
        st.session_state.user_page1 = 1
    if 'user_page2' not in st.session_state:
        st.session_state.user_page2 = 1
    if 'user_page3' not in st.session_state:
        st.session_state.user_page3 = 1
    if 'kuaidi_page' not in st.session_state:
        st.session_state.kuaidi_page = 1
    if st.session_state.detail != "":
        display_details()
    elif st.session_state.edit != "":
        change_edit_user()
    else:
        # 设置导航栏的宽度
        selected0 = option_menu(None, ["查询用户", "查询快递", '审批网点管理员'],
                                icons=['people', 'envelope', 'book'],
                                menu_icon="cast", default_index=0, orientation="horizontal")
        if selected0 == '查询用户':
            selected0 = option_menu(None, ["查询普通用户", "查询快递员", '查询网点管理员'],
                                    menu_icon="cast", default_index=0, orientation="horizontal",
                                    styles={
                                        "container": {
                                            "padding": "2px !important",  # 减小内边距
                                            "margin": "0 !important",  # 移除外边距
                                            "background-color": "#fafafa",  # 背景色
                                            "width": "100% !important",  # 导航栏宽度设置为80
                                            "height": "50px",  # 导航栏高度设置为50px
                                        },
                                    })

            if selected0 == '查询普通用户':
                yy = st.text_input(label='普通用户查询', placeholder='请输入要查询的用户名称')
                con = connect.create_connection()
                result = du.searchyonghulike(con, yy, st.session_state.user_page1)
                con.close()
                if result['status'] == 1:
                    usr_list(result)
                    up_page, yeshu, down_page = st.columns(3)
                    with up_page:
                        if st.button("上一页", use_container_width=True):
                            if st.session_state.user_page1 > 1:
                                st.session_state.user_page1 -= 1
                                st.rerun()
                    with yeshu:
                        # 用st.markdown来显示页数，因为st.text无法居中显示页数
                        st.markdown("<p style='text-align: center;'>" + str(st.session_state.user_page1) + " / "
                                    + str(result['total_pages']) + "</p>", unsafe_allow_html=True)
                    with down_page:
                        if st.button("下一页", use_container_width=True):
                            if st.session_state.user_page1 < result['total_pages']:
                                st.session_state.user_page1 += 1
                                st.rerun()
                elif result['status'] == 0:
                    st.warning(result['message'])
                else:
                    st.error(result['message'])
                if yy != "":
                    if result['status'] == 0:
                        st.warning(result['message'])
                    elif result['status'] == -1:
                        st.error(result['message'])

            elif selected0 == '查询快递员':
                yy = st.text_input(label='快递员查询', placeholder='请输入要查询的快递员名称')
                con = connect.create_connection()
                result = du.searchkuaidilike(con, yy, st.session_state.user_page2)
                con.close()
                if result['status'] == 1:
                    usr_list(result)
                    up_page, yeshu, down_page = st.columns(3)
                    with up_page:
                        if st.button("上一页", use_container_width=True):
                            if st.session_state.user_page2 > 1:
                                st.session_state.user_page2 -= 1
                                st.rerun()
                    with yeshu:
                        # 用st.markdown来显示页数，因为st.text无法居中显示页数
                        st.markdown("<p style='text-align: center;'>" + str(st.session_state.user_page2) + " / "
                                    + str(result['total_pages']) + "</p>", unsafe_allow_html=True)
                    with down_page:
                        if st.button("下一页", use_container_width=True):
                            if st.session_state.user_page2 < result['total_pages']:
                                st.session_state.user_page2 += 1
                                st.rerun()
                elif result['status'] == 0:
                    st.warning(result['message'])
                else:
                    st.error(result['message'])
                if yy != "":
                    if result['status'] == 0:
                        st.warning(result['message'])
                    elif result['status'] == -1:
                        st.error(result['message'])

            elif selected0 == '查询网点管理员':
                yy = st.text_input(label='网点管理员查询', placeholder='请输入要查询的网点管理员名称')
                con = connect.create_connection()
                result = du.searchwangdianlike(con, yy)
                con.close()
                if result['status'] == 1:
                    usr_list(result)
                    up_page, yeshu, down_page = st.columns(3)
                    with up_page:
                        if st.button("上一页", use_container_width=True):
                            if st.session_state.user_page3 > 1:
                                st.session_state.user_page3 -= 1
                                st.rerun()
                    with yeshu:
                        # 用st.markdown来显示页数，因为st.text无法居中显示页数
                        st.markdown("<p style='text-align: center;'>" + str(st.session_state.user_page3) + " / "
                                    + str(result['total_pages']) + "</p>", unsafe_allow_html=True)
                    with down_page:
                        if st.button("下一页", use_container_width=True):
                            if st.session_state.user_page3 < result['total_pages']:
                                st.session_state.user_page3 += 1
                                st.rerun()
                elif result['status'] == 0:
                    st.warning(result['message'])
                else:
                    st.error(result['message'])
                if yy != "":
                    if result['status'] == 0:
                        st.warning(result['message'])
                    elif result['status'] == -1:
                        st.error(result['message'])

        elif selected0 == '查询快递':
            xx = st.text_input(label='查询快递', placeholder='请输入要查询的订单号')
            con = connect.create_connection()
            result = du.search(con, xx, st.session_state.kuaidi_page)
            con.close()
            if result['status'] == 1:
                send_list(result)
                up_page, yeshu, down_page = st.columns(3)
                with up_page:
                    if st.button("上一页", use_container_width=True):
                        if st.session_state.kuaidi_page > 1:
                            st.session_state.kuaidi_page -= 1
                            st.rerun()
                with yeshu:
                    # 用st.markdown来显示页数，因为st.text无法居中显示页数
                    st.markdown("<p style='text-align: center;'>" + str(st.session_state.kuaidi_page) + " / "
                                + str(result['total_pages']) + "</p>", unsafe_allow_html=True)
                with down_page:
                    if st.button("下一页", use_container_width=True):
                        if st.session_state.kuaidi_page < result['total_pages']:
                            st.session_state.kuaidi_page += 1
                            st.rerun()
            elif result['status'] == 0:
                st.warning(result['message'])
            else:
                st.error(result['message'])
            if xx != "":
                if result['status'] == -1:
                    st.error(result['message'])
                elif result['status'] == 0:
                    st.warning(result['message'])
        elif selected0 == '审批网点管理员':
            check_wangdain.check_page()
    with st.sidebar:
        st.title(st.session_state.username)
        qut = st.button('退出登录', key="quit", use_container_width=True)
        if qut:
            st.session_state.status = False
            st.session_state.login_register = True
            st.session_state.detail = ""
            st.session_state.user_page1 = 1
            st.session_state.user_page2 = 1
            st.session_state.user_page3 = 1
            st.session_state.kuaidi_page = 1
            st.session_state.edit = ""
            st.rerun()

