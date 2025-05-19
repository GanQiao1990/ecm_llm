"""
Serial communication handler for the ECG Receiver application.
"""

import serial
import serial.tools.list_ports
import threading
import time

class SerialHandler:
    """Handles serial communication with the ESP32."""
    
    def __init__(self, baudrate=57600):
        """Initialize the serial handler."""
        self.serial_port = None
        self.is_connected = False
        self.baudrate = baudrate
        self.reading_thread = None
        self.stop_thread = False
    
    def list_ports(self):
        """List available serial ports."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
    def connect(self, port):
        """Connect to the specified serial port.
        
        Args:
            port (str): The serial port to connect to.
            
        Returns:
            bool: True if connection was successful, False otherwise.
        """
        try:
            self.serial_port = serial.Serial(port, self.baudrate, timeout=1)
            self.is_connected = True
            print(f"Connected to {port} at {self.baudrate} baud")
            return True
        except Exception as e:
            print(f"Error connecting to {port}: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """Disconnect from the serial port."""
        # Stop the reading thread if it's running
        if self.reading_thread and self.reading_thread.is_alive():
            self.stop_thread = True
            self.reading_thread.join(timeout=1.0)
        
        # Close the serial port
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            print("Disconnected from serial port")
        
        self.is_connected = False
    
    def start_reading(self, callback):
        """Start reading data from the serial port in a separate thread.
        
        Args:
            callback (callable): Function to call with each line of data.
        """
        if not self.is_connected:
            print("Cannot start reading: not connected")
            return False
        
        # Stop any existing thread
        if self.reading_thread and self.reading_thread.is_alive():
            self.stop_thread = True
            self.reading_thread.join(timeout=1.0)
            
        # Reset thread control flag
        self.stop_thread = False
        
        # Start a new thread
        self.reading_thread = threading.Thread(
            target=self._read_serial_data,
            args=(callback,),
            daemon=True
        )
        self.reading_thread.start()
        return True
    
    def _read_serial_data(self, callback):
        """Read data from the serial port in a separate thread.
        
        Args:
            callback (callable): Function to call with each line of data.
        """
        buffer = ""
        last_data_time = time.time()
        
        while not self.stop_thread and self.is_connected and self.serial_port and self.serial_port.is_open:
            try:
                # Read all available data
                if self.serial_port.in_waiting > 0:
                    buffer += self.serial_port.read(self.serial_port.in_waiting).decode('ascii', errors='ignore')
                    last_data_time = time.time()
                    
                    # Process complete lines
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        if callback:
                            callback(line.strip())
                
                # Check for timeout (2 seconds without data)
                if time.time() - last_data_time > 2:
                    print("Warning: No data received (timeout)")
                    time.sleep(0.1)
                    
            except Exception as e:
                print(f"Error reading serial data: {e}")
                time.sleep(0.1)
