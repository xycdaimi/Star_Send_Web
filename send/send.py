import re
import streamlit as st
from sql.connect import create_connection
from sql import xie
from sql.connect import generate_uid


def send():
    sender, consignee = st.columns(2)
    if 'sender_name' not in st.session_state:
        st.session_state['sender_name'] = ''
    if 'sender_phone' not in st.session_state:
        st.session_state['sender_phone'] = ''
    if 'sender_address' not in st.session_state:
        st.session_state['sender_address'] = ''
    if 'sender_company' not in st.session_state:
        st.session_state['sender_company'] = ''
    if 'consignee_name' not in st.session_state:
        st.session_state['consignee_name'] = ''
    if 'consignee_phone' not in st.session_state:
        st.session_state['consignee_phone'] = ''
    if 'consignee_address' not in st.session_state:
        st.session_state['consignee_address'] = ''
    if 'consignee_company' not in st.session_state:
        st.session_state['consignee_company'] = ''
    with sender:
        sender_name = st.text_input('寄件人姓名', placeholder='必填', value=st.session_state.sender_name)
        sender_phone = st.text_input('寄件人手机号', placeholder='必填', value=st.session_state.sender_phone)
        sender_address = st.text_input('寄件人地址', placeholder='必填', value=st.session_state.sender_address)
        sender_company = st.text_input('寄件人公司', placeholder='选填', value=st.session_state.sender_company)
    with consignee:
        consignee_name = st.text_input('收件人姓名', placeholder='必填', value=st.session_state.consignee_name)
        consignee_phone = st.text_input('收件人手机号', placeholder='必填', value=st.session_state.consignee_phone)
        consignee_address = st.text_input('收件人地址', placeholder='必填', value=st.session_state.consignee_address)
        consignee_company = st.text_input('收件人公司', placeholder='选填', value=st.session_state.consignee_company)
    # 设置单选框，选择寄送的快递的类别，是文件，果蔬，医药，食品，大件，其他
    area = st.button('地址薄', use_container_width=True)
    category = st.radio(
        '物品类型',
        ('文件', '果蔬', '医药', '食品', '大件', '其他'), horizontal=True)

    # 设置一个用户可以调节设置物品的重量的可以点击增加的滑块
    weight = st.slider('物品重量', 0.0, 100.0, 1.0, 1.0)
    # 设置寄件方式
    mode = st.radio(
        '寄件方式',
        ('服务点自寄', '上门取件', '自行联系快递员'), horizontal=True)
    # 设置付款方式
    payment = st.radio(
        '付款方式',
        ('寄付现结', '到付', '寄付月结'), horizontal=True)
    # 下单按钮
    submit = st.button('下单', use_container_width=True)
    if area:
        st.session_state.sender_name = st.session_state.username
        st.session_state.sender_phone = st.session_state.tel
        st.session_state.sender_address = st.session_state.area
        st.rerun()
    if submit:
        if sender_name == "" or sender_phone == "" or sender_address == "":
            st.warning("寄件人信息不完整")
        elif consignee_name == "" or consignee_phone == "" or consignee_address == "":
            st.warning("收件人信息不完整")
        elif not re.match(r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|'
                          r'(18[0-9])|166|198|199|(147))\d{8}$', sender_phone):
            st.warning("寄件人手机号格式错误")
        elif not re.match(r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|'
                          r'(18[0-9])|166|198|199|(147))\d{8}$', consignee_phone):
            st.warning("收件人手机号格式错误")
        else:
            if category == '文件':
                category = 0
            elif category == '果蔬':
                category = 1
            elif category == '医药':
                category = 2
            elif category == '食品':
                category = 3
            elif category == '大件':
                category = 4
            else:
                category = 5
            if mode == '服务点自寄':
                mode = 0
            elif mode == '上门取件':
                mode = 1
            else:
                mode = 2
            if payment == '寄付现结':
                payment = 0
            elif payment == '到付':
                payment = 1
            else:
                payment = 2
            conn = create_connection()
            danhao = generate_uid(18)
            data = {'danhao': danhao, 'name1': sender_name, 'area1': sender_address,
                    'tel1': sender_phone, 'company1': sender_company, 'name2': consignee_name,
                    'area2': consignee_address, 'tel2': consignee_phone, 'company2': consignee_company,
                    'type': category, 'weight': weight, 'fanshi': mode, 'fukuan': payment}
            res = xie.dindan(conn, data)
            conn.close()
            if res['status'] == 1:
                st.success(res['message'])
                st.session_state.sender_name = ""
                st.session_state.sender_phone = ""
                st.session_state.sender_address = ""
                st.session_state.sender_company = ""
                st.session_state.consignee_name = ""
                st.session_state.consignee_phone = ""
                st.session_state.consignee_address = ""
                st.session_state.consignee_company = ""
                st.rerun()
            elif res['status'] == 0:
                st.warning(res['message'])
            else:
                st.error(res['message'])
