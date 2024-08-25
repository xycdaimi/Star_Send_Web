import streamlit as st

from sql.connect import create_connection
from sql import du, xie


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
    data = st.session_state.distribute
    for usr in res['data']:
        with st.form(usr[0]):
            name, type1 = st.columns(2)
            with name:
                st.write("姓名：" + (usr[1] if usr[1] else ""))
                st.write("地址：" + (usr[5] if usr[5] else ""))
            with type1:
                st.write("类型：" + types[usr[6]])
                st.write("手机号：" + (usr[4] if usr[4] else ""))
            if st.form_submit_button("分配快递", use_container_width=True):
                conn = create_connection()
                tt = xie.jiedan(conn, data[0], 1, usr)
                conn.close()
                if tt['status'] == 1:
                    st.success("分配成功")
                    st.session_state.distribute = ""
                    st.session_state.manage_page = 1
                    st.rerun()
                elif tt['status'] == 0:
                    st.warning(tt['message'])
                else:
                    st.error(tt['message'])


def manage():
    if 'manage_page' not in st.session_state:
        st.session_state.manage_page = 1
    data = st.session_state.distribute
    back = st.button("返回")
    if back:
        st.session_state.distribute = ""
        st.session_state.manage_page = 1
        st.rerun()
    st.title("快递详情")
    # 显示基本信息
    st.header("📜 快递基本信息")
    st.markdown(f"快递单号：**{data[0]}**")
    st.markdown(f"寄件人地址：**{data[3]}**")
    st.markdown(f"收件人地址：**{data[8]}**")
    # 显示快递员列表并允许分配
    st.header("📦 快递员列表")
    search = st.text_input("", placeholder='请输入快递员uid')
    # 从数据库中获取快递员列表
    conn = create_connection()
    res = du.find_kuaidi_paged(conn, st.session_state.uid, search, st.session_state.manage_page)
    conn.close()
    if res['status'] == 1:

        usr_list(res)
        up_page, yeshu, down_page = st.columns(3)
        with up_page:
            if st.button("上一页", use_container_width=True):
                if st.session_state.manage_page > 1:
                    st.session_state.manage_page -= 1
                    st.rerun()
        with yeshu:
            st.markdown("<p style='text-align: center;'>" + str(st.session_state.manage_page) + " / "
                        + str(res['total_pages']) + "</p>", unsafe_allow_html=True)
        with down_page:
            if st.button("下一页", use_container_width=True):
                if st.session_state.manage_page < res['total_pages']:
                    st.session_state.manage_page += 1
                    st.rerun()
    elif res['status'] == 0:
        st.warning(res['message'])
    else:
        st.error(res['message'])
