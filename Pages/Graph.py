# graph_widget.py
import re
import time
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QMessageBox, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QTime, QThread, pyqtSignal, QTimer
from GetData import GetData

class GraphWidget(QWidget):
    def __init__(self, parent=None, sensitivity_threshold=None):
        super().__init__(parent)
        
        # Store sensitivity threshold
        self.sensitivity_threshold = sensitivity_threshold
        self.peak_pressure = None
        self.peak_time = None
        self.test_completed = False
        self.test_started = False

        layout = QVBoxLayout(self)

        # Add control panel for sensitivity input and test controls
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        
        # Sensitivity input
        sensitivity_label = QLabel("Sensitivity Threshold:")
        self.sensitivity_input = QLineEdit()
        self.sensitivity_input.setPlaceholderText("Enter sensitivity value")
        if self.sensitivity_threshold:
            self.sensitivity_input.setText(str(self.sensitivity_threshold))
        
        # Test control buttons
        self.start_test_btn = QPushButton("Start Test")
        self.reset_test_btn = QPushButton("Reset Test")
        self.test_mode_btn = QPushButton("Test Mode (Fake Data)")
        
        # Peak pressure display
        self.peak_label = QLabel("Peak Pressure: Not detected")
        self.peak_label.setStyleSheet("font-weight: bold; color: red;")
        
        control_layout.addWidget(sensitivity_label)
        control_layout.addWidget(self.sensitivity_input)
        control_layout.addWidget(self.start_test_btn)
        control_layout.addWidget(self.reset_test_btn)
        control_layout.addWidget(self.test_mode_btn)
        control_layout.addWidget(self.peak_label)
        control_layout.addStretch()
        
        layout.addWidget(control_panel)

        # Create plot widget with better performance settings
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        # Setup plot with better styling
        self.plot_widget.setLabel('left', 'Pressure (hPa)')
        self.plot_widget.setLabel('bottom', 'Time (s)')
        self.plot_widget.showGrid(x=True, y=True)
        
        # Enable auto-range for better visualization
        self.plot_widget.enableAutoRange('xy', True)
        
        # Set background color for better visibility
        self.plot_widget.setBackground('w')  # white background

        # Data storage - increased buffer size for smoother plotting
        self.x = []
        self.y = []
        self.max_points = 200  # Increased from 20 to 200 for smoother curves
        self.start_time = QTime.currentTime()

        # Plot references
        self.curve = self.plot_widget.plot(self.x, self.y, pen=pg.mkPen(color='b', width=2))
        
        # Threshold line (will be added when test starts)
        self.threshold_line = None
        
        # Peak point marker (will be added when peak is detected)
        self.peak_marker = None

        # Connect button signals
        self.start_test_btn.clicked.connect(self.start_test)
        self.reset_test_btn.clicked.connect(self.reset_test)
        self.test_mode_btn.clicked.connect(self.start_test_mode)
        
        # Test mode variables
        self.test_mode = False
        self.test_timer = QTimer()
        self.test_timer.timeout.connect(self.generate_test_data)

    def start_test(self):
        """Start the paper bursting test"""
        try:
            self.sensitivity_threshold = float(self.sensitivity_input.text())
            if self.sensitivity_threshold <= 0:
                QMessageBox.warning(self, "Invalid Input", "Sensitivity threshold must be greater than 0")
                return
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for sensitivity threshold")
            return
        
        self.test_started = True
        self.test_completed = False
        self.peak_pressure = None
        self.peak_time = None
        
        # Clear previous data
        self.x.clear()
        self.y.clear()
        self.start_time = QTime.currentTime()
        
        # Add threshold line
        if self.threshold_line is not None:
            self.plot_widget.removeItem(self.threshold_line)
        
        self.threshold_line = self.plot_widget.addLine(y=self.sensitivity_threshold, pen=pg.mkPen(color='r', width=2, style=pg.QtCore.Qt.DashLine))
        
        # Remove previous peak marker
        if self.peak_marker is not None:
            self.plot_widget.removeItem(self.peak_marker)
            self.peak_marker = None
        
        # Update UI
        self.start_test_btn.setEnabled(False)
        self.sensitivity_input.setEnabled(False)
        self.test_mode_btn.setEnabled(False)
        self.peak_label.setText("Peak Pressure: Testing...")
        self.peak_label.setStyleSheet("font-weight: bold; color: orange;")

    def reset_test(self):
        """Reset the test to initial state"""
        self.test_started = False
        self.test_completed = False
        self.test_mode = False
        self.peak_pressure = None
        self.peak_time = None
        
        # Stop test mode timer
        self.test_timer.stop()
        
        # Clear data
        self.x.clear()
        self.y.clear()
        self.curve.setData(self.x, self.y)
        
        # Remove threshold line and peak marker
        if self.threshold_line is not None:
            self.plot_widget.removeItem(self.threshold_line)
            self.threshold_line = None
        
        if self.peak_marker is not None:
            self.plot_widget.removeItem(self.peak_marker)
            self.peak_marker = None
        
        # Update UI
        self.start_test_btn.setEnabled(True)
        self.sensitivity_input.setEnabled(True)
        self.test_mode_btn.setEnabled(True)
        self.peak_label.setText("Peak Pressure: Not detected")
        self.peak_label.setStyleSheet("font-weight: bold; color: red;")

    def update_plot(self, value):
        """Add new pressure value to graph"""
        if value is None:
            return

        elapsed = self.start_time.msecsTo(QTime.currentTime()) / 1000.0  # seconds
        self.x.append(elapsed)
        self.y.append(value)

        # Only check for peak detection if test is started and not completed
        if self.test_started and not self.test_completed and self.sensitivity_threshold is not None:
            # Check if sensitivity threshold is crossed
            if value >= self.sensitivity_threshold and self.peak_pressure is None:
                # Peak detected - this is the highest pressure the paper can hold
                self.peak_pressure = value
                self.peak_time = elapsed
                self.test_completed = True
                
                # Stop test mode timer if it's running
                if self.test_mode:
                    self.test_timer.stop()
                
                # Add peak marker
                self.peak_marker = self.plot_widget.plot([self.peak_time], [self.peak_pressure], 
                                                       symbol='o', symbolSize=10, 
                                                       pen=pg.mkPen(color='red', width=3),
                                                       symbolBrush='red')
                
                # Update UI
                self.peak_label.setText(f"Peak Pressure: {self.peak_pressure:.2f} hPa - TEST COMPLETED")
                self.peak_label.setStyleSheet("font-weight: bold; color: green;")
                
                # Re-enable controls
                self.start_test_btn.setEnabled(True)
                self.sensitivity_input.setEnabled(True)
                self.test_mode_btn.setEnabled(True)
                
                # Update the curve data before returning
                self.curve.setData(self.x, self.y)
                self.plot_widget.update()
                return

        # Keep last max_points for smooth visualization
        if len(self.x) > self.max_points:
            # Remove older points but keep more for smoother curve
            remove_count = len(self.x) - self.max_points
            self.x = self.x[remove_count:]
            self.y = self.y[remove_count:]

        # Update the curve data
        self.curve.setData(self.x, self.y)
        
        # Force immediate update
        self.plot_widget.update()

    def start_test_mode(self):
        """Start test mode with fake data generation"""
        self.test_mode = True
        self.test_started = True
        self.test_completed = False
        self.peak_pressure = None
        self.peak_time = None
        
        # Clear previous data
        self.x.clear()
        self.y.clear()
        self.start_time = QTime.currentTime()
        
        # Set a default sensitivity if not set
        if self.sensitivity_threshold is None:
            try:
                self.sensitivity_threshold = float(self.sensitivity_input.text())
            except ValueError:
                self.sensitivity_threshold = 50.0  # Default threshold
                self.sensitivity_input.setText("50.0")
        
        # Add threshold line
        if self.threshold_line is not None:
            self.plot_widget.removeItem(self.threshold_line)
        
        self.threshold_line = self.plot_widget.addLine(y=self.sensitivity_threshold, pen=pg.mkPen(color='r', width=2, style=pg.QtCore.Qt.DashLine))
        
        # Remove previous peak marker
        if self.peak_marker is not None:
            self.plot_widget.removeItem(self.peak_marker)
            self.peak_marker = None
        
        # Start generating fake data
        self.test_timer.start(100)  # Generate data every 100ms
        
        # Update UI
        self.start_test_btn.setEnabled(False)
        self.sensitivity_input.setEnabled(False)
        self.test_mode_btn.setEnabled(False)
        self.peak_label.setText("Peak Pressure: Testing...")
        self.peak_label.setStyleSheet("font-weight: bold; color: orange;")

    def generate_test_data(self):
        """Generate fake pressure data for testing"""
        import random
        import math
        
        if not self.test_mode or self.test_completed:
            self.test_timer.stop()  # Stop timer if test is completed
            return
        
        # Generate increasing pressure with some noise
        elapsed = self.start_time.msecsTo(QTime.currentTime()) / 1000.0
        base_pressure = min(elapsed * 10, 100)  # Increase pressure over time, max 100
        noise = random.uniform(-2, 2)
        pressure = base_pressure + noise
        
        # Add some realistic pressure variation
        pressure += math.sin(elapsed * 2) * 5
        
        # Update the plot with fake data
        self.update_plot(pressure)

    def get_test_results(self):
        """Return test results"""
        return {
            'peak_pressure': self.peak_pressure,
            'peak_time': self.peak_time,
            'test_completed': self.test_completed,
            'sensitivity_threshold': self.sensitivity_threshold
        }


