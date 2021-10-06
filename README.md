# QPLIB query

Download [QPLIB](https://qplib.zib.de/)

Exract lp files in `QPLIB_query/lp` folder, and `instancedata.csv` to `QPLIB_query` directory

Convert lp files to mps files in `QPLIB_query/mps` folder (CPLEX required):
```
/bin/bash lp2mps.sh
```

Parse `instancedata.csv`, create two sub benchmarks in `QPLIB_query/Continuous` and `QPLIB_query/Discrete`
```
python3 stat.py
```

`QPLIB_query/Continuous` contains lp files and mps files for non-convex QCQP/QP/QCP instances, `nonconvex_continous_data.csv` contains statistics for these instances.

`QPLIB_query/Discrete` contains lp files and mps files for non-convex MI-QCQP/QP/QCP instances,  `nonconvex_discrete_data.csv` contains statistics for these instances.


