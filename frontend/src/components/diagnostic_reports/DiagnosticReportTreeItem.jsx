export function transformDiagnosticReportForServiceCall( diagnostic_reports, serviceCallId ) {
    return diagnostic_reports
        .filter((diagnostic_report) => diagnostic_report.service_call_id === serviceCallId)
        .map((diagnostic_report) => ({
            id: `diagnostic_report-${diagnostic_report.id}`,
            type: "DiagnosticReport",
            label: `${diagnostic_report.file_url} - Notes: ${diagnostic_report.notes}; Created At: ${diagnostic_report.created_at}`,
        }));
}