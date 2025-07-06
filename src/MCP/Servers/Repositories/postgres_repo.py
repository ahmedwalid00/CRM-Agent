from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.MCP.Servers.Repositories.base_repo import MarketingRepository

class PostgresMarketingRepository(MarketingRepository):
    """PostgreSQL implementation for marketing data operations."""

    def __init__(self, db_session: Session):
        self.db = db_session

    async def create_campaign(self, name: str, type: str, description: str) -> str:
        """Inserts a new marketing campaign into the PostgreSQL database."""
        result = self.db.execute(
            text(
                """
                INSERT INTO marketing_campaigns (name, type, description)
                VALUES (:name, :type, :description)
                RETURNING id
                """
            ),
            {"name": name, "type": type, "description": description},
        )
        self.db.commit()
        campaign_id = result.fetchone()[0]
        return str(campaign_id)

    async def create_campaign_email_record(self, campaign_id: UUID, customer_id: int, subject: str, body: str) -> None:
        """Records a campaign email in the PostgreSQL database."""
        self.db.execute(
            text(
                """
                INSERT INTO campaign_emails (campaign_id, customer_id, subject, body)
                VALUES (:campaign_id, :customer_id, :subject, :body)
                """
            ),
            {
                "campaign_id": campaign_id,
                "customer_id": customer_id,
                "subject": subject,
                "body": body
            },
        )
        self.db.commit()