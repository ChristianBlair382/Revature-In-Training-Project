import { transformServiceCallForAtm } from "../service_calls/ServiceCallTreeItem";

const LOW_CASH_THRESHOLD = 500;

export function transformAtmsForBranch( atms, branchId, serviceCalls = [], diagnosticReports = [], technicians = [] ) {
    return atms
        .filter((atm) => atm.branch_id === branchId)
        .map((atm) => ({
            id: `atm-${atm.id}`,
            label: `${atm.serial_num} (${atm.model})`,
            type: 'Atm',
            status: atm.status,
            children: transformServiceCallForAtm( serviceCalls, atm.id, diagnosticReports, atms, technicians ),
        }));
}