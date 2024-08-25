import re
import streamlit as st
from role.admin import admin
from role.courier import courier
from role.subadmin import sub_admin
from role.user import user
from sql.connect import create_connection
from sql.connect import generate_uid
from sql import du
from sql import xie
st.set_page_config(
    page_title="星海寄件",
    page_icon="img/icon.ico",
    layout='centered',
    initial_sidebar_state='expanded',
)
if 'status' not in st.session_state:
    st.session_state['status'] = False
if 'login_register' not in st.session_state:
    st.session_state['login_register'] = True
if 'detail' not in st.session_state:
    st.session_state['detail'] = ""
if 'paisong' not in st.session_state:
    st.session_state.paisong = ""
if 'history_list' not in st.session_state:
    st.session_state['history_list'] = False
if 'user_edit' not in st.session_state:
    st.session_state.user_edit = False
if 'edit' not in st.session_state:
    st.session_state.edit = ""
if 'distribute' not in st.session_state:
    st.session_state.distribute = ""
if not st.session_state['status']:
    # 设置页面标题
    st.title('星海寄件 - 您的快递专家')

    # 添加一些介绍性文字
    st.write('欢迎使用星海寄件，我们提供快速、可靠、安全的快递服务。')
    st.write('无论您需要将包裹送到哪里，我们都能满足您的需求。')

    st.image("img/image1.jpg")

    # 添加一些功能点或者服务介绍
    with st.expander('我们的服务'):
        st.write('我们提供全国范围内的快递服务，包括但不限于：')
        st.markdown('- 快速送达')
        st.markdown('- 实时追踪')
        st.markdown('- 安全包装')
        st.markdown('- 客服支持')

        # 添加一个联系我们的部分
    with st.expander('联系我们'):
        st.write('如果您有任何疑问或需要进一步的帮助，请随时与我们联系：')
        st.write('电话: 123-456-7890')
        st.write('邮箱: [2332607961@qq.com](mailto:2332607961@qq.com)')
    with st.sidebar:
        if st.session_state['login_register']:
            username = st.text_input('账号')
            password = st.text_input('密码', type='password')
        else:
            username = st.text_input('账号')
            password = st.text_input('密码', type='password')
            rePassword = st.text_input('确认密码', type='password')
            phone = st.text_input('手机号')
        login, register = st.columns(2)
        with login:
            submit_login = st.button('登录', use_container_width=True)
        with register:
            submit_register = st.button('注册', use_container_width=True)
        if submit_login and not st.session_state['login_register']:
            st.session_state.login_register = True
            st.rerun()
        elif st.session_state['login_register'] and submit_register:
            st.session_state.login_register = False
            st.rerun()
        elif submit_login and st.session_state['login_register']:
            if username == '':
                st.warning('账号不能为空')
            elif password == '':
                st.warning('密码不能为空')
            else:
                conn = create_connection()
                if conn:
                    res = du.denglu(conn, username, password)
                    if res['status'] == 1:
                        st.session_state['uid'] = res['data'][0]
                        st.session_state['username'] = res['data'][1]
                        st.session_state['password'] = res['data'][2]
                        st.session_state['sex'] = res['data'][3]
                        st.session_state['tel'] = res['data'][4]
                        st.session_state['area'] = res['data'][5]
                        st.session_state['kuaidi'] = res['data'][6]
                        st.session_state['wangdian'] = res['data'][7]
                        st.session_state.status = True
                        st.rerun()
                    elif res['status'] == 0:
                        st.warning(res['message'])
                    else:
                        st.error(res['message'])
                else:
                    st.error('数据库连接失败')
                conn.close()
        elif not st.session_state['login_register'] and submit_register:
            if username == '':
                st.warning('账号不能为空')
            elif password == '':
                st.warning('密码不能为空')
            elif rePassword != password:
                st.warning('两次密码不一致')
            elif phone == '':
                st.warning('手机号不能为空')
            #用正则表达式过滤手机号
            elif not re.match(r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$', phone):
                st.warning('手机号格式不正确')
            else:
                conn = create_connection()
                if conn:
                    flag = du.zhuce(conn, username, phone)
                    if flag['status'] == 1:
                        uid = generate_uid()
                        res = xie.zhuce(conn, uid, username, password, phone)
                        if res['status'] == 1:
                            st.session_state['uid'] = uid
                            st.session_state['username'] = username
                            st.session_state['password'] = password
                            st.session_state['sex'] = None
                            st.session_state['tel'] = phone
                            st.session_state['area'] = None
                            st.session_state['kuaidi'] = 0
                            st.session_state['wangdian'] = None
                            st.session_state.status = True
                            st.rerun()
                        else:
                            st.warning(res['message'])
                    elif flag['status'] == 0:
                        st.warning(flag['message'])
                    else:
                        st.error(flag['message'])
                conn.close()
else:
    if st.session_state.kuaidi == 0 or st.session_state.kuaidi == 1 or st.session_state.kuaidi == 3:
        user()
    elif st.session_state.kuaidi == 2 or st.session_state.kuaidi == 4:
        courier()
    elif st.session_state.kuaidi == 5:
        sub_admin()
    elif st.session_state.kuaidi == 6:
        admin()