class SerialReader(QThread):
    new_value = pyqtSignal(float)
    error = pyqtSignal(str)

    def __init__(self, reader: GetData, command: str = "RAI01;", delay_seconds: float = 0.1):
        super().__init__()
        self._command = command
        self._delay_seconds = delay_seconds  # Reduced default delay for faster updates
        self._running = False
        self._reader = reader  # type: GetData | None

    def run(self):
        self._running = True
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        try:
            while self._running:
                try:
                    # Send command
                    if self._reader.ser.is_open:
                        # Clear any pending data first
                        if self._reader.ser.in_waiting > 0:
                            self._reader.ser.read_all()
                            
                        self._reader.ser.write(self._command.encode("ascii"))
                        self._reader.ser.flush()  # Ensure command is sent immediately
                        
                        # Wait a bit for response
                        time.sleep(0.01)  # Very short wait
                        
                        # Read response
                        raw = self._reader.ser.readline().decode(errors="ignore").strip()
                        
                        if raw:  # Only process if we got data
                            value = self._parse_first_float(raw)
                            if value is not None:
                                self.new_value.emit(value)
                                consecutive_errors = 0  # Reset error counter on success
                        
                    time.sleep(self._delay_seconds)
                    
                except Exception as loop_exc:
                    consecutive_errors += 1
                    if consecutive_errors <= max_consecutive_errors:
                        self.error.emit(f"Serial error (attempt {consecutive_errors}): {str(loop_exc)}")
                    
                    if consecutive_errors >= max_consecutive_errors:
                        self.error.emit(f"Too many consecutive errors. Stopping reader.")
                        break
                        
                    time.sleep(0.5)
                    
        finally:
            try:
                if self._reader is not None:
                    self._reader.close()
            except Exception:
                pass

    def stop(self):
        self._running = False

    def set_delay(self, delay_seconds: float):
        """Dynamically change the update rate"""
        self._delay_seconds = max(0.01, delay_seconds)  # Minimum 10ms delay

    @staticmethod
    def _parse_first_float(text: str):
        if not text:
            return None
        # More robust regex to handle various float formats
        match = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", text)
        if not match:
            return None
        try:
            return float(match.group(0))
        except Exception:
            return None


