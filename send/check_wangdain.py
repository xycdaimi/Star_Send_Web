import streamlit as st

from sql import du, xie
from sql.connect import create_connection
def usr_list2(res):
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
                st.write("用户类型：" + (types[usr[6]] if usr[6] else ""))
                st.write("用户手机号：" + (usr[4] if usr[4] else ""))
            with sub:
                if st.form_submit_button("通过", use_container_width=True, type="primary"):
                    conn = create_connection()
                    res = xie.change(conn, 5, usr[0])
                    conn.close()
                    if res['status'] == 1:
                        st.rerun()
                    elif res['status'] == 0:
                        st.warning(res['message'])
                    else:
                        st.error(res['message'])
                if st.form_submit_button("不通过", use_container_width=True):
                    if usr[6] == 3:
                        conn = create_connection()
                        res = xie.change(conn, 0, usr[0])
                        conn.close()
                        if res['status'] == 1:
                            st.rerun()
                        elif res['status'] == 0:
                            st.warning(res['message'])
                        else:
                            st.error(res['message'])
                    elif usr[6] == 4:
                        conn = create_connection()
                        res = xie.change(conn, 2, usr[0], usr[7])
                        conn.close()
                        if res['status'] == 1:
                            st.rerun()
                        elif res['status'] == 0:
                            st.warning(res['message'])
                        else:
                            st.error(res['message'])


def check_page():
    if 'check_page2' not in st.session_state:
        st.session_state.check_page2 = 1
    conn = create_connection()
    search = st.text_input("", placeholder='请输入用户名或uid')
    res = du.find_check_wangdian(conn, search, st.session_state.check_page2)
    conn.close()
    if res['status'] == 1:
        usr_list2(res)
        up_page, yeshu, down_page = st.columns(3)
        with up_page:
            if st.button("上一页", use_container_width=True):
                if st.session_state.check_page2 > 1:
                    st.session_state.check_page2 -= 1
                    st.rerun()
        with yeshu:
            # 用st.markdown来显示页数，因为st.text无法居中显示页数
            st.markdown("<p style='text-align: center;'>" + str(st.session_state.check_page2) + " / "
                        + str(res['total_pages']) + "</p>", unsafe_allow_html=True)
        with down_page:
            if st.button("下一页", use_container_width=True):
                if st.session_state.check_page2 < res['total_pages']:
                    st.session_state.check_page2 += 1
                    st.rerun()
    elif res['status'] == 0:
        st.warning(res['message'])
    else:
        st.error(res['message'])
