import pymysql
from mysql.connector import Error

# 注册查询
def zhuce(con, zhan=None, tel=None):
    # 构造SQL查询语句，使用参数化查询来防止SQL注入
    sql = "SELECT COUNT(username) AS flag FROM usr WHERE username = %s OR tel = %s"
    status = 0  # 假设查询失败

    try:
        with con.cursor() as cursor:
            cursor.execute(sql, (zhan, tel))
            data = cursor.fetchone()
            flag = data[0]
            if flag == 0:  # 用户不存在，可以注册
                status = 1
                result = {'status': status, 'message': '可以注册'}
            else:  # 用户已存在，注册失败
                result = {'status': status, 'message': '用户已存在'}

    except pymysql.MySQLError as e:
        print(f"数据库查询出错: {e}")
        status = -1  # 查询失败
        result = {'status': status, 'message': f'数据库错误: {e}'}

    # 总是返回result字典
    return result

# 登录查询
def denglu(con, zhan, mima):
    try:
        with con.cursor() as cursor:
            # 查询用户密码
            query = "SELECT * FROM usr WHERE (username = %s OR tel = %s)"
            cursor.execute(query, (zhan, zhan))
            data = cursor.fetchone()

            if data:
                # 用户存在，验证密码
                if data[2] == mima:
                    result = {'status': 1, 'message': '登录成功', 'data': data}

                else:
                    # 密码不正确，返回0表示登录失败
                    result = {'status': 0, 'message': '密码不正确'}
            else:
                # 用户不存在，返回0表示登录失败
                result = {'status': 0, 'message': '用户不存在'}

    except pymysql.MySQLError as e:
        print(f"数据库查询出错: {e}")
        result = {'status': -1, 'message': f'数据库错误: {e}'}

    return result

