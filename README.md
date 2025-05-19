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
   git clone https://github.com/GanQiao1990/ecg-receiver.git
   cd ecg-receiver
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

- **No COM ports available**:
  - Make sure the ESP32 is properly connected
  - Install the correct USB drivers for your ESP32
  - Try unplugging and reconnecting the USB cable

- **Connection issues**:
  - Check that the baud rate matches (default: 57600)
  - Ensure no other program is using the serial port
  - Verify the ESP32 is sending data in the expected format

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
