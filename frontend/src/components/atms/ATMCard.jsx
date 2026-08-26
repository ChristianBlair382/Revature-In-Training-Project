import { Card, CardContent, Typography, Chip, Stack } from "@mui/material";

const LOW_CASH_THRESHOLD = 500;

// Component Structure: Card(CardContent(Typography, Typography, Stack(Chip, Chip)))

function ATMCard({atm}) {
    const isLowCash = atm.cash_lvl < LOW_CASH_THRESHOLD 
    
    return (
        <Card variant="outlined" sx={{ minWidth: 240 }}>
            <CardContent>
                <Typography variant="6" component="div">
                    {atm.serial_num}
                </Typography>
                <Typography color="text.secondary" gutterBottom>
                    {atm.model}
                </Typography>
                <Stack>
                    <Chip
                        label={`$${atm.cash_lvl}`}
                        color={isLowCash ? 'error' : 'success'}
                        size="small"
                    />
                    <Chip
                        label={atm.status}
                        variant="outlined"
                        size="small"
                    />
                </Stack>
            </CardContent>
        </Card>
    )
}

export default ATMCard