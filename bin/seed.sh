#!/usr/bin/env bash

TARGET = "{$:local}" # $1 is the first argument typed after the script name

# redirects the database to be seeded depending on the value of $1
if [ "$TARGET" == "local" ]; then
    # TODO: Please put your postgres login details here
    export DATABASE_URL = "postgresql+asyncpg://postgres:<password>@127.0.0.1:5432/cashcow_dev_2478"
    PSQL_HOST="127.0.0.1"
    PSQL_DB="cashcow_dev_2478"
elif [ "$TARGET" == "rds" ] then 
    # TODO: Please put your postgres login details here
    export DATABASE_URL = "postgresql+asyncpg://<user>:<password>@<your-rds-endpoint>:5432/cashcow"
    PSQL_HOST="<your-rds-endpoint>"
    PSQL_DB="cashcow"
else # Catches any TARGET that isn't either of the provided
    echo "Usage: bin/seed.sh [local|rds]"
    exit 1
fi

echo "Seeding target: $TARGET"
cd backend

# Step 1: Create tables
python -m scripts.create_tables
# Step 2: Populate tables
psql -h "$PSQL_HOST" -U postgres -d "$PSQL_DB" -f ../db/sql/seed.sql
# Step 3: Populate RBAC demo users
python -m scripts.seed_users

echo "Seed complete for $TARGET"