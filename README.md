# Sql-Time-Based-Bruteforce
POC : Bruteforce any field from a SQL table in linear time. This scripts targets a login form vulnerable to time-based SQL injection.

If a website is vulnerable to SQL injection, but does not display any error message, you can use this script to quickly bruteforce anything in the database using the server response time. 

You will need to craft SQL queries for the target website.
This script can be easily adapted to bruteforce using errors instead of delays.
With appropriate queries, you can also bruteforce table or column names and probably many other things.
