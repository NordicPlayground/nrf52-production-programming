# Testing your programming tool
Each folder in this directory contains a specific unit test. The tests provided so far are common and important edge cases that tool manufacturers need to consider when working with nRF52 series devices. Each test folder contains a description of the test and how to run it, along with the hex file (required to run the test) and source code (to understand what's going on).  

# example_test_script.py
This demonstrates how to test your tool. It uses [pynrfjprog](https://pypi.python.org/pypi/pynrfjprog/8.4.0) to test nrfjprog.exe (a programming tool provided by Nordic).  

To run:
> pip install pynrfjprog  
> make sure nrfjprog.exe is installed and in your system path  
> python example_test_script.py
