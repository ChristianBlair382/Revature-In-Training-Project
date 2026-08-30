# Run with: python -m scripts.verify_diagnostics
# From: backend/ with venv active

import asyncio
import boto3
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.orm_models import Diagnostic_Report

BUCKET_NAME = "cashcow-diagnostics-cb2478"
DIAGNOSTICS_PREFIX = "diagnostics/"

def extract_s3_key(file_url: str) -> str:
    without_scheme = file_url.removeprefix("s3://")
    _, _, key = without_scheme.partition("/") # first _ = bucket name, second _ = / after bucket name, key is the remaining string.
    return key

def list_s3_keys(bucket_name: str, prefix: str) -> set[str]:
    s3_client = boto3.client("s3")
    paginator = s3_client.get_paginator("list_objects_v2")

    keys: set[str] = set()
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get("Contents", []):
            keys.add(obj["Key"])
    return keys

async def fetch_diagnostic_reports() -> list[Diagnostic_Report]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Diagnostic_Report))
        return list(result.scalars().all())
    
async def main() -> None:
    s3_keys = list_s3_keys(BUCKET_NAME, DIAGNOSTICS_PREFIX)
    reports = await fetch_diagnostic_reports()

    healthy: list[Diagnostic_Report] = []
    broken: list[Diagnostic_Report] = []
    referenced_keys: set[str] = set()

    for report in reports:
        key = extract_s3_key(report.file_url)
        referenced_keys.add(key)
        if key in s3_keys:
            healthy.append(report)
        else:
            broken.append(report)

    orphaned_keys = s3_keys - referenced_keys
    
    print("\n== Healthy (database row + matching s3 file) ==")
    if not healthy:
        print(" None found. ")
    else:
        for report in healthy:
            print(f"DiagnosticReport {report.id}: {report.file_url}")

    print("== Broken (database row, no matching s3 file) ==")
    if not broken:
        print(" None found. ")
    else:
        for report in broken:
            print(f"DiagnosticReport {report.id}: {report.file_url}")

    print("== Orphaned ( s3 file with no matching database row ) ==")
    if not orphaned_keys:
        print(" None found. ")
    else:
        for key in orphaned_keys:
            print(f"s3://{BUCKET_NAME}/{key}")

if __name__ == "__main__":
    asyncio.run(main())