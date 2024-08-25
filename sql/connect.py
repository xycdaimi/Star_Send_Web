import mysql.connector
import uuid
import random


def create_connection():
    try:
        con = mysql.connector.connect(
            host="localhost",
            port=3306,  # 端口号应该是整数，不是字符串
            user="root",
            password="xyc287224546,a",
            database="star"
        )
        return con
    except mysql.connector.Error as e:
        print(f"数据库连接出错: {e}")
        return None


# 定义一个函数，用来生成随机的uid
def generate_uid(size=16):
    full_uuid = str(uuid.uuid4())
    uid = ''.join(random.choices(full_uuid, k=size))
    return uid


# 定义一个函数，将11位的电话号码中间的数字改为*
def mask_phone_number(phone_number):
    if len(phone_number) == 11:
        return phone_number[:3] + '****' + phone_number[7:]
    else:
        return phone_number
