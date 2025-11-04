# PostgreSQL Speed Test
Speed test for a PostgreSQL server

## Methodology
Thirty (30) trials will be conducted. In each trial, the following queries will
be run. This simulates an average workload for SQL.

1. Creation of 3 tables, each with 2-8 columns.
2. 5 insert statements, to bootstrap the table with some data.
3. 1000 random statements of type select, insert, update, or delete.

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
