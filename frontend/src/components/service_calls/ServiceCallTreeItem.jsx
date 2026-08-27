import { transformDiagnosticReportForServiceCall } from "../diagnostic_reports/DiagnosticReportTreeItem";

export function transformServiceCallForAtm( serviceCalls, atmId, diagnosticReports = [], atms = [], technicians = [] ) {
    return serviceCalls
        .filter((serviceCall) => serviceCall.atm_id === atmId)
        .map((serviceCall) => {
            const atm = atms.find((a) => a.id === serviceCall.atm_id);
            const technician = technicians.find((t) => t.id === serviceCall.technician_id);

            return {
                id: `serviceCall-${serviceCall.id}`,
                type: "ServiceCall",
                label: `${serviceCall.title} (ATM: ${serviceCall.atm_id}, Technician: ${serviceCall.technician_id})`,
                status: serviceCall.status,
                priority: serviceCall.priority,
                atm_branch_id: atm?.branch_id,
                technician_branch_id: technician?.branch_id,
                children: transformDiagnosticReportForServiceCall( diagnosticReports, serviceCall.id ),
            }
        });
}