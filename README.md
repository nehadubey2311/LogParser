log_parser.py
==================================================================
To execute this program run from command line as below:

	$ python log_parser.py 

Description
==================================================================
This program accepts following user input:
1. Path to zipped debugInfo (log file)
2. Fault to be looked up in logs from pre-defined faults
3. If not from pre-defined then any error string to look for


It will then unzip debugInfo log to a predefined destination
after clearing it up and parse logs for fault entered.
The results are then plotted as bar graph and results are provided
in tabular form.

Also a detailed description is provided to help debug the issue
