#!/bin/bash

export PG_USERNAME=postgres
export PG_PASSWORD=postgres
export PG_HOST=127.0.0.1
export PG_PORT=5432
export PG_DATABASE=postgres

export PGTEST_OUTFILE=testresults.out
export PGTEST_QUERYCOUNT=1000

taskset 0x0001 python -u postgrestest.py