class GraphWindow(QMainWindow):
    def __init__(self, command: str = "RAI01;", delay_seconds: float = 0.1):
        super().__init__()
        self.setWindowTitle("Real-time Pressure Graph")
        self.setGeometry(100, 100, 800, 600)  # Set initial size

        self.graph = GraphWidget(self)
        self.setCentralWidget(self.graph)

        # Create reader with faster update rate, using a single GetData instance
        self._reader = SerialReader(reader=GetData(), command=command, delay_seconds=delay_seconds)
        self._reader.new_value.connect(self.graph.update_plot)
        self._reader.error.connect(self._on_error)
        
        # Add a timer to periodically update the graph display
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._force_update)
        self._update_timer.start(50)  # Update display every 50ms

    def _force_update(self):
        """Force graph update for smooth display"""
        self.graph.plot_widget.update()

    def start(self):
        if not self._reader.isRunning():
            self._reader.start()

    def stop(self):
        if self._reader.isRunning():
            self._reader.stop()
            self._reader.wait(1500)

    def set_update_rate(self, delay_seconds: float):
        """Change the data acquisition rate"""
        self._reader.set_delay(delay_seconds)

    def closeEvent(self, event):
        try:
            self.stop()
            self._update_timer.stop()
        finally:
            super().closeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        # Auto-start when shown
        self.start()

    def _on_error(self, message: str):
        # Show error but don't block the application
        print(f"Serial Error: {message}")  # Print to console
        # Optionally show message box for critical errors
        if "Failed to open" in message or "Too many consecutive errors" in message:
            QMessageBox.warning(self, "Serial Error", message)


# Example usage
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create window with faster update rate (10 times per second)
    window = GraphWindow(command="RAI01;", delay_seconds=0.1)
    window.show()
    
    sys.exit(app.exec_())