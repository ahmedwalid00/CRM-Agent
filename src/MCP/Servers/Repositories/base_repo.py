from abc import ABC, abstractmethod
from uuid import UUID

class MarketingRepository(ABC):
    """Abstract Base Class for a marketing data repository."""

    @abstractmethod
    async def create_campaign(self, name: str, type: str, description: str) -> str:
        """
        Creates a new marketing campaign.
        Should return the ID of the newly created campaign.
        """
        ...

    @abstractmethod
    async def create_campaign_email_record(self, campaign_id: UUID, customer_id: int, subject: str, body: str) -> None:
        """
        Records that a campaign email has been sent.
        """
        ...