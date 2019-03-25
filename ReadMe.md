1. 状态码

        codes=[
            {"status_code":"10001","status_text":"注册成功"},
            {"status_code":"10002","status_text":"用户已经存在"},

            {"status_code":"10003","status_text":"登录成功"},
            {"status_code":"10004","status_text":"该用户不存在"},
            {"status_code":"10005","status_text":"密码错误"},
            {"status_code":"10006","status_text":"登录过期"},
            {"status_code":"10007","status_text":"未登录"},

            {"status_code":"10008","status_text":"未找到数据"},
            {"status_code":"10009","status_text":"找到数据"},


            {"status_code":"10010","status_text":"评论成功"},
            {"status_code":"10011","status_text":"评论失败"},

            {"status_code":"10012","status_text":"添加信息成功"},
            {"status_code":"10013","status_text":"添加信息失败"},

            {"status_code":"10020","status_text":"预约成功"},
            {"status_code":"10021","status_text":"预约失败"},

            {"status_code":"10030","status_text":"收藏成功"},
            {"status_code":"10031","status_text":"收藏失败"},

            {"status_code":"10040","status_text":"取消收藏成功"},
            {"status_code":"10041","status_text":"取消收藏失败"},


            {"status_code":"10011","status_text":"评论失败"},
            {"status_code":"10011","status_text":"评论失败"},

            {"status_code":"40004","status_text":"系统错误"},
            {"status_code":"40005","status_text":"数据格式不合法"},
            {"status_code":"40006","status_text":"请求方式错误"}
        ]

2.命名规范:

        命名:
            路由名---全小写--login,regist
            service层文件---add_User,
            dao层文件---addUser,
