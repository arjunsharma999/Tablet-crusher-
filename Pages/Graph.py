# graph_widget.py
import re
import time
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QMessageBox
from PyQt5.QtCore import QTime, QThread, pyqtSignal, QTimer
from GetData import GetData

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

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

        # Plot reference with better styling
        self.curve = self.plot_widget.plot(self.x, self.y, pen=pg.mkPen(color='b', width=2))

    def update_plot(self, value):
        """Add new pressure value to graph"""
        if value is None:
            return

        elapsed = self.start_time.msecsTo(QTime.currentTime()) / 1000.0  # seconds
        self.x.append(elapsed)
        self.y.append(value)

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