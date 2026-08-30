INSERT INTO branches (id, name, location_region, capacity, supervisor_id) VALUES
    (1, 'Citi Bank Corp - Southeast Branch', 'US-Southeast', 100, 101),
    (2, 'Bank of America Corp - Northeast Branch', 'US-Northeast', 100, 101);

INSERT INTO technicians (id, name, branch_id) VALUES
    (201, 'Henry Cavel', 1),
    (202, 'Simon Melvil', 1),
    (203, 'Dan Williams', 2);

INSERT INTO atms (id, serial_num, model, cash_lvl, branch_id, status) VALUES
    (1, 'DL-381920', 'Model XL 3.4', 783.02, 1, 'Operational'),
    (2, 'DL-334518', 'Model XL 3.4', 495.23, 2, 'Low_Cash'),
    (3, 'DL-318291', 'Model XL 3.4', 5928.10, 1, 'Operational'),
    (4, 'DL-393023', 'Model XL 3.4', 3129.45, 2, 'Maintenance'),
    (5, 'DL-371140', 'Model XL 3.4', 3810.78, 2, 'Operational');

INSERT INTO service_calls (id, title, atm_id, technician_id, priority, status) VALUES
    (1, 'Account Access Denied', 1, 201, 'Low', 'In-Progress'),
    (2, 'Machine Out of Service Error', 4, 201, 'Low', 'Pending'),
    (3, 'Machine Jamming Problem', 2, 203, 'Medium', 'Completed'),
    (4, 'Security Concerns', 3, 202, 'Critical', 'In-Progress');

INSERT INTO diagnostic_reports (id, service_call_id, file_url, notes) VALUES
    (1, 3, 'path', 'Issue fixed: replaced deposit funnel mechanism'),
    (2, 4, 'path2', 'May stem from outdated systems');