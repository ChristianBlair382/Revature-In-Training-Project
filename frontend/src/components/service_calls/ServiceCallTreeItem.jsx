import { mockDiagnosticReports } from "../../mockData/diagnosticReports";
import { transformDiagnosticReportForServiceCall } from "../diagnostic_reports/DiagnosticReportTreeItem";

export function transformServiceCallForAtm( serviceCalls, atmId ) {
    return serviceCalls
        .filter((serviceCall) => serviceCall.atm_id === atmId)
        .map((serviceCall) => ({
            id: `serviceCall-${serviceCall.id}`,
            type: "ServiceCall",
            label: `${serviceCall.title} - Priority: ${serviceCall.priority}, Status: ${serviceCall.status}`,
            status: serviceCall.status,
            priority: serviceCall.priority,
            children: transformDiagnosticReportForServiceCall( mockDiagnosticReports, serviceCall.id ),
        }));
}