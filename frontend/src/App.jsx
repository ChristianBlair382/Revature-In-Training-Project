import { useEffect, useMemo, useState } from "react";
import { Alert, CircularProgress, Container, Typography, Box } from "@mui/material";
import { RichTreeView } from "@mui/x-tree-view";

import AppHeader from "./components/layout/AppHeader.jsx";
import CustomTreeItem from "./components/layout/TreeItemCustomLayout.jsx";

//import ATMList from "./components/atms/ATMList.jsx";
import { apiClient } from "./api/client.js";
import { transformBranches } from "./components/branches/BranchTreeItem.jsx";
import LoginForm from './components/auth/LoginForm.jsx';
import { AuthProvider, useAuth } from './context/AuthContext.jsx';

// Requires proper authentication to view
function Dashboard() {
  const {user, logout} = useAuth()

  const [branches, setBranches] = useState([]);
  const [atms, setAtms] = useState([]);
  const [technicians, setTechnicians] = useState([]);
  const [serviceCalls, setServiceCalls] = useState([]);
  const [diagnosticReports, setDiagnosticReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function loadFleetData() {
      setLoading(true);
      setError(null);
      try {
        const branchesRes = await apiClient.get('/branches');
        const atmsRes = await apiClient.get('/atms');
        const techniciansRes = await apiClient.get('/technicians');
        const serviceCallsRes = await apiClient.get('/service_calls');
        const diagnosticReportsRes = await apiClient.get('/diagnostic_reports');

        if (!isMounted) return;

        setBranches(branchesRes.data);
        setAtms(atmsRes.data);
        setTechnicians(techniciansRes.data);
        setServiceCalls(serviceCallsRes.data);
        setDiagnosticReports(diagnosticReportsRes.data);
      } catch {
        if (isMounted) setError('Failed to load fleet data.');
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    loadFleetData();

    return () => {
      isMounted = false;
    };
  }, []);

  const items = useMemo(
    () => transformBranches(branches, atms, technicians, serviceCalls, diagnosticReports),
    [branches, atms, technicians, serviceCalls, diagnosticReports]
  );

  return (
    <>
      <AppHeader username={user?.sub} role={user?.role} onLogout={logout} />
      <Container>
        <Typography sx={{color: 'black'}} variant="h5" component="h2" gutterBottom>Fleet Overview</Typography>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        <Box sx={{ mb: 4 }}>
          {loading ? (
            <CircularProgress />
          ) : (
            <RichTreeView items={items} slots={{ item: CustomTreeItem }} />
          )}
        </Box>
      </Container>
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