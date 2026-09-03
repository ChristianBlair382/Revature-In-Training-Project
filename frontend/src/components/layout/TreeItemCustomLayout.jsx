import { Box, Chip, FormControl, InputLabel, MenuItem, Select, TextField, Typography } from "@mui/material";
import { TreeItem } from "@mui/x-tree-view/TreeItem";
import { useTreeItemModel } from "@mui/x-tree-view/hooks";

export function TreeFilters({ filters, onChange }) {
  return (
    <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', mb: 3 }}>
      <TextField
        label="ATM Cash LeveL < "
        type="number"
        value={filters.atmCashMax}
        onChange={(event) => onChange('atmCashMax', event.target.value)}
        slotProps={{ htmlInput: { min: 0 } }}
      />
      <TextField
        label="Branch Name/Region"
        value={filters.branchSearch}
        onChange={(event) => onChange('branchSearch', event.target.value)}
      />
      <TextField
        label="Technician Name/Branch ID"
        value={filters.technicianSearch}
        onChange={(event) => onChange('technicianSearch', event.target.value)}
      />
      <FormControl>
        <InputLabel id="service-call-status-filter-label">Service Call Status</InputLabel>
        <Select
          labelId="service-call-status-filter-label"
          label="Service call status"
          value={filters.serviceCallStatus}
          onChange={(event) => onChange('serviceCallStatus', event.target.value)}
        >
          <MenuItem value="">All statuses</MenuItem>
          {['Pending', 'In-Progress', 'Completed', 'Failed'].map((status) => (
            <MenuItem key={status} value={status}>{status}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl>
        <InputLabel id="service-call-priority-filter-label">Service Call Priority</InputLabel>
        <Select
          labelId="service-call-priority-filter-label"
          label="Service call priority"
          value={filters.serviceCallPriority}
          onChange={(event) => onChange('serviceCallPriority', event.target.value)}
        >
          <MenuItem value="">All priorities</MenuItem>
          {['Low', 'Medium', 'Critical'].map((priority) => (
            <MenuItem key={priority} value={priority}>{priority}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl>
        <InputLabel id="service-call-colocation-filter-label">Colocation Discrepency</InputLabel>
        <Select
          labelId="service-call-colocation-filter-label"
          label="Service call colocation"
          value={filters.serviceCallColocation}
          onChange={(event) => onChange('serviceCallColocation', event.target.value)}
        >
          <MenuItem value="">All service calls</MenuItem>
          <MenuItem value="discrepancy">Has Discrepancy</MenuItem>
          <MenuItem value="colocated">No Discrepancy</MenuItem>
        </Select>
      </FormControl>
    </Box>
  );
}

export default function CustomTreeItem(props) {
  const item = useTreeItemModel(props.itemId);
  const ATM_STATUS_COLOR = {
    Operational: 'success',
    Maintenance: 'info',
    Offline: 'error',
    };
  const SERVICE_CALL_STATUS_COLOR = {
    Pending: 'info',
    'In-Progress': 'warning',
    Completed: 'success',
    Failed: 'error',
    };
  const SERVICE_CALL_PRIORITY_COLOR = {
    Low: 'success',
    Medium: 'warning',
    Critical: 'error',
    };
  return (
    <TreeItem
      {...props}
      label={
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {/* <Typography variant="body2">{item?.type}</Typography> */}
          <Typography variant="body2">{item?.id}</Typography>
          <Typography variant="body2">{item?.label}</Typography>
          {item?.type === 'Atm' && (
            <Chip
                size="small"
                label={item.status}
                color={ATM_STATUS_COLOR[item.status] ?? 'default'}
            />
          )}
          {item?.type === 'ServiceCall' && (
            <>
                <Chip 
                    size="small"
                    label={`Status: ${item.status}`}
                    color={SERVICE_CALL_STATUS_COLOR[item.status] ?? 'default'}
                />
                <Chip 
                    size="small"
                    label={`Priority: ${item.priority}`}
                    color={SERVICE_CALL_PRIORITY_COLOR[item.priority] ?? 'default'}
                />
            </>
          )}
          {item?.type === 'ServiceCall' && 
            item?.atm_branch_id !== undefined &&
            item?.technician_branch_id !== undefined &&
            item.atm_branch_id !== item.technician_branch_id && (
            <>
                <Chip 
                    size="small"
                    label="Discrepency Detected!"
                    color={'error'}
                />
            </>
          )}
        </Box>
      }
    />
  );
}