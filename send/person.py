import re
import streamlit as st
from sql.connect import create_connection
from sql import xie
def my_person():
    st.title("个人信息")
    st.subheader('用户名：' + st.session_state.username)
    st.subheader('性别：' + (st.session_state.sex if st.session_state.sex else '未填写'))
    st.subheader('手机号：' + st.session_state.tel)
    st.subheader('地址：' + (st.session_state.area if st.session_state.area else '未填写'))


def change_my_person():
    if st.button('返回'):
        st.session_state.user_edit = False
        st.rerun()
    st.title("修改个人信息")
    username = st.text_input('用户名', value=st.session_state.username)
    password = st.text_input('密码', value=st.session_state.password, type='password')
    sex = st.radio(
        '性别',
        ('男', '女'),
        index=(0 if st.session_state.sex == '男' else 1),
        horizontal=True
    )
    tel = st.text_input('手机号', value=st.session_state.tel)
    area = st.text_input('地址', value=st.session_state.area)

    if st.button('提交'):
        if username == '':
            st.warning('账号不能为空')
        elif password == '':
            st.warning('密码不能为空')
        elif tel == '':
            st.warning('手机号不能为空')
        # 用正则表达式过滤手机号
        elif not re.match(r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$',
                          tel):
            st.warning('手机号格式不正确')
        else:
            conn = create_connection()
            res = xie.update_user(conn, st.session_state.uid, username, password, sex, tel, area)
            conn.close()
            if res['status'] == 1:
                st.success('修改成功')
                st.session_state.username = username
                st.session_state.sex = sex
                st.session_state.tel = tel
                st.session_state.area = area
                st.session_state.user_edit = False
                st.rerun()
            elif res['status'] == 0:
                st.warning(res['message'])
            else:
                st.error(res['message'])
