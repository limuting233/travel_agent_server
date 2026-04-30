from enum import Enum


class StatusInfo(Enum):
    """
    状态信息枚举类
    """
    # (http状态码, 业务状态码, 状态描述)
    SUCCESS = (200, 10200, "操作成功")

    # 全局系统类 (10xxx)
    BAD_REQUEST = (400, 10400, "参数校验失败")

    # 用户与权限类 (20xxx)
    LOGIN_EMPTY_CREDENTIALS = (200, 20001, "用户名和密码不能为空")
    LOGIN_INVALID_LENGTH = (200, 20002, "用户名或密码须为5-12位")
    LOGIN_INVALID_CREDENTIALS = (200, 20003, "用户名或密码错误")
    REGISTER_USERNAME_EXISTS = (200, 20004, "用户名已存在")
