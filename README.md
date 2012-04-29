# Abinit band structure csv script kit

Extract band structure data from abinit `.out` files and write to `stdout` in a universal `.csv` format.

All scripts work with Python 3 (tested with 3.2.3), but `abinit_bands_csv_to_gnuplot.py` doesn't work with Python 2 (tested with 2.7.3). Python3 interpreter might be named in many ways in your system. Try:

`python [script_name]`

`python3 [script_name]`

`env python3 [script_name]`

And ensure that python3 is installed in your system: look in `/usr/bin` for anything beginning with `python`, run `python -V` or finally try to install python3 using your package manager.

## abinit_bands_to_csv.py
Extracts band structure data from an Abinit `.out` file. Typical usage:

`python abinit_bands_info.py path/to/my/file.out > path/to/output/file.csv`

Since there might be many band structure datasets in one `.out` file, few options to pick the right one are provided. First: the second script might be used to view how many and how long datasets are there in the file. Second: this script provides few CLI parameters for picking the desired set.

Run `python abinit_bands_to_csv.py --help` to see the possible options.

## abinit_bands_info.py
Displays some info about the `.out` file.

## abinit_bands_csv_to_gnuplot.py
Looks into a generated `.csv` file and creates a gnuplot template, for easy graphing.

Tries to recognise high symmetry points and label them automatically. This is an experimental and not well-tested feature, please carefully check the output before publishing any graphs in Nature. Works only for FCC right now.

Typical usage:

`python abinit_bands_csv_to_gnuplot.py path/to/input/file.csv > path/to/output/file.gnuplot`
