import { Grid } from "@mui/material";
import ATMCard from "./ATMCard";

// Component Structure: Grid(foreach atm in atms(Grid(ATMCard)))

function ATMList({atms}) {
    return (
        <Grid container spacing={2}>
            {atms.map((atm)=>
                <Grid item="true" key={atm.id}>
                    <ATMCard atm={atm}/>
                </Grid>
            )}
        </Grid>
    )
}

export default ATMList