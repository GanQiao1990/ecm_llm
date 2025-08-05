"""
Main window for the ECG Receiver application.
"""

from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, 
                           QPushButton, QComboBox, QHBoxLayout, QLabel, QMessageBox)
from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot
import pyqtgraph as pg
import numpy as np
import time
from datetime import datetime
import os

from ..core.serial_handler import SerialHandler
from ..core.data_recorder import DataRecorder

class ECGMainWindow(QMainWindow):
    """Main window for the ECG Receiver application."""
    
    # Define signals for thread safety
    data_received = pyqtSignal(str)
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Application state
        self.serial_handler = SerialHandler()
        self.data_recorder = DataRecorder()
        
        # Data buffers - increased size for better visualization
        self.max_points = 2000  # Increased buffer size
        self.time_data = np.zeros(self.max_points)
        self.ecg_data = np.zeros(self.max_points)
        self.pointer = 0
        
        # Create the time axis (time in seconds, 8 seconds of data)
        self.time_axis = np.linspace(-8, 0, self.max_points)
        
        # Connection state
        self.current_port = None
        self.packets_received = 0
        self.last_packet_time = None
        
        # Connect signals
        self.data_received.connect(self.process_data_slot)
        
        # Initialize the UI
        self.init_ui()
        
        # Set up data update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)  # Update at 20Hz
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('ECG Real-time Monitor')
        self.setGeometry(100, 100, 1200, 800)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        
        # Control panel
        control_layout = QHBoxLayout()
        
        # Port selection
        self.port_combo = QComboBox()
        self.port_combo.setMinimumWidth(150)
        control_layout.addWidget(QLabel("Port:"))
        control_layout.addWidget(self.port_combo)
        
        # Connect/Disconnect button
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.toggle_connection)
        control_layout.addWidget(self.connect_btn)
        
        # Refresh ports button
        refresh_btn = QPushButton("Refresh Ports")
        refresh_btn.clicked.connect(self.scan_ports)
        control_layout.addWidget(refresh_btn)
        
        # Record button
        self.record_btn = QPushButton("Start Recording")
        self.record_btn.setEnabled(False)
        self.record_btn.clicked.connect(self.toggle_recording)
        control_layout.addWidget(self.record_btn)
        
        # Status label
        self.status_label = QLabel("Status: Disconnected")
        control_layout.addWidget(self.status_label)
        
        layout.addLayout(control_layout)
        
        # Plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setLabel('left', 'ECG (μV)')
        self.plot_widget.setLabel('bottom', 'Time (s)')
        self.plot_widget.setTitle('ECG Waveform')
        self.plot_curve = self.plot_widget.plot(pen='b')
        
        layout.addWidget(self.plot_widget)
        main_widget.setLayout(layout)
        
        # Initial port scan
        self.scan_ports()
    
    def scan_ports(self):
        """Scan for available serial ports."""
        self.port_combo.clear()
        for port in self.serial_handler.list_ports():
            self.port_combo.addItem(port)
    
    def toggle_connection(self):
        """Connect to or disconnect from the selected serial port."""
        if not self.serial_handler.is_connected:
            port = self.port_combo.currentText()
            if not port:
                self.status_label.setText("Status: No port selected")
                QMessageBox.warning(self, "Connection Error", "Please select a serial port.")
                return
                
            print(f"Attempting to connect to {port}...")
            self.current_port = port
            
            if self.serial_handler.connect(port):
                self.connect_btn.setText("Disconnect")
                self.record_btn.setEnabled(True)
                self.status_label.setText(f"Status: Connected to {port}")
                
                # Reset statistics
                self.packets_received = 0
                
                # Clear previous data
                self.pointer = 0
                self.ecg_data.fill(0)
                
                print(f"Successfully connected to {port}")
                
                # Start the data processing thread with thread-safe callback
                self.serial_handler.start_reading(self.handle_serial_data)
            else:
                self.status_label.setText(f"Status: Connection failed")
                QMessageBox.critical(self, "Connection Error", 
                                   f"Could not connect to {port}.\n\n"
                                   "Please check:\n"
                                   "- Device is connected\n"
                                   "- Port is not in use\n"
                                   "- Device drivers are installed")
        else:
            self.disconnect_serial()
    
    def disconnect_serial(self):
        """Disconnect from the serial port."""
        if self.data_recorder.recording:
            self.stop_recording()
            
        self.serial_handler.disconnect()
        self.connect_btn.setText("Connect")
        self.record_btn.setEnabled(False)
        self.status_label.setText("Status: Disconnected")
    
    def toggle_recording(self):
        """Start or stop recording data to CSV."""
        if not self.data_recorder.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording data to a CSV file."""
        if self.data_recorder.start_recording():
            self.record_btn.setText("Stop Recording")
            self.status_label.setText(f"Status: Recording to {self.data_recorder.current_filename}")
        else:
            self.status_label.setText("Status: Could not start recording")
    
    def stop_recording(self):
        """Stop recording data to CSV."""
        self.data_recorder.stop_recording()
        self.record_btn.setText("Start Recording")
        self.status_label.setText("Status: Connected")
    
    def handle_serial_data(self, data):
        """Handle data received from serial port (called from worker thread)."""
        # Emit signal to handle data in main thread
        self.data_received.emit(data)
    
    @pyqtSlot(str)
    def process_data_slot(self, data):
        """Process data in the main thread (connected to data_received signal)."""
        self.process_data(data)
    
    def process_data(self, data):
        """Process a data line and update the buffers."""
        current_time = time.time()
        self.last_packet_time = current_time
        
        # Handle different data formats
        ecg_value = None
        
        if data.startswith('DATA,'):
            # Standard CSV format: "DATA,timestamp,ecg,resp,hr,status"
            try:
                parts = data.split(',')
                if len(parts) >= 4:  # We need at least timestamp, ecg, resp, hr
                    ecg_value = float(parts[2])
            except (ValueError, IndexError) as e:
                print(f"Error parsing CSV data: {data[:50]}... Error: {e}")
                
        elif data.startswith('ERROR,') or data.startswith('INFO,'):
            # Log system messages
            print(f"Device: {data}")
            return  # Don't process as ECG data
            
        else:
            # Try to parse as simple numeric data
            try:
                data_clean = data.strip()
                
                # Handle single numeric value (like "-7", "-6", "-5")
                if data_clean and (data_clean.replace('-', '').replace('.', '').isdigit() or 
                                   data_clean.replace('-', '').replace('.', '').replace(' ', '').isdigit()):
                    ecg_value = float(data_clean)
                    
                # Handle multiple space/comma separated values
                else:
                    parts = data_clean.replace(',', ' ').split()
                    if 1 <= len(parts) <= 5:  # 1-5 numeric values
                        # Try each part as potential ECG value
                        for part in parts:
                            try:
                                test_value = float(part.strip())
                                # Use the first valid numeric value as ECG
                                if ecg_value is None:
                                    ecg_value = test_value
                                break
                            except ValueError:
                                continue
                                
            except Exception as e:
                # If we can't parse it at all, just log it
                if data.strip():  # Only log non-empty lines
                    print(f"Unknown data format: {data[:50]}...")
                return
        
        # If we successfully extracted an ECG value, process it
        if ecg_value is not None:
            # Update statistics
            self.packets_received += 1
            
            # Update data buffer
            self.ecg_data[self.pointer] = ecg_value
            self.pointer = (self.pointer + 1) % self.max_points
            
            # Save to CSV if recording
            if self.data_recorder.recording:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                self.data_recorder.write_data(timestamp, ecg_value)
                
            # Optional: Print received values for debugging
            if self.packets_received % 50 == 0:  # Print every 50th packet
                print(f"Received ECG value: {ecg_value} (Packet #{self.packets_received})")
    
    def update_plot(self):
        """Update the plot with new data."""
        if self.pointer == 0:
            return
            
        # Create x-axis data (time in seconds, assuming 200Hz sampling rate)
        x = np.roll(self.time_axis, -self.pointer)
        
        # Get the data in the correct order for plotting
        if self.pointer > 0:
            y = np.concatenate((self.ecg_data[self.pointer:], self.ecg_data[:self.pointer]))
        else:
            y = self.ecg_data
            
        # Update the plot
        self.plot_curve.setData(x, y)
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.disconnect_serial()
        event.accept()
