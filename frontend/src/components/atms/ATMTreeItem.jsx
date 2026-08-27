import { mockServiceCalls } from "../../mockData/serviceCalls";
import { transformServiceCallForAtm } from "../service_calls/ServiceCallTreeItem";

const LOW_CASH_THRESHOLD = 500;

export function transformAtmsForBranch( atms, branchId ) {
    return atms
        .filter((atm) => atm.branch_id === branchId)
        .map((atm) => ({
            id: `atm-${atm.id}`,
            label: `${atm.serial_num} (${atm.model})`,
            type: 'Atm',
            status: atm.status,
            children: transformServiceCallForAtm( mockServiceCalls, atm.id ),
        }));
}