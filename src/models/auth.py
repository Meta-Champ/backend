from pydantic import BaseModel, Field


class AuthLogin(BaseModel):
    username: str = Field(..., examples=['admin'], description='Юзернейм пользователя')
    password: str = Field(..., examples=['password'], description='Пароль пользователя')


class AuthTokens(BaseModel):
    access_token: str = Field(
        ...,
        examples=['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJkZTJkODEwMC1hNjFmLTQwZDUtYWQ3Zi03ZjYyOGQ1ZDA3MWEiLCJzdWIiOiJsZWdlaGQwIiwiaWF0IjoxNzE5OTk4NTEwLCJleHAiOjE3MjA2MDMzMTAsInR5cCI6IkJlYXJlciIsInRva2VuX3R5cGUiOiJhY2Nlc3MifQ.-Y24u6ZOQhw3pJ1RW_XCukScqyh7jZOy_wzagKozXW'],
        description='Токен для взаимодействия c API'
    )

    refresh_token: str = Field(
        ...,
        examples=['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJkZTJkODEwMC1hNjFmLTQwZDUtYWQ3Zi03ZjYyOGQ1ZDA3MWEiLCJzdWIiOiJsZWdlaGQwIiwiaWF0IjoxNzE5OTk4NTEwLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMjU5MDUxMH0.nlvvsZvBn5KM5Qf2Kp4yONgwu9kr_fSyPwuuYQyOFb8'],
        description='Токен для обновления access_token'
    )
