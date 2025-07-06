"""
This script defines and runs the 'marketing' MCP server.

It follows modern architecture principles:
1.  **Centralized Config**: Loads settings from a single source.
2.  **Repository Pattern**: Business logic is separated into a 'repository' class.
3.  **Manual Dependency Injection**: Inside each tool, it creates the necessary
    dependencies (like a database session and repository) for that specific request.
"""
import sys
from uuid import UUID
from contextlib import contextmanager

from mcp.server.fastmcp import FastMCP

from src.Helpers.config import get_settings
from src.Authentication.database import setup_database_engine
from src.MCP.Servers.Repositories.postgres_repo import PostgresMarketingRepository

# ----------------------------
# 1. INITIALIZATION ON STARTUP
# ----------------------------
print("Initializing Marketing MCP Server...")

# Load application settings from .env using our singleton
try:
    settings = get_settings()
except Exception as e:
    print(f"FATAL: Could not load settings. Error: {e}", file=sys.stderr)
    sys.exit(1)

# Set up the database engine and session factory. This happens only once when the script starts.
db_engine, SessionLocal = setup_database_engine(settings.SUPABASE_URI)

# Initialize the MCP server instance
mcp = FastMCP("marketing")


# -------------------------------------
# 2. DEPENDENCY PROVIDER (Manual DI)
# -------------------------------------

@contextmanager
def get_repository():
    """
    A context manager that handles the lifecycle of dependencies for a single tool call.
    - Creates a DB session.
    - Creates the repository with that session.
    - Yields the repository to the tool.
    - Ensures the DB session is closed, even if errors occur.
    """
    db_session = None
    try:
        db_session = SessionLocal()
        repo = PostgresMarketingRepository(db_session=db_session)
        yield repo
    finally:
        if db_session:
            db_session.close()


# ----------------------------
# 3. TOOL DEFINITIONS
# ----------------------------

@mcp.tool()
async def create_campaign(name: str, type: str, description: str) -> str:
    """Create a marketing campaign.
    
    Args:
        name: The name of the campaign.
        type: The type of the campaign. One of: loyalty, referral, re-engagement
        description: The description of the campaign.

    Returns:
        The ID of the created campaign.
    """
    print(f"Executing tool: create_campaign(name='{name}')")
    # Use our context manager to get a repository instance
    with get_repository() as repo:
        # Delegate all business logic to the repository method
        campaign_id = await repo.create_campaign(
            name=name, type=type, description=description
        )
        return campaign_id

@mcp.tool()
async def send_campaign_email(campaign_id: UUID, customer_id: int, subject: str, body: str) -> str:
    """Send a campaign email and record it in the database.
    
    Args:
        campaign_id: The ID of the campaign.
        customer_id: The ID of the customer.
        subject: The subject of the email.
        body: The body of the email.

    Returns:
        A confirmation that the email was sent.
    """
    print(f"Executing tool: send_campaign_email(campaign_id='{campaign_id}')")
    # Use our context manager again for this request
    with get_repository() as repo:
        # Delegate to the repository
        await repo.create_campaign_email_record(
            campaign_id=campaign_id,
            customer_id=customer_id,
            subject=subject,
            body=body,
        )
    return f"Successfully sent <{subject}> to customer <{customer_id}>!"


# ----------------------------
# 4. SCRIPT EXECUTION
# ----------------------------

if __name__ == "__main__":
    try:
        print("Marketing MCP Server is running and waiting for requests...")
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        # Cleanly dispose of the database connection pool when the server exits.
        if db_engine:
            db_engine.dispose()
            print("Database connection pool closed.")