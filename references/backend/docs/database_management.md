# Database Management Guide

## Overview

This document outlines the procedures for managing the database in our FastAPI application. We use PostgreSQL as our database and Alembic for database migrations.

## Key Principles

1. **Data Persistence**: The database is configured to persist data between sessions using Docker volumes.
2. **No Automatic Schema Changes**: The application never modifies the database schema automatically.
3. **Migration-Based Schema Management**: All schema changes must be done through Alembic migrations.
4. **Health Monitoring**: Database connectivity is verified on startup and for each request.

## Database Connection

The database connection is configured in `docker-compose.yml`:

```yaml
POSTGRES_USER: postgres
POSTGRES_PASSWORD: password
POSTGRES_DB: mydb
```

## Managing Database Migrations

### Creating a New Migration

1. Make changes to your SQLAlchemy models in the `app/models` directory
2. Generate a new migration:
   ```bash
   cd backend
   alembic revision --autogenerate -m "description of changes"
   ```
3. Review the generated migration in `alembic/versions/`
4. Apply the migration:
   ```bash
   alembic upgrade head
   ```

### Common Migration Commands

```bash
# View current migration state
alembic current

# View migration history
alembic history

# Upgrade to the latest migration
alembic upgrade head

# Upgrade by one migration
alembic upgrade +1

# Downgrade by one migration
alembic downgrade -1

# Downgrade all migrations
alembic downgrade base

# Generate a new migration
alembic revision --autogenerate -m "description"
```

## Backup and Restore

### Creating Database Backups

```bash
# From host machine
docker exec -t your_postgres_container pg_dump -U postgres mydb > backup.sql

# Or using docker-compose
docker-compose exec db pg_dump -U postgres mydb > backup.sql
```

### Restoring from Backup

```bash
# From host machine
cat backup.sql | docker exec -i your_postgres_container psql -U postgres -d mydb

# Or using docker-compose
cat backup.sql | docker-compose exec -i db psql -U postgres -d mydb
```

## Troubleshooting

### Common Issues

1. **Migration Conflicts**
   - Always review generated migrations before applying
   - If conflicts occur, downgrade to a stable version and recreate migration

2. **Connection Issues**
   - Check the health endpoint at `/health`
   - Verify database container is running: `docker-compose ps`
   - Check logs: `docker-compose logs db`

3. **Data Persistence Issues**
   - Verify volume configuration in `docker-compose.yml`
   - Check volume status: `docker volume ls`

### Health Checks

The application includes built-in health checks:
- `/health` endpoint verifies database connectivity
- Each request verifies database connection
- Failed health checks return HTTP 503

## Best Practices

1. **Always Backup Before Migrations**
   ```bash
   docker-compose exec db pg_dump -U postgres mydb > pre_migration_backup.sql
   ```

2. **Test Migrations in Development**
   - Never run untested migrations in production
   - Always have a rollback plan

3. **Monitor Database Size**
   ```bash
   docker-compose exec db psql -U postgres -d mydb -c "\l+"
   ```

4. **Regular Maintenance**
   - Monitor database logs
   - Check for slow queries
   - Regular backups
   - Periodic health checks

## Development Workflow

1. Create new model or modify existing one in `app/models/`
2. Generate migration
3. Review migration file
4. Test migration in development
5. Apply migration
6. Update API endpoints as needed
7. Test thoroughly
8. Commit changes with migration files

## Security Considerations

1. Never commit database credentials
2. Use environment variables for sensitive data
3. Regular security updates
4. Proper access control
5. Regular audit of database access

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/) 