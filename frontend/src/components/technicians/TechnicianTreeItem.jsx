export function transformTechniciansForBranch( technicians, branchId ) {
    return technicians
        .filter((technician) => technician.branch_id === branchId)
        .map((technician) => ({
            id: `Technician-${technician.id}`,
            type: 'Technician',
            label: `${technician.name}; Deployed at Branch (${technician.branch_id})`,
        }));
}