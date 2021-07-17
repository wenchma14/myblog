class MyBlogError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __str__(self):
        return "%d: %s" % (self.code, self.message)

    def keys(self):
        return 'code', 'message'

    def __getitem__(self, item):
        return getattr(self, item)


NOError = MyBlogError(100000, '成功')
ServiceError = MyBlogError(100001, '系统错误，请稍后重试')
RecordNotFoundError = MyBlogError(100002, '没有发现记录')
SendCodeError = MyBlogError(100003, '发送验证码失败')
EmailError = MyBlogError(100004, '邮箱错误')
CodeError = MyBlogError(100005, '验证码不正确或过期')
PasswordError = MyBlogError(100006, '密码错误')
UserStatusError = MyBlogError(100007, '用户已被封禁')
TokenError = MyBlogError(100008, 'token认证失败')
ParamsError = MyBlogError(100009, '参数错误')
SendCodeFrequentlyError = MyBlogError(1000010, '发送验证码频繁，请稍候重试')
SendCodeTooFrequentlyError = MyBlogError(100011, '发送验证码频繁，请明天重试')
UserNoPermission = MyBlogError(100012, '用户没有权限')
