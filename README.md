# PostgreSQL Speed Test
Paired speed comparison for a PostgreSQL server.

Compares the throughput of PostgreSQL server against another.

## Methodology
Thirty (30) trials will be conducted. In each trial, the following queries will
be run. This simulates an average workload for SQL.

1. Creation of 4 tables, each with 2-8 columns.
2. Between 100 and 10000 rows will be inserted into each table.
3. 5000 random statements of type select, insert, update, or delete.

## Instructions
Edit the file `postgrestest.ini` with the connection information for the servers you want to compare.

This program is single-threaded. It is recommended to host the PostgreSQL server on another machine, or at least set its affinity to a different CPU from the testing if testing on a single multicore machine.

## License
```
    Copyright (C) 2025  Yuliang Huang <https://github.com/yhuang3-uf/>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
