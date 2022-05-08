# pwl-utilities

Utilities for working with LTspice PWL files.

### Usage

### `csv_to_pwl.py` 

Converts an oscilloscope trace CSV file to a PWL file.

The CSV file should contain a single voltage value per line. 

The sample interval should be specified via the `-s` or `--sample_interval` option.

Example:

```
python3 csv_to_pwl.py -i trace.csv -o trace.pwl -s 0.4ns
```

The input and/or output files may be left unspecified, in which case stdin / stdout are used. 

### `pwl_cycle.py`

Create a PWL that repeats a given PWL a number of times using a specified period.

The number of cycles should be specified via the `-n` or `--num_cycles` option.

The period per cycle should be specified via the `-p` or `--period` option.

The input and/or output files may be left unspecified, in which case stdin / stdout are used. 

Example:


```
python3 pwl_cycle.py -i trace.pwl -n 12 -p 3µs
```
