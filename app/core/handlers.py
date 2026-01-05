from fastapi import Request, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.enums import StatusInfo
from app.core.exceptions import BusinessException
from loguru import logger


def handler_request_validation_exception(request: Request, exception: RequestValidationError) -> JSONResponse:
    """
    请求参数校验异常处理器，用于处理FastAPI在请求参数校验过程中抛出的异常
    :param request: 请求实例
    :param exception: 请求参数校验异常实例
    :return: JSONResponse 包含错误信息的响应体
    """
    logger.error(f"[RequestValidationError处理器] 请求路径:{request.url.path}, 异常信息:{exception}")
    # logger.exception(exception)
    errors = exception.errors()
    error_messages = []
    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"][1:])  # 去掉 "body" 前缀
        msg = error["msg"]
        error_messages.append(f"{field}: {msg}")
    error_message = "; ".join(error_messages)
    return JSONResponse(
        status_code=StatusInfo.BAD_REQUEST.value[0],
        content={
            "code": StatusInfo.BAD_REQUEST.value[1],
            "message": "error",
            "error_message": error_message,
            "data": None
        }
    )


def handler_business_exception(request: Request, exception: BusinessException) -> JSONResponse:
    """
    业务异常处理器，用于处理业务逻辑中抛出的异常
    :param request: 请求实例
    :param exception: 业务异常实例
    :return: JSONResponse 包含错误信息的响应体
    """

    http_code = exception.http_code  # 从异常实例中获取HTTP状态码
    code = exception.code  # 从异常实例中获取业务状态码
    error_message = exception.error_message  # 从异常实例中获取错误消息

    logger.error(f"[BusinessException处理器] http状态码:{http_code}, 业务状态码:{code}, 错误消息:{error_message}")

    return JSONResponse(
        status_code=http_code,
        content={
            "code": code,
            "message": "error",
            "error_message": error_message,
            "data": None
        }
    )


def register_exception_handlers(app: FastAPI):
    """
    注册异常处理器
    :param app: FastAPI应用实例
    :return:
    """
    logger.info("正在注册异常处理器 ...")
    app.add_exception_handler(RequestValidationError, handler_request_validation_exception)
    app.add_exception_handler(BusinessException, handler_business_exception)
    logger.info("异常处理器注册完成")
