# Run with: python -m scripts.python_demo
# From: backend/ with venv active

from app.py_models import Branch, Technician, ATM, Service_Call, Diagnostic_Report, ATM_STATUS, SERVICE_CALL_PRIORITY

# Returns a list of atms that are below the specified threshold.
def find_low_cash_atms(atms: list[ATM], threshold: int = 1000) -> list[ATM]:
    return [
        atm for atm in atms
        if atm.status != ATM_STATUS.OFFLINE and ATM.is_low_cash(atm, threshold)
    ]

# Returns a list of service_calls that have assigned atms and assigned technicians whose branch IDs don't match.
def find_colocation_discrepencies(service_calls: list[Service_Call], atms: list[ATM], technicians: list[Technician]) -> list[Service_Call]:
    return [
        service_call for service_call in service_calls
        if ATM.find_by_id(service_call.atm_id) is not None and Technician.find_by_id(service_call.technician_id) is not None and
        ATM.find_by_id(service_call.atm_id).branch_id != Technician.find_by_id(service_call.technician_id).branch_id
    ]

def seed_demo_data() -> None:
    Branch(1, 'Citi Bank Corp - Southeast Branch', 'US-Southeast', 100, 101)
    Branch(2, 'Bank of America Corp - Northeast Branch', 'US-Northeast', 100, 101)

    Technician(201, 'Henry Cavel', 1)
    Technician(202, 'Simon Melvil', 1)
    Technician(203, 'Dan Williams', 2)

    ATM(1, 'DL-381920', 'Model XL 3.4', 783.02, 1, 'Operational')
    ATM(2, 'DL-334518', 'Model XL 3.4', 495.23, 2, 'Low_Cash')
    ATM(3, 'DL-318291', 'Model XL 3.4', 5928.10, 1, 'Operational')
    ATM(4, 'DL-393023', 'Model XL 3.4', 3129.45, 2, 'Maintenance')
    ATM(5, 'DL-381920', 'Model XL 3.4', 3810.78, 2, 'Operational')

    Service_Call(1, 'Account Access Denied', 1, 201, 'Low', 'In-Progress')
    Service_Call(2, 'Machine Out of Service Error', 4, 201, 'Low', 'Pending')
    Service_Call(3, 'Machine Jamming Problem', 2, 203, 'Medium', 'Completed')
    Service_Call(4, 'Security Concerns', 3, 202, 'Critical', 'In-Progress')

    Diagnostic_Report(1, 3, 'path', 'Issue fixed: replaced deposit funnel mechanism')
    Diagnostic_Report(2, 4, 'path', 'May stem from outdated systems')

def main() -> None:
    seed_demo_data()

    print("==FULL ATM REGISTRY==")
    for atm in ATM.registry:
        print(atm)

    print("\n==LOW BATTERY ALERT (< $1000)==")
    alerts = find_low_cash_atms(ATM.registry, threshold=1000)
    if not alerts:
        print("No atms found.")
    else:
        for atm in alerts:
            print(f" ALERT: {atm.serial_num} at ${atm.cash_lvl} (branch:{atm.branch_id})")

    print("\n==FACILITY ID DISCREPENCIES==")
    discrepencies = find_colocation_discrepencies(Service_Call.registry, ATM.registry, Technician.registry)
    if not discrepencies:
        print("No discrepencies found.")
    else:
        for service_call in discrepencies:
            print(f" DISCREPENCY: {service_call.title} - ID:{service_call.id}; ATM Facility ID - {ATM.find_by_id(service_call.atm_id).branch_id}; "
                  f" Technician Facility ID - {Technician.find_by_id(service_call.technician_id).branch_id}")
        
    
if __name__ == "__main__":
    main()