# 查询订单根据订单号
def search(con, danhao, page=1):
    page_size = 4
    try:
        # Calculate total number of pages
        with con.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM send WHERE 订单号 like %s", ("%"+danhao+"%",))
            total_count = cursor.fetchone()[0]
            if total_count == 0:
                return {'status': 0, 'message': '订单号不存在', 'data': [], 'total_pages': 0}
            total_pages = -(-total_count // page_size)  # Equivalent to math.ceil(total_count / page_size)

        # Ensure page number is valid
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages

            # Perform the query
        start = (page - 1) * page_size
        sql = "SELECT * FROM send WHERE 订单号 like %s LIMIT %s, %s"
        with con.cursor() as cursor:
            cursor.execute(sql, ("%"+danhao+"%", start, page_size))
            data = cursor.fetchall()
            result = {'status': 1, 'message': '查询成功', 'data': data, 'total_pages': total_pages}
    except Error as e:
        # Handle database errors
        result = {'status': -1, 'message': f'数据库错误: {e}', 'data': [], 'total_pages': 0}
    except Exception as e:
        # Handle other types of errors
        result = {'status': -1, 'message': f'未知错误: {e}', 'data': [], 'total_pages': 0}

    return result

# 查询用户根据用户名或uid
def searchyonghu(con, yonghu):
    # 构造SQL查询语句，使用参数化查询来防止SQL注入
    sql = "SELECT * FROM usr WHERE uid = %s OR username = %s"
    try:
        with con.cursor() as cursor:
            # 使用参数化查询
            cursor.execute(sql, (yonghu, yonghu))
            # fetchall() 方法返回所有查询结果
            data = cursor.fetchall()
            if data:
                result= {'status': 1, 'message': '查询成功', 'data': data}
            else:
                result = {'status': 0, 'message': '用户不存在', 'data': []}

    except pymysql.MySQLError as e:
        print(f"数据库查询出错: {e}")
        result = {'status': -1, 'message': f'数据库错误: {e}', 'data': []}

    return result

# 查询快递员
def searchkuaidi(con, kuaiyuan):
    sql = "SELECT * FROM usr WHERE (uid = %s OR username = %s) AND kuaidi = 2"
    try:
        with con.cursor() as cursor:
            cursor.execute(sql, (kuaiyuan, kuaiyuan))
            data = cursor.fetchall()
            if data:
                result= {'status': 1, 'message': '查询成功', 'data': data}

            else:
                result = {'status': 0, 'message': '用户不存在','data': []}
    except pymysql.MySQLError as e:
        result = {'status': -1, 'message': f'数据库错误: {e}', 'data': []}

    return result

# 查询网点管理员
def search_wang(con):
    # 构造SQL查询语句，使用参数化查询来防止SQL注入
    # 注意：由于kuaidi是一个具体的值，这里不需要参数化
    sql = "SELECT username FROM usr WHERE kuaidi = 5"
    try:
        with con.cursor() as cursor:
            cursor.execute(sql)
            # 使用fetchall()来获取所有匹配的行
            data = cursor.fetchall()
            if data:
                # 将结果转换为列表，其中每个元素是一个字典，包含username
                result_list = [{'username': row[0]} for row in data]
                result = {'status': 1, 'message': '查询成功', 'data': result_list}
            else:
                result = {'status': 0, 'message': '没有找到网点管理员'}
    except pymysql.MySQLError as e:
        result = {'status': -1, 'message': f'数据库错误: {e}'}

        # 将数据返回
    return result

# 查询寄件的快递信息
def jifenye(con, uid, page=1):
    page_size = 4
    try:
        # Calculate total number of pages
        with con.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM send WHERE 寄件人uid=%s and 物流状态 < 5", (uid,))
            total_count = cursor.fetchone()[0]
            if total_count == 0:
                return {'status': 0, 'message': '没有寄件快递', 'data': [], 'total_pages': 0}
            total_pages = -(-total_count // page_size)  # Equivalent to math.ceil(total_count / page_size)

        # Ensure page number is valid
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages

            # Perform the query
        start = (page - 1) * page_size
        sql = "SELECT * FROM send WHERE 寄件人uid=%s and 物流状态 < 5 LIMIT %s, %s"
        with con.cursor() as cursor:
            cursor.execute(sql, (uid, start, page_size))
            data = cursor.fetchall()
            result = {'status': 1, 'message': '查询成功', 'data': data, 'total_pages': total_pages}
    except Error as e:
        # Handle database errors
        result = {'status': -1, 'message': f'数据库错误: {e}', 'data': [], 'total_pages': 0}
    except Exception as e:
        # Handle other types of errors
        result = {'status': -1, 'message': f'未知错误: {e}', 'data': [], 'total_pages': 0}

    return result

#查询收件的快递信息
def shoufenye(con, uid, page=1):
    page_size = 4
    try:
        # 计算总页数
        with con.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM send WHERE 收件人uid=%s and 物流状态 < 5", (uid,))
            total_count = cursor.fetchone()[0]
            if total_count == 0:
                return {'status': 0, 'message': '没有收件快递', 'data': [], 'total_pages': 0}
            total_pages = -(-total_count // page_size)  # 相当于math.ceil(total_count / page_size)

        # 确保页数是有效的
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages

            # 执行查询
        start = (page - 1) * page_size
        sql = f"SELECT * FROM send WHERE 收件人uid=%s and 物流状态 < 5 LIMIT %s, %s"
        with con.cursor() as cursor:
            cursor.execute(sql, (uid, start, page_size))
            data = cursor.fetchall()
            result = {'status': 1, 'message': '查询成功', 'data': data, 'total_pages': total_pages}

    except Error as e:
        # 处理数据库错误
        result = {'status': -1, 'message': f'数据库错误: {e}', 'data': [], 'total_pages': 0}
    except Exception as e:
        # 处理其他类型的错误
        result = {'status': -1, 'message': f'未知错误: {e}', 'data': [], 'total_pages': 0}

        # 返回结果
    return result


def history_lishi(con, uid, text, page=1):
    page_size = 4
    try:
        # 计算总页数
        with con.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM send WHERE (收件人uid=%s or 寄件人uid =%s) and 物流状态 = 5 and 订单号 like %s", (uid , uid , "%"+text+"%",))
            total_count = cursor.fetchone()[0]
            if total_count == 0:
                return {'status': 0, 'message': '没有历史记录', 'data': [], 'total_pages': 0}
            total_pages = -(-total_count // page_size)  # 相当于math.ceil(total_count / page_size)

        # 确保页数是有效的
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages

            # 执行查询
        start = (page - 1) * page_size
        sql = f"SELECT * FROM send WHERE (收件人uid=%s or 寄件人uid =%s) and 物流状态 = 5 and 订单号 like %s ORDER BY 派件时间 DESC LIMIT %s, %s"
        with con.cursor() as cursor:
            cursor.execute(sql, (uid,uid,"%"+text+"%", start, page_size))
            data = cursor.fetchall()
            result = {'status': 1, 'message': '查询成功', 'data': data, 'total_pages': total_pages}

    except Error as e:
        # 处理数据库错误
        result = {'status': -1, 'message': f'数据库错误: {e}', 'data': [], 'total_pages': 0}
    except Exception as e:
        # 处理其他类型的错误
        result = {'status': -1, 'message': f'未知错误: {e}', 'data': [], 'total_pages': 0}

        # 返回结果
    return result


# 派件员未接单的快递
def jiedan(con, search_order_id=None, page=1):
    page_size = 4

    def execute_query(search_condition, page_num):
        with con.cursor() as cursor:
            # 如果没有搜索条件或搜索条件为空字符串，则只考虑物流状态为0的订单
            if search_condition is None or search_condition == "":
                cursor.execute("SELECT COUNT(*) FROM send WHERE 物流状态 = 0")
                sql = "SELECT * FROM send WHERE 物流状态 = 0 LIMIT %s, %s"
            else:
                # 如果有搜索条件，则同时考虑物流状态和订单号
                cursor.execute("SELECT COUNT(*) FROM send WHERE 物流状态 = 0 AND 订单号 = %s", (search_condition,))
                sql = "SELECT * FROM send WHERE 物流状态 = 0 AND 订单号 = %s LIMIT %s, %s"

            total_count = cursor.fetchone()[0]

            if total_count == 0:
                return None  # 表示没有找到匹配的订单

            total_pages = -(-total_count // page_size)  # 相当于math.ceil(total_count / page_size)

            # 确保页数是有效的
            page_num = max(1, min(page_num, total_pages))

            start = (page_num - 1) * page_size

            # 执行查询（根据搜索条件和分页）
            cursor.execute(sql, (start, page_size) if search_condition is None or search_condition == "" else (
            search_condition, start, page_size))

            results = cursor.fetchall()
            return {'status': 1, 'message': '查询成功', 'data': results, 'total_pages': total_pages}

    try:
        # 尝试执行查询
        result = execute_query(search_order_id, page)  # 将page传递给execute_query函数
        if result is None:
            return {'status': 0, 'message': '没有找到匹配的订单', 'data': [], 'total_pages': 0}
        else:
            return result

    except Exception as e:
        # 处理异常
        return {'status': 0, 'message': f'查询出错: {e}', 'data': [], 'total_pages': 0}

#查询快递订单
def find_send(con, page=1, search=None):
    page_size = 4

    try:
        # 计算总页数（根据搜索条件）
        with con.cursor() as cursor:
            if search is None:
                # 如果没有搜索条件，则计算所有订单的总数
                cursor.execute("SELECT COUNT(*) FROM send")
            else:
                # 如果有搜索条件，则计算匹配订单号的订单总数
                cursor.execute("SELECT COUNT(*) FROM send WHERE 订单号 LIKE %s", ('%' + search + '%',))
            total_count = cursor.fetchone()[0]

            if total_count == 0:
                return {'status': 0, 'message': '没有找到匹配的订单', 'data': [], 'total_pages': 0}

            total_pages = -(-total_count // page_size)  # 相当于math.ceil(total_count / page_size)

        # 确保页数是有效的
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages

            # 计算起始索引
        start = (page - 1) * page_size

        # 执行查询（根据搜索条件和分页）
        sql = "SELECT * FROM send"
        params = ()
        if search is not None:
            sql += " WHERE 订单号 LIKE %s"
            params = ('%' + search + '%',)
        sql += " LIMIT %s, %s"
        params += (start, page_size)

        with con.cursor() as cursor:
            cursor.execute(sql, params)
            data = cursor.fetchall()

            # 返回结果
        return {
            'status': 1,
            'message': '查询成功',
            'data': data,
            'total_pages': total_pages
        }

    except Exception as e:
        # 处理异常
        return {
            'status': -1,
            'message': f'查询出错: {e}',
            'data': [],
            'total_pages': 0
        }

# 查询所有用户
def yonghu(con, page=1, search=None):
    page_size = 4

    try:
        # 计算总行数（首先根据搜索条件过滤）
        with con.cursor() as cursor:
            # 如果没有搜索条件，则只考虑kuaidi小于6的用户
            if search is None:
                cursor.execute("SELECT COUNT(*) FROM usr WHERE kuaidi < 6")
            else:
                # 如果提供了搜索条件，则同时考虑kuaidi和uid或username
                cursor.execute("SELECT COUNT(*) FROM usr WHERE kuaidi < 6 AND (uid = %s OR username LIKE %s)",
                               (search, '%' + search + '%'))
            total_count = cursor.fetchone()[0]

            if total_count == 0:
                return {'status': 0, 'message': '没有找到匹配的用户', 'data': [], 'total_pages': 0}

            total_pages = -(-total_count // page_size)  # 相当于math.ceil(total_count / page_size)

        # 确保页数是有效的
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages

            # 计算起始索引
        start = (page - 1) * page_size

        # 执行查询（根据搜索条件和分页）
        if search is None:
            sql = "SELECT * FROM usr WHERE kuaidi < 6 LIMIT %s, %s"
        else:
            sql = "SELECT * FROM usr WHERE kuaidi < 6 AND (uid = %s OR username LIKE %s) LIMIT %s, %s"
            # 注意：这里我们使用search两次，一次用于uid的精确匹配，一次用于username的模糊匹配
        with con.cursor() as cursor:
            cursor.execute(sql, (search, '%' + search + '%', start, page_size))
            data = cursor.fetchall()

            # 返回结果
        return {
            'status': 1,
            'message': '查询成功',
            'data': data,
            'total_pages': total_pages
        }

    except Exception as e:
        # 处理异常
        return {
            'status': -1,
            'message': f'查询出错: {e}',
            'data': [],
            'total_pages': 0
        }

# 查询快递员用户
def putong(con, page=1, search=None):
    page_size = 4

    try:
        # 初始化搜索条件
        search_conditions = []
        if search:
            search_conditions.append("(uid = %s OR username LIKE %s)")

            # 构造完整的SQL查询语句
        where_clause = "WHERE kuaidi = 2"
        if search_conditions:
            where_clause += " AND " + " AND ".join(search_conditions)

            # 替换%s为实际参数
        params = [2]  # 初始参数为kuaidi的值
        if search:
            params.extend([search, '%' + search + '%'])  # 添加search和模糊匹配的参数

        # 计算总行数
        with con.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM usr {where_clause}", params)
            total_count = cursor.fetchone()[0]

            if total_count == 0:
                return {'status': 0, 'message': '没有找到匹配的快递员', 'data': [], 'total_pages': 0}

                # 计算总页数
            total_pages = -(-total_count // page_size)

            # 确保页数是有效的
            if page < 1:
                page = 1
            elif page > total_pages:
                page = total_pages

                # 计算起始索引
            start = (page - 1) * page_size

            # 执行查询
            sql = f"SELECT * FROM usr {where_clause} LIMIT %s, %s"
            params.extend([start, page_size])  # 添加分页参数

            with con.cursor() as cursor:
                cursor.execute(sql, params)
                results = cursor.fetchall()

                # 将结果转换为字典列表（假设我们知道列名）
                column_names = [i[0] for i in cursor.description]
                data = [dict(zip(column_names, row)) for row in results]

                # 返回结果
            return {
                'status': 1,
                'message': '查询成功',
                'data': data,
                'total_pages': total_pages
            }

    except Exception as e:
        # 处理异常
        return {
            'status': -1,
            'message': f'查询出错: {e}',
            'data': [],
            'total_pages': 0
        }

# 查询快递员的订单
def paisong(con, uid, text, page=1):
    page_size = 4

    # 构造SQL查询语句，使用参数化查询来防止SQL注入
    sql_count = "SELECT COUNT(*) FROM send WHERE 物流状态 > 0 AND 物流状态 < 5 AND 快递员uid = %s AND 订单号 LIKE %s"
    sql_select = "SELECT * FROM send WHERE 物流状态 > 0 AND 物流状态 < 5 AND 快递员uid = %s AND 订单号 LIKE %s LIMIT %s, %s"

    try:
        with con.cursor() as cursor:
            # 查询总数
            cursor.execute(sql_count, (uid, "%"+text+"%",))
            total_count = cursor.fetchone()[0]
            if total_count == 0:
                return {'status': 0, 'message': '你目前没有快递订单', 'data': [], 'total_pages': 0}

            # 计算总页数
            total_pages = (total_count + page_size - 1) // page_size

            # 确保页码在有效范围内
            page = max(1, min(page, total_pages))

            # 计算起始位置
            start = (page - 1) * page_size

            # 执行查询
            cursor.execute(sql_select, (uid, "%"+text+"%", start, page_size))
            data = cursor.fetchall()


            # 返回结果和总页数
            return {
                'status': 1,
                'message': '查询成功',
                'data': data,
                'total_pages': total_pages
            }

    except pymysql.MySQLError as e:
        # 处理异常
        return {
            'status': -1,
            'message': f'数据库错误: {e}',
            'data': [],
            'error': str(e)
        }


# 查询普通用户
def searchyonghulike(con, yonghu, page=1):
    # 页大小是固定的，这里我们设置为4
    page_size = 4
    # 确保页码是正整数，并至少为1
    page_number = max(1, page)

    # 初始的LIKE参数
    search_param_uid = f'%{yonghu}%'
    search_param_username = f'%{yonghu}%'

    # 计算总记录数
    total_count_sql = "SELECT COUNT(*) AS total FROM usr WHERE kuaidi IN (0, 1) AND (uid = %s OR username LIKE %s)"
    try:
        with con.cursor() as cursor:
            cursor.execute(total_count_sql, (search_param_uid, search_param_username))
            total_count = cursor.fetchone()[0]
            if total_count == 0:
                return {'status': 0, 'message': '没有找到匹配的用户', 'data': [], 'total_pages': 0}

            # 计算总页数
            total_pages = (total_count + page_size - 1) // page_size

            # 校验页码（如果需要的话）
            if page_number > total_pages:
                page_number = total_pages

                # 分页查询的SQL
            offset = (page_number - 1) * page_size
            sql = "SELECT * FROM usr WHERE kuaidi IN (0, 1) AND (uid = %s OR username LIKE %s) LIMIT %s OFFSET %s"

            # 执行分页查询
            with con.cursor() as cursor:
                cursor.execute(sql, (search_param_uid, search_param_username, page_size, offset))
                data = cursor.fetchall()

                if data:
                    result = {
                        'status': 1,
                        'message': '查询成功',
                        'data': data,
                        'total_pages': total_pages,
                    }

                else:
                    result = {
                        'status': 0,
                        'message': '没有找到匹配的用户',
                        'data': [],
                        'total_pages': total_pages,
                    }

    except pymysql.MySQLError as e:
        print(f"数据库查询出错: {e}")
        result = {
            'status': -1,
            'message': f'数据库错误: {e}',
            'data': [],
        }

    return result

# 查找网点管理员下的快递员
def find_kuaidi_paged(con, wanguid, kuaiuid_pattern, page=1):
    # 页大小是固定的，这里我们设置为4
    page_size = 4
    # 确保页码是正整数，并至少为1
    page_number = max(1, page)

    # 构造带通配符的搜索模式，比如 '%somepattern%'
    search_param_uid = f'%{kuaiuid_pattern}%'

    # 计算总记录数
    total_count_sql = "SELECT COUNT(*) AS total FROM usr WHERE wangdian = %s AND uid LIKE %s"
    try:
        with con.cursor() as cursor:
            # 获取总记录数
            cursor.execute(total_count_sql, (wanguid, search_param_uid))
            total_count = cursor.fetchone()[0]

            if total_count == 0:
                return {
                    'status': 0,
                    'message': '未找到匹配的快递员',
                    'data': [],
                    'total_pages': 0

                }

            # 计算总页数
            total_pages = (total_count + page_size - 1) // page_size

            # 校验页码
            if page_number > total_pages:
                page_number = total_pages

                # 分页查询的SQL
            offset = (page_number - 1) * page_size
            sql = "SELECT * FROM usr WHERE wangdian = %s AND uid LIKE %s LIMIT %s OFFSET %s"

            # 执行分页查询
            with con.cursor() as cursor:
                cursor.execute(sql, (wanguid, search_param_uid, page_size, offset))
                results = cursor.fetchall()

            if results:
                return {
                    'status': 1,
                    'message': '查询成功',
                    'data': results,
                    'total_pages': total_pages
                }
            else:
                return {
                    'status': 0,
                    'message': '未找到匹配的快递员',
                    'data': [],
                    'total_pages': total_pages
                }

    except pymysql.MySQLError as e:
        return {
            'status': -1,
            'message': f'数据库查询出错: {e}',
            'data': [],
            'total_pages': 0
        }
    except Exception as e:
        return {
            'status': -1,
            'message': f'查询出错: {e}',
            'data': [],
            'total_pages': 0,
        }


# 查找快递待审批
def find_check_kuaidi(con, text, page=1):
    page_size = 4
    try:
        # 计算总页数
        with con.cursor() as cursor:
            cursor.execute(
                f"SELECT COUNT(*) FROM usr WHERE kuaidi = 1 and (uid = %s or username like %s)",
                ("%" + text + "%", "%" + text + "%",))
            total_count = cursor.fetchone()[0]
            if total_count == 0:
                return {'status': 0, 'message': '未查询到待审核的快递员', 'data': [], 'total_pages': 0}
            total_pages = -(-total_count // page_size)  # 相当于math.ceil(total_count / page_size)
        # 确保页数是有效的
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages
            # 执行查询
        start = (page - 1) * page_size
        sql = "SELECT * FROM usr WHERE kuaidi = 1 and (uid = %s or username like %s) LIMIT %s, %s"
        with con.cursor() as cursor:
            cursor.execute(sql, ("%" + text + "%", "%" + text + "%", start, page_size))
            data = cursor.fetchall()
            result = {'status': 1, 'message': '查询成功', 'data': data, 'total_pages': total_pages}
    except Error as e:
        # 处理数据库错误
        result = {'status': -1, 'message': f'数据库错误: {e}', 'data': [], 'total_pages': 0}
    except Exception as e:
        # 处理其他类型的错误
        result = {'status': -1, 'message': f'未知错误: {e}', 'data': [], 'total_pages': 0}
        # 返回结果
    return result

# 查找网点管理员待审批
def find_check_wangdian(con, text, page=1):
    page_size = 4
    try:
        # 计算总页数
        with con.cursor() as cursor:
            cursor.execute(
                f"SELECT COUNT(*) FROM usr WHERE (kuaidi = 3 or kuaidi = 4) and (uid = %s or username like %s)",
                ("%" + text + "%", "%" + text + "%",))
            total_count = cursor.fetchone()[0]
            if total_count == 0:
                return {'status': 0, 'message': '未查询到待审核的网点管理员', 'data': [], 'total_pages': 0}
            total_pages = -(-total_count // page_size)  # 相当于math.ceil(total_count / page_size)
        # 确保页数是有效的
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages
            # 执行查询
        start = (page - 1) * page_size
        sql = "SELECT * FROM usr WHERE (kuaidi = 3 or kuaidi = 4) and (uid = %s or username like %s) LIMIT %s, %s"
        with con.cursor() as cursor:
            cursor.execute(sql, ("%" + text + "%", "%" + text + "%", start, page_size))
            data = cursor.fetchall()
            result = {'status': 1, 'message': '查询成功', 'data': data, 'total_pages': total_pages}
    except Error as e:
        # 处理数据库错误
        result = {'status': -1, 'message': f'数据库错误: {e}', 'data': [], 'total_pages': 0}
    except Exception as e:
        # 处理其他类型的错误
        result = {'status': -1, 'message': f'未知错误: {e}', 'data': [], 'total_pages': 0}
        # 返回结果
    return result


def searchwangdianlike(con, keyword, page_num=1):
    page_size = 4
    keyword_like = f'%{keyword}%'

    # 第一步：获取总记录数
    sql_count = """  
    SELECT COUNT(*) AS total_count FROM usr  
    WHERE (username LIKE %s OR uid = %s)  
    AND (kuaidi = 5)  
    """
    with con.cursor() as cursor:
        cursor.execute(sql_count, (keyword_like, keyword_like))
        result = cursor.fetchone()
        total_count = result[0] if result else 0

        if total_count == 0:
            return {'status': 0, 'message': '未查询到匹配的网点管理员', 'data': [], 'total_pages': 0}

        # 计算总页数
    total_pages = (total_count + page_size - 1) // page_size

    # 校验页码
    if page_num < 1:
        page_num = 1
    if page_num > total_pages:
        page_num = total_pages
    offset = (page_num - 1) * page_size

    try:
        # 第二步：执行分页查询
        sql = """  
        SELECT * FROM usr  
        WHERE (username LIKE %s OR uid = %s)  
        AND (kuaidi = 5)  
        LIMIT %s OFFSET %s  
        """
        with con.cursor() as cursor:
            params = (keyword_like, keyword_like, page_size, offset)
            cursor.execute(sql, params)
            data = cursor.fetchall()

            if data:
                result = {
                    'status': 1,
                    'message': '查询成功',
                    'data': data,
                    'total_pages': total_pages
                }
            else:
                result = {
                    'status': 0,
                    'message': '没有找到匹配的网点管理员',
                    'data': [],
                    'total_pages': total_pages
                }

    except pymysql.MySQLError as e:
        result = {
            'status': -1,
            'message': f'数据库错误: {e}',
            'data': [],
            'total_pages': 0
        }

    return result


def searchkuaidilike(con, kuaiyuan, page_num=1):
    page_size = 4
    kuaiyuan_like = f'%{kuaiyuan}%'

    # 第一步：获取总记录数
    sql_count = """  
    SELECT COUNT(*) AS total_count FROM usr  
    WHERE (uid = %s OR username LIKE %s)  
    AND (kuaidi = 2 OR kuaidi = 4)  
    """
    total_pages = 0

    try:
        with con.cursor() as cursor:
            cursor.execute(sql_count, (kuaiyuan_like, kuaiyuan_like))
            result = cursor.fetchone()
            if result:
                total_count = result[0]
                if total_count == 0:
                    return {'status': 0, 'message': '未查询到匹配的快递员', 'data': [], 'total_pages': 0}
                total_pages = (total_count + page_size - 1) // page_size  # 向上取整

            # 校验页码
            if page_num < 1:
                page_num = 1
            if page_num > total_pages:
                page_num = total_pages

            offset = (page_num - 1) * page_size

            # 第二步：执行分页查询
            sql = """  
            SELECT * FROM usr  
            WHERE (uid = %s OR username LIKE %s)  
            AND (kuaidi = 2 OR kuaidi = 4)  
            LIMIT %s OFFSET %s  
            """
            params = (kuaiyuan_like, kuaiyuan_like, page_size, offset)
            cursor.execute(sql, params)
            data = cursor.fetchall()

            if data:
                result = {
                    'status': 1,
                    'message': '查询成功',
                    'data': data,
                    'total_pages': total_pages
                }
            else:
                result = {
                    'status': 0,
                    'message': '没有找到匹配的用户',
                    'data': [],
                    'total_pages': total_pages
                }

    except pymysql.MySQLError as e:
        result = {
            'status': -1,
            'message': f'数据库错误: {e}',
            'data': [],
            'total_pages': 0  # 在错误情况下，页码总数设置为0
        }

    return result

# if __name__ == "__main__":
#     # 连接数据库
#     con = create_connection()
#
#     # 测试注册功能
#     zhan = "test_zha"
#     uid="0002"
#     tel = "17873952629"
#     mima="123456"
#     danhao="123124"
#     kuaidi="0001"
#     page=1
#     print(paisong(con, page, uid))
