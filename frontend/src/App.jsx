import { useCallback, useEffect, useMemo, useState } from "react";
import { Alert, Button, Card, CardContent, CircularProgress, Container, List, ListItem, ListItemText, Menu, MenuItem, Typography, Box, Snackbar } from "@mui/material";
import { RichTreeView } from "@mui/x-tree-view";

import AppHeader from "./components/layout/AppHeader.jsx";
import CustomTreeItem, { TreeFilters } from "./components/layout/TreeItemCustomLayout.jsx";
import AddEntreeDialog from "./components/admin/AddEntreeDialog.jsx";

//import ATMList from "./components/atms/ATMList.jsx";
import { apiClient } from "./api/client.js";
import { transformBranches } from "./components/branches/BranchTreeItem.jsx";
import LoginForm from './components/auth/LoginForm.jsx';
import { AuthProvider, useAuth } from './context/AuthContext.jsx';

// Requires proper authentication to view
function Dashboard() {
  const {user, logout} = useAuth()
  const [notification, setNotification] = useState(null)

  const [branches, setBranches] = useState([]);
  const [atms, setAtms] = useState([]);
  const [technicians, setTechnicians] = useState([]);
  const [serviceCalls, setServiceCalls] = useState([]);
  const [diagnosticReports, setDiagnosticReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [adminMenuAnchor, setAdminMenuAnchor] = useState(null);
  const [addEntreeDialogOpen, setAddEntreeDialogOpen] = useState(false);
  const [filters, setFilters] = useState({
    atmCashMax: '',
    branchSearch: '',
    technicianSearch: '',
    serviceCallStatus: '',
    serviceCallPriority: '',
    serviceCallColocation: '',
  });

  const loadFleetData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const branchesRes = await apiClient.get('/branches');
      const atmsRes = await apiClient.get('/atms');
      const techniciansRes = await apiClient.get('/technicians');
      const serviceCallsRes = await apiClient.get('/service_calls');
      const diagnosticReportsRes = await apiClient.get('/diagnostic_reports');

      setBranches(branchesRes.data);
      setAtms(atmsRes.data);
      setTechnicians(techniciansRes.data);
      setServiceCalls(serviceCallsRes.data);
      setDiagnosticReports(diagnosticReportsRes.data);
    } catch {
      setError('Failed to load fleet data.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadFleetData();
  }, [loadFleetData]);

  const filteredData = useMemo(() => {
    const branchSearch = filters.branchSearch.trim().toLowerCase();
    const technicianSearch = filters.technicianSearch.trim().toLowerCase();
    const cashMax = filters.atmCashMax === '' ? null : Number(filters.atmCashMax);

    return {
      branches: branches.filter((branch) =>
        !branchSearch || `${branch.name} ${branch.location_region}`.toLowerCase().includes(branchSearch)
      ),
      atms: atms.filter((atm) => cashMax === null || Number(atm.cash_lvl) <= cashMax),
      technicians: technicians.filter((technician) =>
        !technicianSearch || `${technician.name} ${technician.branch_id}`.toLowerCase().includes(technicianSearch)
      ),
      serviceCalls: serviceCalls.filter((serviceCall) =>
        (!filters.serviceCallStatus || serviceCall.status === filters.serviceCallStatus) &&
        (!filters.serviceCallPriority || serviceCall.priority === filters.serviceCallPriority) &&
        (!filters.serviceCallColocation || (() => {
          const atm = atms.find((candidate) => candidate.id === serviceCall.atm_id);
          const technician = technicians.find((candidate) => candidate.id === serviceCall.technician_id);
          const hasDiscrepancy = atm?.branch_id !== undefined &&
            technician?.branch_id !== undefined &&
            atm.branch_id !== technician.branch_id;

          return filters.serviceCallColocation === 'discrepancy'
            ? hasDiscrepancy
            : !hasDiscrepancy;
        })())
      ),
    };
  }, [branches, atms, technicians, serviceCalls, filters]);

  const items = useMemo(
    () => transformBranches(
      filteredData.branches,
      filteredData.atms,
      filteredData.technicians,
      filteredData.serviceCalls,
      diagnosticReports
    ),
    [filteredData, diagnosticReports]
  );
  const atmModelMetrics = useMemo(() => {
    const metricsByModel = new Map();

    atms.forEach((atm) => {
      if (!atm.model) return;

      const modelMetrics = metricsByModel.get(atm.model) || { completed: 0, failed: 0 };
      serviceCalls
        .filter((serviceCall) => serviceCall.atm_id === atm.id)
        .forEach((serviceCall) => {
          if (serviceCall.status === 'Completed') modelMetrics.completed += 1;
          if (serviceCall.status === 'Failed') modelMetrics.failed += 1;
        });
      metricsByModel.set(atm.model, modelMetrics);
    });

    return [...metricsByModel.entries()]
      .sort(([firstModel], [secondModel]) => firstModel.localeCompare(secondModel))
      .map(([model, metrics]) => {
        const terminalCalls = metrics.completed + metrics.failed;
        const completionPercentage = terminalCalls === 0
          ? 0
          : Math.round((metrics.completed / terminalCalls) * 100);

        return { model, ...metrics, completionPercentage };
      });
  }, [atms, serviceCalls]);
  const maintenanceFlaggedBranches = useMemo(() => branches
    .map((branch) => {
      const assignedAtms = atms.filter((atm) => atm.branch_id === branch.id);
      const maintenanceAtms = assignedAtms.filter((atm) => atm.status === 'Maintenance');

      return {
        name: branch.name,
        maintenancePercentage: assignedAtms.length === 0
          ? 0
          : (maintenanceAtms.length / assignedAtms.length) * 100,
      };
    })
    .filter((branch) => branch.maintenancePercentage >= 30), [branches, atms]);
  const supervisorMetrics = useMemo(() => branches
    .map((branch) => {
      const activeTechnicianIds = new Set(
        technicians
          .filter((technician) => technician.branch_id === branch.id)
          .filter((technician) => serviceCalls.some((serviceCall) =>
            serviceCall.technician_id === technician.id && serviceCall.status === 'In-Progress'
          ))
          .map((technician) => technician.id)
      );

      return {
        branchName: branch.name,
        supervisorId: branch.supervisor_id,
        activeTechnicianCount: activeTechnicianIds.size,
      };
    })
    .filter((branch) => branch.activeTechnicianCount > 0), [branches, technicians, serviceCalls]);
  const isOperationsAdmin = user?.role === 'Operations_Admin' || user?.role === 'OPERATIONS_ADMIN';
  const isFieldTechnician = user?.role === 'Field_Technician' || user?.role === 'FIELD_TECHNICIAN';

  return (
    <>
      <AppHeader username={user?.sub} role={user?.role} onLogout={logout} />
      <Container>
        <Box>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography sx={{color: 'black'}} variant="h5" component="h2" gutterBottom>
                Fleet Statistics
              </Typography>
              <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(3, 1fr)' }}>
                {/* Model Reliability Metrics */}
                <Card variant="outlined">
                  <CardContent>
                    <Typography color="text.secondary">Reliability Metrics</Typography>
                    <List dense>
                      {atmModelMetrics.map(({ model, completed, failed, completionPercentage }) => (
                        <ListItem key={model} disablePadding>
                          <ListItemText
                            primary={model}
                            secondary={`${completed}:${failed} (${completionPercentage}% completed)`}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
                {/* Maintenance Flagged Branches */}
                <Card variant="outlined">
                  <CardContent>
                    <Typography color="text.secondary">Maintenance Flagged Branches</Typography>
                    {maintenanceFlaggedBranches.length > 0 ? (
                      <List dense>
                        {maintenanceFlaggedBranches.map((branch) => (
                          <ListItem key={branch.name} disablePadding>
                            <ListItemText
                              primary={branch.name}
                              secondary={`${Math.round(branch.maintenancePercentage)}% of assigned ATMs`}
                            />
                          </ListItem>
                        ))}
                      </List>
                    ) : (
                      <Typography sx={{ mt: 2 }}>No branches meet this criteria.</Typography>
                    )}
                  </CardContent>
                </Card>

                <Card variant="outlined">
                  <CardContent>
                    <Typography color="text.secondary">Active Technicians by Supervisor</Typography>
                    {supervisorMetrics.length > 0 ? (
                      <List dense>
                        {supervisorMetrics.map(({ branchName, supervisorId, activeTechnicianCount }) => (
                          <ListItem key={`${branchName}-${supervisorId}`} disablePadding>
                            <ListItemText
                              primary={`${branchName} (Supervisor ID: ${supervisorId})`}
                              secondary={`${activeTechnicianCount} technician${activeTechnicianCount === 1 ? '' : 's'} with "In-Progress" calls`}
                            />
                          </ListItem>
                        ))}
                      </List>
                    ) : (
                      <Typography sx={{ mt: 2 }}>No supervisor IDs meet this criteria.</Typography>
                    )}
                  </CardContent>
                </Card>

              </Box>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Typography sx={{color: 'black'}} variant="h5" component="h2">Fleet Overview</Typography>
          {isOperationsAdmin && (
            <>
              <Button
                variant="contained"
                onClick={(event) => setAdminMenuAnchor(event.currentTarget)}
                aria-controls={adminMenuAnchor ? 'admin-actions-menu' : undefined}
                aria-haspopup="true"
                aria-expanded={adminMenuAnchor ? 'true' : undefined}
              >
                Admin Actions
              </Button>
              <Menu
                id="admin-actions-menu"
                anchorEl={adminMenuAnchor}
                open={Boolean(adminMenuAnchor)}
                onClose={() => setAdminMenuAnchor(null)}
              >
                <MenuItem
                  onClick={() => {
                    setAdminMenuAnchor(null);
                    setAddEntreeDialogOpen(true);
                  }}
                >
                  Add Entree
                </MenuItem>
              </Menu>
            </>
          )}
        </Box>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        <TreeFilters
          filters={filters}
          onChange={(name, value) => setFilters((currentFilters) => ({ ...currentFilters, [name]: value }))}
        />
        <Box sx={{ mb: 4 }}>
          {loading ? (
            <CircularProgress />
          ) : (
            <RichTreeView items={items} slots={{ item: CustomTreeItem }} />
          )}
        </Box>
      </Container>

      {isOperationsAdmin && (
        <AddEntreeDialog
          open={addEntreeDialogOpen}
          onClose={() => setAddEntreeDialogOpen(false)}
          onSuccess={async () => {
            await loadFleetData();
            setNotification('Entree added successfully.');
          }}
        />
      )}

      <Snackbar open={Boolean(notification)} autoHideDuration={4000} onClose={() => setNotification(null)}>
        <Alert severity="success" onClose={() => setNotification(null)}>{notification}</Alert>
      </Snackbar>
    </>
  );
}

function AppContent() {
  const {isAuthenticated} = useAuth();
  return isAuthenticated ? <Dashboard /> : <LoginForm />;
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
    // <>
    //   <AppHeader />
    //   <Container maxWidth='lg' sx={{ mt: 4 }}>
    //     <Typography sx={{ color: 'black' }} variant="h5" component="h2" gutterBottom>
    //       Cash Cow Overview
    //     </Typography>
    //     <Box>
    //       <RichTreeView items={items} slots={{ item: CustomTreeItem }} />
    //     </Box>
    //   </Container>
    // </>
  );
}

/**
 * 
    <Typography sx={{color: 'black'}} variant="h5" component="h2" gutterBottom>
      LIVE ATMS
    </Typography>
    <Box sx={{ mb: 4 }}>
      <ATMList atms={mockATMs} />
    </Box>
 */