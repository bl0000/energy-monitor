-- SQL queries for calculating power usage for July 2024

USE energymon;

SELECT
    SUM(watts / 1000 * (5.0 / 60)) AS total_kwh_used
FROM power_used
WHERE added >= '2024-07-01 00:00:00'
  AND added < '2024-08-01 00:00:00';

 SELECT
    AVG(watts) AS average_power_used
FROM power_used
WHERE added >= '2024-07-01 00:00:00'
  AND added < '2024-08-01 00:00:00';
