import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from "@mui/material";
import { useState } from "react";
import { apiClient } from "../../api/client.js";

const dataTables = [
  { value: "atms", label: "ATMs" },
  { value: "branches", label: "Branches" },
  { value: "technicians", label: "Technicians" },
  { value: "service_calls", label: "Service Calls" },
  { value: "diagnostic_reports", label: "Diagnostic Reports" },
];

const tableFields = {
  atms: [
    { name: "serial_num", label: "Serial number" },
    { name: "model", label: "Model" },
    { name: "cash_lvl", label: "Cash level", type: "number" },
    { name: "branch_id", label: "Branch ID", type: "number" },
    {
      name: "status",
      label: "Status",
      options: ["Operational", "Maintenance", "Offline"],
    },
  ],
  branches: [
    { name: "name", label: "Name" },
    { name: "location_region", label: "Location region" },
    { name: "capacity", label: "Capacity", type: "number" },
    { name: "supervisor_id", label: "Supervisor ID", type: "number" },
  ],
  technicians: [
    { name: "name", label: "Name" },
    { name: "branch_id", label: "Branch ID", type: "number" },
  ],
  service_calls: [
    { name: "title", label: "Title" },
    { name: "atm_id", label: "ATM ID", type: "number" },
    { name: "technician_id", label: "Technician ID", type: "number" },
    { name: "priority", label: "Priority", options: ["Low", "Medium", "Critical"] },
    {
      name: "status",
      label: "Status",
      options: ["Pending", "In-Progress", "Completed", "Failed"],
    },
  ],
  diagnostic_reports: [
    { name: "service_call_id", label: "Service Call ID", type: "number" },
    { name: "file_url", label: "File URL" },
    { name: "notes", label: "Notes", multiline: true },
  ],
};

function AddEntreeDialog({ open, onClose, onSuccess }) {
  const [selectedTable, setSelectedTable] = useState("");
  const [formValues, setFormValues] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);

  const handleTableChange = (event) => {
    const table = event.target.value;
    setSelectedTable(table);
    setSubmitError(null);
    setFormValues(
      Object.fromEntries(tableFields[table].map((field) => [field.name, ""]))
    );
  };

  const handleFieldChange = (event) => {
    const { name, value } = event.target;
    setFormValues((currentValues) => ({
      ...currentValues,
      [name]: value,
    }));
  };

  const validateForm = () => {
    const invalidFields = tableFields[selectedTable].filter((field) => {
      const value = formValues[field.name];
      const isEmpty = value === undefined || value === null || String(value).trim() === "";
      const isNegativeNumber = field.type === "number" && Number(value) < 0;

      return isEmpty || isNegativeNumber;
    });

    if (invalidFields.length === 0) return true;

    const fieldLabels = invalidFields.map((field) => field.label).join(", ");
    setSubmitError(`Please provide valid values for: ${fieldLabels}.`);
    return false;
  };

  const handleCreate = async () => {
    if (!validateForm()) return;

    setIsSubmitting(true);
    setSubmitError(null);

    try {
      const response = await apiClient.post(`/${selectedTable}`, formValues);
      onSuccess?.(response.data);
      onClose();
    } catch (error) {
      const message = error.response?.data?.detail || error.message || "The entree could not be created.";
      setSubmitError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle sx={{color: 'black'}}>Add Entree</DialogTitle>
      <DialogContent>
        <FormControl fullWidth sx={{ mt: 1 }}>
          <InputLabel id="add-entree-table-label">Data table</InputLabel>
          <Select
            labelId="add-entree-table-label"
            id="add-entree-table"
            label="Data table"
            value={selectedTable}
            onChange={handleTableChange}
          >
            <MenuItem value="" disabled>
              Select a data table
            </MenuItem>
            {dataTables.map((table) => (
              <MenuItem key={table.value} value={table.value}>
                {table.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        {submitError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {submitError}
          </Alert>
        )}
        {selectedTable && (
          <Box sx={{ display: "grid", gap: 2, mt: 3 }}>
            {tableFields[selectedTable].map((field) => (
              field.options ? (
                <FormControl key={field.name} fullWidth>
                  <InputLabel id={`${selectedTable}-${field.name}-label`}>
                    {field.label}
                  </InputLabel>
                  <Select
                    labelId={`${selectedTable}-${field.name}-label`}
                    id={`${selectedTable}-${field.name}`}
                    label={field.label}
                    name={field.name}
                    value={formValues[field.name] || ""}
                    onChange={handleFieldChange}
                  >
                    {field.options.map((option) => (
                      <MenuItem key={option} value={option}>
                        {option}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              ) : (
                <TextField
                  key={field.name}
                  label={field.label}
                  name={field.name}
                  type={field.type || "text"}
                  value={formValues[field.name] || ""}
                  onChange={handleFieldChange}
                  multiline={field.multiline}
                  minRows={field.multiline ? 3 : undefined}
                  fullWidth
                />
              )
            ))}
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={isSubmitting}>Cancel</Button>
        <Button variant="contained" onClick={handleCreate} disabled={!selectedTable || isSubmitting}>
          {isSubmitting ? <CircularProgress size={24} color="inherit" /> : "Add Entree"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default AddEntreeDialog;
