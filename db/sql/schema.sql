CREATE TYPE ATM_STATUS AS ENUM ('Operational', 'Maintenance', 'Offline');
CREATE TYPE SERVICE_CALL_STATUS AS ENUM ('Pending', 'In-Progress', 'Completed', 'Failed');
CREATE TYPE SERVICE_CALL_PRIORITY AS ENUM ('Low', 'Medium', 'Critical');

--Branches Table
CREATE TABLE IF NOT EXISTS branches (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location_region VARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    supervisor_id INT NOT NULL
);

--Technicians Table
CREATE TABLE IF NOT EXISTS technicians (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    branch_id INT NOT NULL REFERENCES branches(id)
);

--ATMS Table
CREATE TABLE IF NOT EXISTS atms (
    id SERIAL PRIMARY KEY,
    serial_num VARCHAR(50) NOT NULL UNIQUE,
    model VARCHAR(100) NOT NULL,
    cash_lvl NUMERIC(6, 2) NOT NULL CHECK (cash_lvl BETWEEN 0 AND 100),
    branch_id INT NOT NULL REFERENCES branches(id),
    status ATM_STATUS NOT NULL DEFAULT 'Offline'
);

--Service Call Table
CREATE TABLE IF NOT EXISTS service_calls (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    atm_id INT NOT NULL REFERENCES atms(id),
    technician_id INT NOT NULL REFERENCES technicians(id),
    priority SERVICE_CALL_PRIORITY NOT NULL,
    status SERVICE_CALL_STATUS NOT NULL DEFAULT 'Pending'
);

--Diagnostic Reports Table
CREATE TABLE IF NOT EXISTS diagnostic_reports (
    id SERIAL PRIMARY KEY,
    service_call_id INT NOT NULL REFERENCES service_calls(id),
    file_url TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);