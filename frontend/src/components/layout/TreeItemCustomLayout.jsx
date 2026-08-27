import { Box, Typography, Chip } from "@mui/material";
import { TreeItem } from "@mui/x-tree-view/TreeItem";
import { useTreeItemModel } from "@mui/x-tree-view/hooks";

export default function CustomTreeItem(props) {
  const item = useTreeItemModel(props.itemId);
  const ATM_STATUS_COLOR = {
    Operational: 'success',
    Low_Cash: 'warning',
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
          <Typography variant="body2">{item?.type}</Typography>
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
                    label={item.status}
                    color={SERVICE_CALL_STATUS_COLOR[item.status] ?? 'default'}
                />
                <Chip 
                    size="small"
                    label={item.priority}
                    color={SERVICE_CALL_PRIORITY_COLOR[item.priority] ?? 'default'}
                />
            </>
          )}
        </Box>
      }
    />
  );
}