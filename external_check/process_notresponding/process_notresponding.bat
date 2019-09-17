@echo off
set process_name=%1
tasklist /FI  "IMAGENAME eq %process_name%" /FI "status eq NOT RESPONDING"|find "%process_name%" /c
