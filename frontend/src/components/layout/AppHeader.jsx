import { AppBar, Toolbar, Typography } from "@mui/material";
import PrecisionManufacturingIcon from "@mui/icons-material/PrecisionManufacturing"

// Component Structure: AppBar(Toolbar(PrecisionManufacturingIcon, Typography))

function AppHeader() {
    return (
        <AppBar position="static">
            <Toolbar>
                <PrecisionManufacturingIcon sx={{mr: 2}} />
                <Typography variant="6" component="h1">
                    CashCow Branch Operations Command Center
                </Typography>
            </Toolbar>
        </AppBar>
    )
}

export default AppHeader;