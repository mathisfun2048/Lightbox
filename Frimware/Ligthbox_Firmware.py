# main.py - LED Cube Audio Visualizer Main Application
import time
import threading
import signal
import sys
from led_controller import LEDMatrix
from audio_processor import AudioProcessor
from pattern_manager import PatternManager
from hardware_controls import ControlsManager
from config import Config

class LEDCubeApp:
    def __init__(self):
        self.config = Config()
        self.running = True
        
        # Initialize hardware components
        self.led_matrix = LEDMatrix(
            pin=18, 
            width=self.config.MATRIX_WIDTH, 
            height=self.config.MATRIX_HEIGHT
        )
        
        self.audio_processor = AudioProcessor(
            sample_rate=self.config.SAMPLE_RATE,
            chunk_size=self.config.CHUNK_SIZE
        )
        
        self.pattern_manager = PatternManager(self.led_matrix, self.audio_processor)
        self.controls = ControlsManager(
            rotary_pins=(2, 3, 4),  # A, B, Button
            button_pins=(17, 27)     # Button1, Button2
        )
        
        # Set up signal handlers for clean shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        print("\nShutting down gracefully...")
        self.running = False
        
    def handle_controls(self):
        """Handle rotary encoder and button inputs"""
        # Rotary encoder for pattern selection
        if self.controls.rotary_changed():
            direction = self.controls.get_rotary_direction()
            if direction > 0:
                self.pattern_manager.next_pattern()
            elif direction < 0:
                self.pattern_manager.previous_pattern()
                
        # Rotary button for mode switching
        if self.controls.rotary_button_pressed():
            self.pattern_manager.next_mode()
            
        # Button 1 for brightness control
        if self.controls.button1_pressed():
            self.led_matrix.adjust_brightness(0.1)
            
        # Button 2 for settings
        if self.controls.button2_pressed():
            self.pattern_manager.toggle_settings()
    
    def run(self):
        """Main application loop"""
        print("LED Cube Audio Visualizer Starting...")
        
        # Start audio processing in separate thread
        audio_thread = threading.Thread(target=self.audio_processor.start)
        audio_thread.daemon = True
        audio_thread.start()
        
        print("System ready!")
        
        try:
            while self.running:
                # Handle user controls
                self.handle_controls()
                
                # Update current pattern
                self.pattern_manager.update()
                
                # Update LED matrix
                self.led_matrix.update()
                
                # Control frame rate
                time.sleep(1.0 / self.config.FRAME_RATE)
                
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean shutdown"""
        print("Cleaning up...")
        self.audio_processor.stop()
        self.led_matrix.clear()
        self.led_matrix.update()
        print("Shutdown complete.")

if __name__ == "__main__":
    app = LEDCubeApp()
    app.run()


# led_controller.py - LED Matrix Management
import board
import neopixel
import numpy as np
import time

class LEDMatrix:
    def __init__(self, pin=18, width=16, height=16, brightness=0.5):
        self.width = width
        self.height = height
        self.brightness = brightness
        
        # Initialize NeoPixel strip
        try:
            self.pixels = neopixel.NeoPixel(
                board.pin.Pin(pin), 
                width * height, 
                brightness=brightness,
                auto_write=False
            )
        except:
            # Fallback for testing without hardware
            print("Warning: NeoPixel hardware not available, using simulation mode")
            self.pixels = None
            
        # Frame buffer - RGB values for each pixel
        self.buffer = np.zeros((height, width, 3), dtype=np.uint8)
        self.prev_buffer = np.zeros((height, width, 3), dtype=np.uint8)
        
    def set_pixel(self, x, y, color):
        """Set individual pixel color (x, y, (r, g, b))"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y, x] = color
            
    def set_pixel_hsv(self, x, y, h, s, v):
        """Set pixel using HSV color space"""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        self.set_pixel(x, y, (int(r * 255), int(g * 255), int(b * 255)))
    
    def fill(self, color):
        """Fill entire matrix with color"""
        self.buffer[:, :] = color
        
    def clear(self):
        """Clear the matrix (set all pixels to black)"""
        self.buffer.fill(0)
        
    def draw_line(self, x0, y0, x1, y1, color):
        """Draw line using Bresenham's algorithm"""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        x, y = x0, y0
        while True:
            self.set_pixel(x, y, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
                
    def draw_circle(self, cx, cy, radius, color, filled=False):
        """Draw circle"""
        for y in range(max(0, cy - radius), min(self.height, cy + radius + 1)):
            for x in range(max(0, cx - radius), min(self.width, cx + radius + 1)):
                dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if filled and dist <= radius:
                    self.set_pixel(x, y, color)
                elif not filled and abs(dist - radius) < 0.7:
                    self.set_pixel(x, y, color)
    
    def adjust_brightness(self, delta):
        """Adjust overall brightness"""
        self.brightness = max(0.1, min(1.0, self.brightness + delta))
        if self.pixels:
            self.pixels.brightness = self.brightness
            
    def apply_gamma_correction(self):
        """Apply gamma correction for better color representation"""
        gamma = 2.2
        self.buffer = np.power(self.buffer / 255.0, 1.0 / gamma) * 255
        self.buffer = self.buffer.astype(np.uint8)
    
    def update(self):
        """Push buffer to physical LEDs"""
        if self.pixels is None:
            return  # Simulation mode
            
        # Only update changed pixels for efficiency
        if not np.array_equal(self.buffer, self.prev_buffer):
            # Convert 2D buffer to 1D pixel array
            for y in range(self.height):
                for x in range(self.width):
                    # Handle zigzag LED strip layout
                    if y % 2 == 0:
                        pixel_index = y * self.width + x
                    else:
                        pixel_index = y * self.width + (self.width - 1 - x)
                    
                    color = tuple(self.buffer[y, x])
                    self.pixels[pixel_index] = color
            
            self.pixels.show()
            self.prev_buffer = self.buffer.copy()


# audio_processor.py - Audio Analysis
import numpy as np
import pyaudio
import threading
from scipy import signal
from collections import deque
import time

class AudioProcessor:
    def __init__(self, sample_rate=44100, chunk_size=1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.running = False
        
        # Audio data buffers
        self.audio_buffer = deque(maxlen=sample_rate // 10)  # 100ms buffer
        self.fft_data = np.zeros(chunk_size // 2)
        self.volume_history = deque(maxlen=30)  # 30 frame history
        
        # Frequency bands for visualization
        self.freq_bands = self._create_frequency_bands()
        self.band_values = np.zeros(len(self.freq_bands))
        
        # Beat detection
        self.beat_threshold = 0.3
        self.last_beat_time = 0
        self.beat_detected = False
        
        # Initialize PyAudio
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = None
        except:
            print("Warning: PyAudio not available, using simulation mode")
            self.audio = None
            
    def _create_frequency_bands(self):
        """Create logarithmic frequency bands for visualization"""
        # Create 16 frequency bands from 20Hz to 20kHz
        min_freq = 20
        max_freq = min(20000, self.sample_rate // 2)
        bands = np.logspace(np.log10(min_freq), np.log10(max_freq), 17)
        return [(bands[i], bands[i+1]) for i in range(16)]
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """PyAudio callback function"""
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        self.audio_buffer.extend(audio_data)
        return (None, pyaudio.paContinue)
    
    def start(self):
        """Start audio processing"""
        if self.audio is None:
            self._simulate_audio()
            return
            
        self.running = True
        
        try:
            self.stream = self.audio.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback
            )
            self.stream.start_stream()
            
            # Processing loop
            while self.running:
                if len(self.audio_buffer) >= self.chunk_size:
                    self._process_audio()
                time.sleep(0.01)  # 100Hz processing rate
                
        except Exception as e:
            print(f"Audio error: {e}")
        finally:
            self.stop()
    
    def _simulate_audio(self):
        """Simulate audio data for testing"""
        self.running = True
        t = 0
        while self.running:
            # Generate fake audio data with beat
            beat_freq = 2.0  # 2 Hz beat
            audio_sim = np.sin(2 * np.pi * 440 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * beat_freq * t))
            
            # Simulate frequency bands
            for i in range(len(self.band_values)):
                self.band_values[i] = abs(np.sin(t * (i + 1) * 0.5)) * 0.8
            
            # Simulate beat detection
            self.beat_detected = np.sin(2 * np.pi * beat_freq * t) > 0.8
            
            t += 0.02  # 50Hz simulation rate
            time.sleep(0.02)
    
    def _process_audio(self):
        """Process audio buffer and extract features"""
        # Get latest audio chunk
        audio_chunk = np.array(list(self.audio_buffer)[-self.chunk_size:])
        
        # Calculate volume (RMS)
        volume = np.sqrt(np.mean(audio_chunk ** 2))
        self.volume_history.append(volume)
        
        # FFT analysis
        windowed = audio_chunk * np.hanning(len(audio_chunk))
        fft = np.fft.fft(windowed)
        self.fft_data = np.abs(fft[:len(fft)//2])
        
        # Extract frequency bands
        freqs = np.fft.fftfreq(self.chunk_size, 1/self.sample_rate)[:self.chunk_size//2]
        
        for i, (low_freq, high_freq) in enumerate(self.freq_bands):
            band_mask = (freqs >= low_freq) & (freqs < high_freq)
            self.band_values[i] = np.mean(self.fft_data[band_mask]) if np.any(band_mask) else 0
        
        # Normalize band values
        max_val = np.max(self.band_values)
        if max_val > 0:
            self.band_values = self.band_values / max_val
        
        # Beat detection
        if len(self.volume_history) > 10:
            recent_avg = np.mean(list(self.volume_history)[-10:])
            historical_avg = np.mean(list(self.volume_history)[:-10])
            
            current_time = time.time()
            if (recent_avg > historical_avg * (1 + self.beat_threshold) and 
                current_time - self.last_beat_time > 0.3):  # Minimum 300ms between beats
                self.beat_detected = True
                self.last_beat_time = current_time
            else:
                self.beat_detected = False
    
    def get_frequency_bands(self):
        """Get current frequency band values (0-1)"""
        return self.band_values.copy()
    
    def get_volume(self):
        """Get current volume level (0-1)"""
        return list(self.volume_history)[-1] if self.volume_history else 0
    
    def is_beat_detected(self):
        """Check if beat was detected"""
        return self.beat_detected
    
    def stop(self):
        """Stop audio processing"""
        self.running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()


# config.py - Configuration Settings
class Config:
    # Hardware Configuration
    MATRIX_WIDTH = 16
    MATRIX_HEIGHT = 16
    LED_PIN = 18
    
    # Audio Configuration
    SAMPLE_RATE = 44100
    CHUNK_SIZE = 1024
    
    # Display Configuration
    FRAME_RATE = 60
    DEFAULT_BRIGHTNESS = 0.5
    
    # Control Configuration
    ROTARY_PINS = {
        'A': 2,
        'B': 3,
        'BUTTON': 4
    }
    
    BUTTON_PINS = {
        'BUTTON1': 17,
        'BUTTON2': 27
    }
    
    # Pattern Configuration
    PATTERN_MODES = ['AUDIO', 'AMBIENT', 'GAMES']
    AUDIO_PATTERNS = ['spectrum', 'waveform', 'circles', 'bars']
    AMBIENT_PATTERNS = ['clock', 'weather', 'matrix_rain', 'fire']