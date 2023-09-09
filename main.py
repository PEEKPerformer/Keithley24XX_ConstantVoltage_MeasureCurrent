import pyvisa
import time
import csv

# User Inputs
voltage = float(input("Enter the voltage in volts: "))
duration = float(input("Enter the duration in hours: "))
compliance = float(input("Enter the current compliance in milliamperes: "))

# Initialize PyVISA resource manager and connect to the Keithley 2420
rm = pyvisa.ResourceManager()
keithley = rm.open_resource('GPIB0::24::INSTR')

# Configure the SourceMeter to source voltage and set to user-defined voltage
keithley.write(f":SOUR:FUNC VOLT")
keithley.write(f":SOUR:VOLT {voltage}")

# Set current compliance to user-defined value in Amperes
keithley.write(f":SENS:CURR:PROT {compliance * 1e-3}")

# Open a CSV file to log the data
with open('test_data.csv', 'w', newline='') as csvfile:
    data_writer = csv.writer(csvfile)
    data_writer.writerow(['Time', 'Elapsed Time (s)', 'Current (A)'])

    # Capture the start time for elapsed time calculation
    start_time = time.time()

    # Loop for user-defined duration in seconds
    end_time = start_time + duration * 3600  # Convert duration to seconds
    while time.time() < end_time:
        # Query the instrument
        raw_data = keithley.query(":MEAS:CURR?")

        # Parse the string to get current
        parsed_data = raw_data.strip().split(',')
        current = float(parsed_data[1])  # Assuming current is the second value

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Log the data along with the current time and elapsed time
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        data_writer.writerow([current_time, elapsed_time, current])

        # Print elapsed time and measured current for debugging
        print(f"Elapsed time: {elapsed_time} seconds, Measured Current: {current} A")

        # Wait for the next measurement (every second)
        time.sleep(1)
