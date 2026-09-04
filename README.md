# Revature In-Training Project - CashCow
This project is a culmination of the work learning how to use Python, SQL, AWS and other technologies.

## LATEST BUGS
- Primary Key Sequencing - The datatables are filled with dummy data upon start up, but the data isn't tracked by anything, so when trying add new entrees, the table must cycle through all Primary Keys currently in use until it reaches the end and can start using new ones. This should be patched out later.

### FEATURES TO BE ADDED
- RichTreeList Actions - The RichTreeList can only display data, but none of the data can be manipulated/modified or deleted. Adding data requires hitting a button completely disconnected from it. Rather than this setup, each entree in the list should have a "modify" and "delete" button on all items, along with a button at the bottom of any given list to add an entree to that specific list.
- Diagnostic Report File Uploading - while it is possible to add files to the s3 bucket associated with diagnostic reports, it can only be done via command terminal. It should be implemented into the frontend whenever a user tries to add a diagnostic report and should be required for a post to go through to prevent "broken" entrees.
- User Posts - there is currently no way to add new users other than hard coding them into the "seed_users" script. This should be implemented into the frontend as an admin-only action.