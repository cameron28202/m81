from lakeshore import SSMSystem
import pyvisa
from time import sleep
from math import sqrt

# Connect to instrument via USB
my_M81 = SSMSystem()

# Instantiate source and measure modules
balanced_current_source = my_M81.get_source_module(1)
voltage_measure = my_M81.get_measure_module(1)

def set_digital_io(side):
    # establish connection
    rm = pyvisa.ResourceManager()
    device_address = "" # what is device address?
    instrument = rm.open_resource(device_address)

    # see which side the device is currently on
    initial_cmd = 'DIGital:OSETing?'
    current_bit = instrument.query(initial_cmd)
    print(f"Current bit: {current_bit}")

    # send command to change sides
    cmd = f'DIGital:OSETing {side}'
    instrument.write(cmd)

    # see if it changed to the correct side (bit)
    verify_cmd = 'DIGital:OSETing?'
    new_bit = instrument.query(verify_cmd)
    print(f"New updated bit: {new_bit}")


def measure_resistance():
    # Set the source frequency to 13.7 Hz
    balanced_current_source.set_frequency(13.7)

    # Set the source current peak amplitude to 1 mA
    balanced_current_source.set_current_amplitude(0.001)

    # Set the voltage measure module to reference the source 1 module with a 100 ms time constant
    voltage_measure.setup_lock_in_measurement('S1', 0.1)

    # Enable the source output
    balanced_current_source.enable()

    # Wait for 15 time constants before taking a measurement
    sleep(1.5)
    lock_in_magnitude = voltage_measure.get_lock_in_r()

    # Get the amplitude of the current source
    peak_current = balanced_current_source.get_current_amplitude()

    # Calculate the resistance
    return lock_in_magnitude * sqrt(2) / peak_current

def calculate_conductivity():
    pass

def main():
    resistances = []
    for side in range(1, 5):
        set_digital_io(side)
        resistance = measure_resistance()
        print(f"Resistance for side {side}: {resistance}")
        resistances.append(resistance)
    
    avg_resistance = sum(resistances) / len(resistances)
    print(f"Average resistance: {avg_resistance}")

if __name__ == "__main__":
    main()