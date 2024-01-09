import pydantic_settings
from typing import Literal

from utils.resource_handler import path


class Configure(pydantic_settings.BaseSettings):
    context: Literal['local', 'remote'] = 'remote'
    deviceName: str = 'Pixel_3a_API_34_extension_level_7_x86_64'
    timeout: float = 20.0
    appWaitActivity: str = "org.wikipedia.*"
    app: str = './app-alpha-universal-release.apk'
    server_url: str = 'http://127.0.0.1:4723'
    platformVersion: str = "13.0"


class Credentials(pydantic_settings.BaseSettings):
    login: str = 'dummy_value'
    password: str = 'dummy_value'


loaded_configuration = Configure(_env_file=path(f'.env.{Configure().context}'))
loaded_creds = Credentials(_env_file=path(f'.env.credentials'))
