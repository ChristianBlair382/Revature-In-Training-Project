import { useState } from "react";
import { Alert, Box, Button, CircularProgress, Paper, TextField, Typography } from "@mui/material";
import { useAuth } from "../../context/AuthContext.jsx"

export default function LoginForm() {
    const {login} = useAuth();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [isLoggingIn, setIsLoggingIn] = useState(false);


    const handleSubmit = async (event) => {
        event.preventDefault()
        setError(null);
        setIsLoggingIn(true);
        try {
            await login(username, password);
        } catch {
            setError('Username or password invalid.')
        } finally {
            setIsLoggingIn(false);
        }
    }

    return (
        <Box sx={{display: 'flex', justifyContent: 'center', mt: 8}}>
            <Paper component="form" onSubmit={handleSubmit} variant="outlined" sx={{p: 4, width: 320}}>
                <Typography variant="h5" gutterBottom>CashCow Login</Typography>
                {error && 
                    <Alert severity="error" sx={{mb: 2}}>
                        {error}
                    </Alert>
                }
                {isLoggingIn && (
                    <Alert
                        severity="info"
                        icon={<CircularProgress size={20} />}
                        sx={{mb: 2}}
                    >
                        Logging in...
                    </Alert>
                )}
                <TextField
                    label="Username"
                    fullWidth
                    margin="normal"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                />
                <TextField
                    label="Password"
                    type="password"
                    fullWidth
                    margin="normal"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                />
                <Button
                    type="submit"
                    variant="contained"
                    fullWidth
                    sx={{ mt: 2 }}
                    disabled={isLoggingIn}
                >
                    {isLoggingIn ? 'Logging In...' : 'Log In'}
                </Button>
            </Paper>
        </Box>
    )
}