-- Sets the needed Permissions in MySQL/MariaDB.
-- Replace "PACKMANSENSUSER" with your user account and "YOURPASS" with your password
-- Then provide them in your packman.conf

GRANT USAGE ON *.* TO 'PACKMANSENSUSER'@'%' IDENTIFIED BY PASSWORD Password('YOURPASS');
GRANT INSERT, REFERENCES ON `packMan`.`pM_Logs` TO 'PACKMANSENSUSER'@'%';
GRANT SELECT, INSERT, UPDATE ON `packMan`.`pM_DigitalInputs` TO 'PACKMANSENSUSER'@'%';
GRANT SELECT, REFERENCES ON `packMan`.`pM_Events` TO 'PACKMANSENSUSER'@'%';
