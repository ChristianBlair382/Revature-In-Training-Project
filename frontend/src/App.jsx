import { useMemo } from "react";
import { Container, Typography, Box } from "@mui/material";
import { RichTreeView } from "@mui/x-tree-view";

import AppHeader from "./components/layout/AppHeader.jsx";
import CustomTreeItem from "./components/layout/TreeItemCustomLayout.jsx";
//import ATMList from "./components/atms/ATMList.jsx";
import { mockBranches } from "./mockData/branches.js";
import { mockATMs } from './mockData/atms.js';
import { mockTechnicians } from "./mockData/technicians.js";
import { transformBranches } from "./components/branches/BranchTreeItem.jsx";

export default function App() {
  const items = useMemo(
    () => transformBranches(mockBranches, mockATMs, mockTechnicians),
    []
  );

  return (
    <>
      <AppHeader />
      <Container maxWidth='lg' sx={{ mt: 4 }}>
        <Typography sx={{ color: 'black' }} variant="h5" component="h2" gutterBottom>
          Cash Cow Overview
        </Typography>
        <Box>
          <RichTreeView items={items} slots={{ item: CustomTreeItem }} />
        </Box>
      </Container>
    </>
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