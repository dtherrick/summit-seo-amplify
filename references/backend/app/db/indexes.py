"""Database indexes module.

This module defines database indexes for optimizing query performance.
It provides functions to create and manage indexes for all models.

The module includes:
- Index creation for all models
- Index management utilities
- Index validation

Example:
    ```python
    from app.db.indexes import create_indexes
    
    # Create all indexes
    await create_indexes(engine)
    ```
"""

from sqlalchemy import Index, text
from sqlalchemy.ext.asyncio import AsyncEngine
from loguru import logger

from app.models.user import User
from app.models.business import Business
from app.models.survey import SurveyResponse

async def create_indexes(engine: AsyncEngine) -> None:
    """Create all database indexes.
    
    Creates optimized indexes for:
    - User queries (email, created_at)
    - Business queries (name, created_at)
    - Survey queries (customer_id, created_at)
    
    Args:
        engine: SQLAlchemy async engine
        
    Example:
        ```python
        await create_indexes(engine)
        ```
    """
    async with engine.begin() as conn:
        # User indexes
        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_users_email 
            ON users (email);
            
            CREATE INDEX IF NOT EXISTS ix_users_created_at 
            ON users (created_at DESC);
        """))
        logger.info("Created user indexes")
        
        # Business indexes
        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_businesses_name 
            ON businesses (name);
            
            CREATE INDEX IF NOT EXISTS ix_businesses_created_at 
            ON businesses (created_at DESC);
            
            CREATE INDEX IF NOT EXISTS ix_businesses_user_id 
            ON businesses (user_id);
        """))
        logger.info("Created business indexes")
        
        # Survey indexes
        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_survey_responses_customer_id 
            ON survey_responses (customer_id);
            
            CREATE INDEX IF NOT EXISTS ix_survey_responses_created_at 
            ON survey_responses (created_at DESC);
            
            CREATE INDEX IF NOT EXISTS ix_survey_responses_business_id 
            ON survey_responses (business_id);
        """))
        logger.info("Created survey indexes")

async def validate_indexes(engine: AsyncEngine) -> dict:
    """Validate existing indexes and their usage statistics.
    
    Args:
        engine: SQLAlchemy async engine
        
    Returns:
        dict: Index statistics and health information
        
    Example:
        ```python
        stats = await validate_indexes(engine)
        print(f"Total indexes: {stats['total_indexes']}")
        ```
    """
    async with engine.begin() as conn:
        # Get index statistics
        result = await conn.execute(text("""
            SELECT
                schemaname,
                tablename,
                indexname,
                idx_scan,
                idx_tup_read,
                idx_tup_fetch
            FROM pg_stat_user_indexes
            WHERE schemaname = 'public';
        """))
        
        indexes = []
        for row in result:
            indexes.append({
                "schema": row.schemaname,
                "table": row.tablename,
                "index": row.indexname,
                "scans": row.idx_scan,
                "tuples_read": row.idx_tup_read,
                "tuples_fetched": row.idx_tup_fetch
            })
        
        return {
            "total_indexes": len(indexes),
            "indexes": indexes
        }

async def analyze_index_usage(engine: AsyncEngine) -> dict:
    """Analyze index usage and provide optimization recommendations.
    
    Args:
        engine: SQLAlchemy async engine
        
    Returns:
        dict: Index usage analysis and recommendations
        
    Example:
        ```python
        analysis = await analyze_index_usage(engine)
        print("Unused indexes:", analysis["unused_indexes"])
        ```
    """
    async with engine.begin() as conn:
        # Get unused indexes
        result = await conn.execute(text("""
            SELECT
                schemaname,
                tablename,
                indexname,
                idx_scan
            FROM pg_stat_user_indexes
            WHERE schemaname = 'public'
                AND idx_scan = 0
                AND indexname NOT LIKE '%_pkey';
        """))
        
        unused_indexes = []
        for row in result:
            unused_indexes.append({
                "schema": row.schemaname,
                "table": row.tablename,
                "index": row.indexname
            })
        
        # Get most used indexes
        result = await conn.execute(text("""
            SELECT
                schemaname,
                tablename,
                indexname,
                idx_scan
            FROM pg_stat_user_indexes
            WHERE schemaname = 'public'
            ORDER BY idx_scan DESC
            LIMIT 5;
        """))
        
        most_used = []
        for row in result:
            most_used.append({
                "schema": row.schemaname,
                "table": row.tablename,
                "index": row.indexname,
                "scans": row.idx_scan
            })
        
        return {
            "unused_indexes": unused_indexes,
            "most_used_indexes": most_used,
            "recommendations": [
                "Consider dropping unused indexes to improve write performance",
                "Monitor index usage patterns over time",
                "Consider partial indexes for specific query patterns"
            ]
        } 