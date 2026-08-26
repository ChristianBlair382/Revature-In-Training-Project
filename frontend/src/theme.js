import { createTheme } from "@mui/material";

const theme = createTheme({
    palette: {
        mode: 'light',
        primary: {
            main: '#304add'
        },
        secondary: {
            main: '#c96436'
        }
    },
    shape: {
        borderRadius: 4
    }
});

export default theme;