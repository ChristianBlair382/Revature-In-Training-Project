import { transformAtmsForBranch } from "../atms/ATMTreeItem"
import { transformTechniciansForBranch } from "../technicians/TechnicianTreeItem"

export function transformBranches(branches, atms, technicians, serviceCalls = [], diagnosticReports = []) {
  return branches.map((branch) => ({
    id: `branch-${branch.id}`,
    type: "Branch",
    label: `${branch.name} - ${branch.location_region}`,
    children: [
      ...transformAtmsForBranch( atms, branch.id, serviceCalls, diagnosticReports, technicians ),
      ...transformTechniciansForBranch( technicians, branch.id),
    ],
  }))
}