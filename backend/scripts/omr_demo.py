# Run with: python -m scripts.omr_demo
# From: backend/ with venv active

import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.orm_models import ATM, ATM_STATUS, Service_Call, Technician

# business question 1
async def find_low_cash_atms(session, threshold: int = 1000) -> list["ATM"]:
    # Use "statement" objects to represent SQL queries in SQLAlchemy
    statement = (
        select(ATM)
        .options(selectinload(ATM.branch)) # statement object parameter; selectinload 
        .where(ATM.status != ATM_STATUS.OFFLINE, ATM.cash_lvl < threshold)
        .order_by(ATM.id)
    )
    result = await session.execute(statement)
    return list(result.scalars().all())

# business question 2
async def colocation_discrepencies(session) -> list["Service_Call"]:
    statement = (
        select(Service_Call)
        .join(ATM, ATM.id == Service_Call.atm_id)
        .join(Technician, Technician.id == Service_Call.technician_id)
        .where(ATM.branch_id != Technician.branch_id)
        .order_by(Service_Call.id)
    )
    result = await session.execute(statement)
    return list(result.scalars().all())

async def main() -> None:
    async with AsyncSessionLocal() as session:
        all_atms_stmt = select(ATM).options(selectinload(ATM.branch)).order_by(ATM.id)

        all_atms = await session.execute(all_atms_stmt)
        print("\n== FULL ATM REGISTRY (via ORM) ==")
        for atm in all_atms.scalars():
            print(f"{atm!r} -> branch: {atm.branch.name}")

        alerts = await find_low_cash_atms(session, threshold=1000)
        print("\n == LOW CASH ATMS (< $1000) ==")
        if not alerts:
            print("----------------------------")
            print("No atms below threshold.\n")
        else:
            for atm in alerts:
                print(f" ALERT: {atm.serial_num} at ${atm.cash_lvl} Branch: {atm.branch.name}")

        discrepencies = await colocation_discrepencies(session)
        print("\n == COLOCATION DISCREPENCIES (via ORM) ==")
        if not discrepencies:
            print("-----------------------------")
            print("No discrepencies detected.\n")
        else:
            for service_call in discrepencies:
                atm = await session.get(ATM, service_call.atm_id)
                technician = await session.get(Technician, service_call.technician_id)
                print(f" {service_call.id}: {service_call.title} - ATM Branch ID: {atm.branch_id} - Technician Branch ID: {technician.branch_id}")

if __name__ == "__main__":
    asyncio.run(main())