import { Container, Typography, Box } from "@mui/material";
import AppHeader from "./components/layout/AppHeader.jsx";
import ATMList from "./components/atms/ATMList.jsx";
import { mockATMs } from './mockData/atms.js';

function App() {
  return (
    <>
      <AppHeader />
      <Container maxWidth='lg' sx={{ mt: 4 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          Cash Cow Overview
        </Typography>
        <Box sx={{ mb: 4 }}>
          <ATMList atms={mockATMs} />
        </Box>
      </Container>
    </>
  )
}

export default App