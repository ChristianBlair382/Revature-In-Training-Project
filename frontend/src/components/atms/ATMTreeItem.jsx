import { transformServiceCallForAtm } from "../service_calls/ServiceCallTreeItem";

export function transformAtmsForBranch( atms, branchId, serviceCalls = [], diagnosticReports = [], technicians = [] ) {
    return atms
        .filter((atm) => atm.branch_id === branchId)
        .map((atm) => ({
            id: `ATM-${atm.id}`,
            label: `${atm.serial_num} (${atm.model}), $${atm.cash_lvl}`,
            type: 'Atm',
            status: atm.status,
            cash_lvl: atm.cash_lvl,
            children: transformServiceCallForAtm( serviceCalls, atm.id, diagnosticReports, atms, technicians ),
        }));
}