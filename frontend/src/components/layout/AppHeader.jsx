import { AppBar, Toolbar, Typography, Box, Button } from "@mui/material";
import PrecisionManufacturingIcon from "@mui/icons-material/PrecisionManufacturing"

// Component Structure: AppBar(Toolbar(PrecisionManufacturingIcon, Typography))

function AppHeader({username, role, onLogout}) {
    return (
        <AppBar position="static">
            <Toolbar>
                <PrecisionManufacturingIcon sx={{mr: 2}} />
                <Typography variant="6" component="h1">
                    CashCow Branch Operations Command Center
                </Typography>
                {username && (
                    <Box>
                        <Typography>{username}({role})</Typography>
                        <Button color="inherit" onClick={onLogout}>Log Out</Button>
                    </Box>
                )}
            </Toolbar>
        </AppBar>
    )
}

export default AppHeader;