# Run with: python -m scripts.upload_diagnostic
# From: backend/ with venv active

import asyncio
import boto3

from app.database import AsyncSessionLocal
from app.orm_models import Diagnostic_Report

BUCKET_NAME = "cashcow-diagnostics-cb2478"
LOCAL_FILE_PATH = "scripts/dummy_diagnostics/sample_diagnostic.txt"
S3_KEY = "diagnostics/dl-381920.txt"

def upload_to_s3() -> str:
    s3_client= boto3.client("s3")
    s3_client.upload_file(LOCAL_FILE_PATH, BUCKET_NAME, S3_KEY)
    return f"s3://{BUCKET_NAME}/{S3_KEY}"

async def record_diagnostic_log(fileUrl: str) -> None:
    async with AsyncSessionLocal() as session:
        report = Diagnostic_Report(
            service_call_id = 3,
            file_url = fileUrl,
            notes="Uploaded via day8_upload_diagnostic script.",
        )

        session.add(report)
        await session.commit()
        await session.refresh(report)
        print(f"Created Diagnostic Report id={report.id}, file_url={report.file_url}")

async def main() -> None:
    file_url = upload_to_s3()
    print(f"Uploaded to {file_url}")
    await record_diagnostic_log(file_url)

if __name__ == "__main__":
    asyncio.run(main())