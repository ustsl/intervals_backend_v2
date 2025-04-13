import uuid
import os

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from src.database.models.user_model.tables import UserModel, get_user_db
from src.settings import (
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST_USER,
    EMAIL_PORT,
    EMAIL_USE_SSL,
    EMAIL_USE_TLS,
    SECRET_AUTH_TOKEN,
)

SECRET = SECRET_AUTH_TOKEN


class UserManager(UUIDIDMixin, BaseUserManager[UserModel, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
        self, user: UserModel, request: Optional[Request] = None
    ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: UserModel, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        # Вызываем асинхронную функцию отправки письма для сброса пароля
        await self.send_reset_password_email(user, token)

    async def on_after_request_verify(
        self, user: UserModel, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def send_reset_password_email(self, user: UserModel, token: str):
        await self._send_email(user, token)

    async def _send_email(self, user: UserModel, token: str):
        subject = "INTERVALS. Сброс пароля"
        body = (
            f"Привет,\n\n"
            f"Был запрошен сброс пароля:\n\n"
            f"Перейдите по ссылке: https://intervals.ru/oauth/reset/{token}\n\n"
            f"Если вы не запрашивали сброс, то проигнорируйте это письмо\n\n"
            f"Желаем удачи!\n"
            f"INTERVALS"
        )

        msg = MIMEMultipart()
        msg["From"] = EMAIL_HOST_USER
        msg["To"] = user.email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            await aiosmtplib.send(
                msg,
                sender=EMAIL_HOST_USER,
                recipients=[user.email],
                hostname=EMAIL_HOST,
                port=EMAIL_PORT,
                username=EMAIL_HOST_USER,
                password=EMAIL_HOST_PASSWORD,
                start_tls=EMAIL_USE_TLS,
            )
            print(f"Password reset email sent to {user.email}")
        except Exception as e:
            print(f"Error sending password reset email to {user.email}: {e}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
