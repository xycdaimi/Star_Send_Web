import re

import streamlit as st

from sql import xie
from sql.connect import create_connection


def change_edit_user():
    data = st.session_state.edit
    if st.button('返回'):
        st.session_state.edit = ""
        st.rerun()
    st.title("修改用户信息")
    username = st.text_input('用户名', value=data[1])
    password = st.text_input('密码', value=data[2], type='password')
    sex = st.radio(
        '性别',
        ('男', '女'),
        index=(0 if data[3] == '男' else 1),
        horizontal=True
    )
    tel = st.text_input('手机号', value=data[4])
    area = st.text_input('地址', value=data[5])
    quanxian = st.radio("权限",
                        ('普通用户', "快递员待审核", "快递员","用户升网点管理员待审核", "快递升网点管理员待审核",
                         "网点管理员", '管理员'), horizontal=True, index=int(data[6]))
    permission = 0
    wangdian = None
    if int(data[6]) == 2:
        wangdian = st.text_input('对应的网点管理员uid', value=data[6])
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
            if quanxian == '普通用户':
                permission = 0
            elif quanxian == '快递员待审核':
                permission = 1
            elif quanxian == '快递员':
                permission = 2
            elif quanxian == '用户升网点管理员待审核':
                permission = 3
            elif quanxian == '快递升网点管理员待审核':
                permission = 4
            elif quanxian == '网点管理员':
                permission = 5
            else:
                permission = 6
            conn = create_connection()
            res = xie.edit_user(conn, data[0], username, password, sex, tel, area, permission, wangdian)
            conn.close()
            if res['status'] == 1:
                st.success('修改成功')
                st.session_state.edit = ""
                st.rerun()
            elif res['status'] == 0:
                st.warning(res['message'])
            else:
                st.error(res['message'])
