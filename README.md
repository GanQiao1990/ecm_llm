# ECG Receiver

A standalone application for real-time ECG data visualization from ADS1292R sensor connected to an ESP32 board.

## Features

- **Real-time ECG Monitoring**: View live ECG waveform with a scrolling display
- **Simple User Interface**: Easy-to-use GUI with port selection and recording controls
- **Data Logging**: Save ECG data to timestamped CSV files for later analysis
- **Cross-platform**: Works on Windows, macOS, and Linux

## Project Structure

```
ecg_receiver/
├── core/                 # Core functionality modules
│   ├── __init__.py       
│   ├── data_recorder.py  # Handles saving ECG data to CSV files
│   └── serial_handler.py # Manages serial communication with ESP32
├── gui/                  # User interface components
│   ├── __init__.py
│   └── main_window.py    # Main application window
├── __init__.py           # Package initialization
└── main.py               # Application entry point
```

## Requirements

- Python 3.8 or higher
- PyQt5 and PyQtGraph for the GUI
- pyserial for serial communication
- numpy for data processing
- ESP32 with ADS1292R shield
- USB cable for connecting ESP32 to computer

## Installation

### Method 1: From Source

1. **Clone the repository**
   ```bash
   git clone https://github.com/GanQiao1990/ecg_receiver_standalone-.git
   cd ecg_receiver_standalone-
   ```

2. **Install with pip**
   ```bash
   pip install -e .
   ```

### Method 2: Install Dependencies Directly

1. **Install required packages**
   ```bash
   pip install pyserial numpy PyQt5 pyqtgraph
   ```

## Usage

### Using as Installed Package

After installation, you can run the application from any directory:

```bash
ecg-receiver
```

### Running from Source

Navigate to the project directory and run:

```bash
python -m ecg_receiver.main
```

## ESP32 Configuration

1. **Upload the ESP32 Code**
   - Open `ESP32_ADS1292R_ECG.ino` in Arduino IDE
   - Select your ESP32 board and port
   - Upload the code to your ESP32

2. **Hardware Connection**
   - Connect ESP32 to your computer via USB
   - Connect the ADS1292R shield to the ESP32 following the pin mapping in the Arduino sketch

## Using the Application

1. **Launch the application** as described above
2. **Select your ESP32's COM port** from the dropdown menu
3. **Click "Connect"** to begin receiving data
4. **Click "Start Recording"** to save data to a CSV file (optional)
5. **Monitor the ECG waveform** in the main display

## Troubleshooting

### Connection Issues

- **No COM ports available**:
  - Make sure the ESP32 is properly connected
  - Install the correct USB drivers for your ESP32
  - Try unplugging and reconnecting the USB cable
  - On Linux, you may need permissions to access serial ports: `sudo usermod -a -G dialout $USER` (then logout/login)

- **Connection fails**:
  - Check that the baud rate matches (default: 57600)
  - Ensure no other program is using the serial port
  - Try different timeout values (the improved version automatically tries multiple timeouts)
  - Verify the ESP32 is sending data in the expected format

- **No data received**:
  - Check the ESP32 serial monitor to verify it's sending data
  - Ensure the data format matches: `DATA,timestamp,ecg_value,resp_value,heart_rate,status`
  - Try different serial port settings (the improved version tries multiple configurations)
  - Check for loose connections or cable issues

- **Data parsing errors**:
  - Verify the ESP32 is sending properly formatted CSV data
  - Check for missing commas or extra characters in the data stream
  - Enable debug logging to see raw data being received

### Testing Connection

Use the included test script to debug connection issues:

```bash
python test_connection.py
```

This script will:
- List available serial ports
- Attempt to connect to the first available port
- Display raw data being received
- Show connection statistics

### Performance Issues

- **Slow or choppy display**:
  - The buffer size has been increased to 2000 points (8 seconds of data)
  - Try reducing the plot update rate if your system is slow
  - Close other applications that might be using system resources

- **High CPU usage**:
  - The improved version uses more efficient data handling
  - Consider reducing the sample rate on the ESP32 side if needed

### Debug Mode

To enable detailed logging, modify the source code to increase verbosity or add print statements to track data flow.

## Improvements in This Version

- **Enhanced connection handling**: Multiple timeout attempts and better error recovery
- **Thread-safe data processing**: Uses Qt signals for safe GUI updates
- **Better error messages**: More descriptive error dialogs and status updates
- **Improved data validation**: Validates data format before processing
- **Larger data buffer**: 8 seconds of data display instead of 5
- **Connection testing**: Included test script for debugging
- **Automatic reconnection attempts**: Basic framework for reconnection (can be extended)
- **Better resource management**: Proper cleanup of threads and file handles

## Data Format

The ESP32 should send data in the following format:
```
DATA,timestamp,ecg_value,resp_value,heart_rate,status
```

For example:
```
DATA,1234567890,1024,512,75,OK
```

## License

This project is open source and available under the MIT License.

## Acknowledgments

- This project utilizes the ADS1292R ECG front-end chip for high-quality ECG signal acquisition
- Built with PyQt5 and PyQtGraph for efficient real-time visualization
