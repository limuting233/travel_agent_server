from pathlib import Path

from pydantic_settings import BaseSettings
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # 项目根目录


class Settings(BaseSettings):
    """
    配置类，用于存储应用程序的配置参数
    """
    # 项目配置
    PROJECT_NAME: str = "Travel Agent Server"  # 项目名称
    PROJECT_VERSION: str = "0.1.0"  # 项目版本号

    # OpenAI API 配置
    OPENAI_API_BASE: str  # OpenAI API 基础 URL
    OPENAI_API_KEY: str  # OpenAI API 密钥

    # Ollama API 配置
    OLLAMA_API_BASE: str  # Ollama API 基础 URL
    OLLAMA_API_KEY: str  # Ollama API 密钥

    # 高德地图 API 配置
    AMAP_API_BASE: str  # 高德地图 API 基础 URL
    AMAP_API_KEY: str  # 高德地图 API 密钥
    AMAP_MCP_BASE_URL: str  # 高德地图 MCP 接口基础 URL
    AMAP_MCP_TIMEOUT: int  # 高德地图 MCP 请求超时时间（秒）

    # 数据库配置
    DB_HOST: str  # 数据库主机地址
    DB_PORT: str  # 数据库端口号
    DB_USER: str  # 数据库用户名
    DB_PASSWORD: str  # 数据库密码
    DB_NAME: str  # 数据库名称
    DB_POOL_SIZE: int  # 数据库连接池大小
    DB_MAX_OVERFLOW: int  # 数据库最大连接数溢出值

    # 小红书 MCP 配置
    XHS_MCP_URL: str  # 小红书 MCP 接口 URL
    XHS_MCP_TIMEOUT: int  # 小红书 MCP 请求超时时间（秒）

    # 日志配置
    LOG_LEVEL: str = "INFO"  # 日志级别
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"  # 日志格式

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")  # 环境变量文件路径
        case_sensitive = True  # 环境变量名称大小写敏感
        env_file_encoding = "utf-8"  # 环境变量文件编码
        extra = "ignore"  # 忽略额外的环境变量


settings = Settings()
