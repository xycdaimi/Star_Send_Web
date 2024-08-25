from datetime import datetime
import pymysql
from mysql.connector import Error
from pymysql.cursors import DictCursor

# 注册
def zhuce(con, uid, zhan, mima, tel):
    # 构造SQL插入语句，使用参数化查询来防止SQL注入
    sql = "INSERT INTO usr (`uid`, `username`, `password`,`tel`) VALUES (%s, %s, %s, %s)"
    try:
        with con.cursor() as cursor:
            cursor.execute(sql, (uid, zhan, mima, tel))
            rows_affected = cursor.rowcount  # 检查受影响的行数
            if rows_affected == 1:
                # 创建一个新的字典来存储结果
                result = {'status': 1,'message': '注册成功'}
                con.commit()  # 提交事务

            else:
                # 如果插入失败（这通常不应该发生，除非有并发问题或数据库约束），返回一个错误状态
                result = {'status': 0,'message': '注册失败'}

    except pymysql.MySQLError as e:
        result = {'status': -1,'message': f'数据库错误: {e}'}

    return result

#将快递信息插入数据库
def dindan(con, biao_data):
    try:
        with con.cursor() as cursor:
            # 查询寄件人和收件人的UID
            ju_count = "SELECT COUNT(*) FROM usr WHERE tel = %s"
            su_count = "SELECT COUNT(*) FROM usr WHERE tel = %s"

            # 检查寄件人电话号码的行数
            cursor.execute(ju_count, (biao_data['tel1'],))
            count1 = cursor.fetchone()[0]
            if count1 > 1:
                result = {'status': -1, 'message': '数据库错误'}
                return result

                # 检查收件人电话号码的行数
            cursor.execute(su_count, (biao_data['tel2'],))
            count2 = cursor.fetchone()[0]
            if count2 > 1:
                result = {'status': -1, 'message': '数据库错误'}
                return result

                # 现在我们可以安全地执行原始查询来获取UID，因为我们知道每个电话号码只有一个匹配项
            ju = "SELECT uid FROM usr WHERE tel = %s"
            su = "SELECT uid FROM usr WHERE tel = %s"
            cursor.execute(ju, (biao_data['tel1'],))
            data1 = cursor.fetchone()
            cursor.execute(su, (biao_data['tel2'],))
            data2 = cursor.fetchone()


            if data1 and data2:
                # 构造插入语句（使用参数化查询）
                sql = (
                    "INSERT INTO send (订单号, 寄件人uid, 寄件人姓名, 寄件人地址, 寄件人电话, "
                    "寄件人公司, 收件人uid, 收件人姓名, 收件人地址, 收件人电话, 收件人公司, "
                    "物品类型, 物品重量, 寄件方式, 付款方式) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                )
                values = (
                    biao_data['danhao'], data1[0], biao_data['name1'], biao_data['area1'],
                    biao_data['tel1'], biao_data['company1'], data2[0], biao_data['name2'],
                    biao_data['area2'], biao_data['tel2'], biao_data['company2'],
                    biao_data['type'], biao_data['weight'], biao_data['fanshi'], biao_data['fukuan']
                )
                cursor.execute(sql, values)
                rows_affected = cursor.rowcount  # 检查受影响的行数
                if rows_affected == 1:
                    result = {'status': 1, 'message': '订单提交成功'}
                    con.commit()
            else:
                result = {'status': 0, 'message': '寄件人或收件人不存在'}

    except Error as e:
        result = {'status': -1, 'message': f'数据库错误: {e}'}

    return result

def change(con, kuaidi, uid,wangdian=None):
    # 构造SQL更新语句，使用参数化查询来防止SQL注入
    sql = "UPDATE usr SET kuaidi = %s, wangdian = %s WHERE uid = %s"
    try:
        with con.cursor() as cursor:
            # 执行SQL语句
            cursor.execute(sql, (kuaidi, wangdian, uid))  # 注意参数的顺序应与SQL语句中的顺序一致

            rows_affected = cursor.rowcount  # 检查受影响的行数
            if rows_affected == 1:
                # 创建一个新的字典来存储结果
                result = {'status': 1, 'message': '修改成功'}
                con.commit()  # 提交事务

            else:
                # 如果没有行被影响（例如，没有与给定uid匹配的记录），返回一个错误状态
                result = {'status': 0, 'message': '修改失败'}

    except pymysql.MySQLError as e:
        # 如果出现错误，回滚事务并返回一个错误响应
        con.rollback()  # 确保在发生异常时回滚事务
        result = {'status': -1, 'message': f'数据库错误: {e}'}

    return result

# 接单，更新快递状态，并更新快递员信息
def jiedan(con, danhao, type, user):
    # 假设user是一个字典，包含'uid'和'tel'两个键
    try:
        with con.cursor() as cursor:
            if type == 1:
                # 使用datetime.now()来获取当前时间
                now = datetime.now()
                sql = "UPDATE send SET 物流状态 = %s, 派件时间 = %s, 快递员uid = %s, 快递员电话 = %s WHERE 订单号 = %s"
                cursor.execute(sql, (type, now, user[0], user[4], danhao))
            else:
                sql = "UPDATE send SET 物流状态 = %s WHERE 订单号 = %s"
                cursor.execute(sql, (type, danhao))

            rows_affected = cursor.rowcount  # 检查受影响的行数
            if rows_affected == 1:
                # 创建一个新的字典来存储结果
                result = {'status': 1, 'message': '接单成功'}
                con.commit()  # 提交事务

            else:
                # 如果插入失败（这通常不应该发生，除非有并发问题或数据库约束），返回一个错误状态
                result = {'status': 0, 'message': '接单失败'}

    except pymysql.MySQLError as e:
        # 如果出现错误返回一个错误响应
        result = {'status': -1, 'message': f'数据库错误: {e}'}

    return result

# 签收，将物流状态改为2，并更新签收时间，根据订单号查找
def qianshou(con, danhao, type):
    try:
        with con.cursor() as cursor:
            # 使用datetime.now()来获取当前时间
            now = datetime.now()

            sql = "UPDATE send SET 物流状态 = %s, 签收时间 = %s WHERE 订单号 = %s"
            cursor.execute(sql, (type, now, danhao))

            rows_affected = cursor.rowcount  # 检查受影响的行数
            if rows_affected == 1:
                # 创建一个新的字典来存储结果
                result = {'status': 1, 'message': '签收成功'}
                con.commit()  # 提交事务

            else:
                # 如果插入失败（这通常不应该发生，除非有并发问题或数据库约束），返回一个错误状态
                result = {'status': 0, 'message': '签收失败'}


    except pymysql.MySQLError as e:
        # 如果出现错误，回滚事务并返回一个错误响应
        result = {'status': -1, 'message': f'数据库错误: {e}'}

    return result

# 删除用户，根据uid删除
def shan(con, uid):
    try:
        with con.cursor() as cursor:
            # 构造SQL删除语句，使用参数化查询
            sql = "DELETE FROM usr WHERE uid = %s"
            cursor.execute(sql, (uid,))

            rows_affected = cursor.rowcount  # 检查受影响的行数
            if rows_affected == 1:
                # 创建一个新的字典来存储结果
                result = {'status': 1, 'message': '删除成功'}
                con.commit()  # 提交事务

            else:
                # 如果插入失败（这通常不应该发生，除非有并发问题或数据库约束），返回一个错误状态
                result = {'status': 0, 'message': '删除失败'}

    except pymysql.MySQLError as e:
        # 如果出现错误，回滚事务并返回一个错误响应
        result = {'status': -1, 'message': f'数据库错误: {e}'}

    return result

# 删除快递，根据订单号删除
def shanchu(con, danhao):
    try:
        with con.cursor(DictCursor) as cursor:
            # 构造SQL删除语句，使用参数化查询
            sql = "DELETE FROM send WHERE 订单号 = %s"

            cursor.execute(sql, (danhao,))

            rows_affected = cursor.rowcount  # 检查受影响的行数
            if rows_affected == 1:
                # 创建一个新的字典来存储结果
                result = {'status': 1, 'message': '删除成功'}
                con.commit()  # 提交事务

            else:
                # 如果插入失败，返回一个错误状态
                result = {'status': 0, 'message': '删除失败'}

    except pymysql.MySQLError as e:
        # 如果出现错误，回滚事务并返回一个错误响应
        result = {'status': -1, 'message': f'数据库错误: {e}'}

    return result

# 更新用户信息
def update_user(con, uid, zhan, mima, sex, tel, area):
    try:
        with con.cursor() as cursor:
            # 构造SQL更新语句，使用参数化查询
            sql = "UPDATE usr SET username = %s, password = %s, sex = %s, tel = %s, area = %s WHERE uid = %s"
            cursor.execute(sql, (zhan, mima, sex, tel, area, uid))

            rows_affected = cursor.rowcount  # 检查受影响的行数
            if rows_affected == 1:
                # 创建一个新的字典来存储结果
                result = {'status': 1, 'message': '更新成功'}
                con.commit()  # 提交事务

            else:
                # 如果没有行被更新（可能是uid不存在或其他原因），返回一个错误状态
                result = {'status': 0, 'message': '更新失败，可能用户不存在或数据未变动'}

    except pymysql.MySQLError as e:
        # 如果出现错误，回滚事务并返回一个错误响应
        con.rollback()  # 添加回滚操作
        result = {'status': -1, 'message': f'数据库错误: {e}'}

    return result

def edit_user(con, uid, zhan, mima, sex, tel, area, prm,guanliuid=None):
    try:
        with con.cursor() as cursor:
            # 构造SQL更新语句，使用参数化查询
            if guanliuid == None:
                sql = "UPDATE usr SET username = %s, password = %s, sex = %s, tel = %s, area = %s,kuaidi = %s WHERE uid = %s"
                cursor.execute(sql, (zhan, mima, sex, tel, area, prm, uid))
            else:
                sql = "UPDATE usr SET username = %s, password = %s, sex = %s, tel = %s, area = %s, kuaidi = %s,wangdian = %s WHERE uid = %s"
                cursor.execute(sql, (zhan, mima, sex, tel, area, prm, guanliuid, uid))

            rows_affected = cursor.rowcount  # 检查受影响的行数
            if rows_affected == 1:
                # 创建一个新的字典来存储结果
                result = {'status': 1, 'message': '更新成功'}
                con.commit()  # 提交事务

            else:
                # 如果没有行被更新（可能是uid不存在或其他原因），返回一个错误状态
                result = {'status': 0, 'message': '更新失败，可能用户不存在或数据未变动'}

    except pymysql.MySQLError as e:
        # 如果出现错误，回滚事务并返回一个错误响应
        con.rollback()  # 添加回滚操作
        result = {'status': -1, 'message': f'数据库错误: {e}'}

    return result