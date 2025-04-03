from datetime import datetime, timedelta
import uuid
from fastapi import HTTPException
from sqlalchemy import text
from src.database.dals import DAL


class TemporaryLinkDAL(DAL):

    async def create_or_update(self, dashboard_id: uuid.UUID):

        new_secret = uuid.uuid4()
        new_available_until = datetime.now() + timedelta(days=1)

        query = text(
            """
            INSERT INTO temporary_link (id, secret_link, available_until)
            VALUES (:id, :secret_link, :available_until)
            ON CONFLICT (id) DO UPDATE
            SET secret_link = EXCLUDED.secret_link,
                available_until = EXCLUDED.available_until
            RETURNING id, secret_link, available_until;
        """
        )
        params = {
            "id": dashboard_id,
            "secret_link": new_secret,
            "available_until": new_available_until,
        }
        result = await self.db_session.execute(query, params)
        row = result.fetchone()
        result = dict(row._mapping)
        await self.db_session.commit()
        return result

    async def get(self, secret_link: uuid.UUID):
        query = text(
            """
            SELECT id, available_until
            FROM temporary_link
            WHERE secret_link = :secret_link
              AND available_until > current_timestamp
            """
        )
        params = {"secret_link": secret_link}
        result = await self.db_session.execute(query, params)

        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Secret link not found")
        result = dict(row._mapping)
        return result
