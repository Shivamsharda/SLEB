import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
import threading
import time
import pygame
import librosa
import soundfile as sf
from scipy.fft import fft, fftfreq

class BinauralBeatsFlasher:
    def __init__(self, root):
        self.root = root
        self.root.title("Binaural Beats Screen Flasher")
        self.root.geometry("800x600")
        
        self.audio_file = None
        self.is_playing = False
        self.flash_thread = None
        self.audio_thread = None
        self.current_frequency = 0
        self.flash_window = None
        self.mode = "auto"  # "auto" or "manual"
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Control Frame
        control_frame = tk.Frame(self.root, bg="#2c3e50", padx=20, pady=20)
        control_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(control_frame, text="Binaural Beats Screen Flasher", 
                               font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=10)
        
        # Mode Selection
        mode_frame = tk.Frame(control_frame, bg="#2c3e50")
        mode_frame.pack(pady=15)
        
        mode_label = tk.Label(mode_frame, text="Mode:", 
                             font=("Arial", 12, "bold"), bg="#2c3e50", fg="white")
        mode_label.pack(side=tk.LEFT, padx=5)
        
        self.mode_var = tk.StringVar(value="auto")
        
        auto_radio = tk.Radiobutton(mode_frame, text="Auto-Detect Frequency", 
                                    variable=self.mode_var, value="auto",
                                    font=("Arial", 11), bg="#2c3e50", fg="white",
                                    selectcolor="#34495e", activebackground="#2c3e50",
                                    command=self.mode_changed)
        auto_radio.pack(side=tk.LEFT, padx=10)
        
        manual_radio = tk.Radiobutton(mode_frame, text="Manual Frequency", 
                                      variable=self.mode_var, value="manual",
                                      font=("Arial", 11), bg="#2c3e50", fg="white",
                                      selectcolor="#34495e", activebackground="#2c3e50",
                                      command=self.mode_changed)
        manual_radio.pack(side=tk.LEFT, padx=10)
        
        # Manual frequency input
        self.manual_frame = tk.Frame(control_frame, bg="#2c3e50")
        self.manual_frame.pack(pady=10)
        
        manual_label = tk.Label(self.manual_frame, text="Frequency (Hz):", 
                               font=("Arial", 11), bg="#2c3e50", fg="white")
        manual_label.pack(side=tk.LEFT, padx=5)
        
        self.freq_entry = tk.Entry(self.manual_frame, font=("Arial", 11), width=10)
        self.freq_entry.insert(0, "10")
        self.freq_entry.pack(side=tk.LEFT, padx=5)
        self.freq_entry.config(state=tk.DISABLED)
        
        freq_info = tk.Label(self.manual_frame, text="(0.5 - 40 Hz)", 
                            font=("Arial", 9), bg="#2c3e50", fg="#95a5a6")
        freq_info.pack(side=tk.LEFT, padx=5)
        
        # File selection
        file_frame = tk.Frame(control_frame, bg="#2c3e50")
        file_frame.pack(pady=15)
        
        self.file_label = tk.Label(file_frame, text="No file selected", 
                                   font=("Arial", 10), bg="#2c3e50", fg="white")
        self.file_label.pack(side=tk.LEFT, padx=10)
        
        browse_btn = tk.Button(file_frame, text="Browse Audio File", 
                              command=self.browse_file, 
                              font=("Arial", 11), bg="#3498db", fg="white",
                              padx=20, pady=5, cursor="hand2")
        browse_btn.pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = tk.Frame(control_frame, bg="#2c3e50")
        button_frame.pack(pady=20)
        
        self.start_btn = tk.Button(button_frame, text="▶ Start", 
                                   command=self.start_flashing,
                                   font=("Arial", 14, "bold"), 
                                   bg="#27ae60", fg="white",
                                   padx=40, pady=12, state=tk.DISABLED,
                                   cursor="hand2")
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # Info Frame
        info_frame = tk.Frame(control_frame, bg="#34495e", relief=tk.RIDGE, bd=2)
        info_frame.pack(pady=20, padx=20, fill=tk.X)
        
        self.freq_label = tk.Label(info_frame, text="Current Frequency: 0 Hz", 
                                   font=("Arial", 13, "bold"), bg="#34495e", fg="#ecf0f1")
        self.freq_label.pack(pady=10)
        
        self.status_label = tk.Label(info_frame, text="Status: Ready", 
                                     font=("Arial", 11), bg="#34495e", fg="#95a5a6")
        self.status_label.pack(pady=5)
        
        # Instructions
        inst_frame = tk.Frame(control_frame, bg="#2c3e50")
        inst_frame.pack(pady=15)
        
        inst_label = tk.Label(inst_frame, 
                             text="Press ESC to stop fullscreen flashing", 
                             font=("Arial", 10, "italic"), 
                             bg="#2c3e50", fg="#e74c3c")
        inst_label.pack()
        
    def mode_changed(self):
        if self.mode_var.get() == "manual":
            self.freq_entry.config(state=tk.NORMAL)
        else:
            self.freq_entry.config(state=tk.DISABLED)
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio Files", "*.wav *.mp3 *.ogg *.flac"), ("All Files", "*.*")]
        )
        if filename:
            self.audio_file = filename
            self.file_label.config(text=f"File: {filename.split('/')[-1]}")
            self.start_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Audio file loaded")
    
    def detect_binaural_frequency(self, audio_data, sr):
        """
        Detect binaural beat frequency from stereo audio by analyzing
        the difference between left and right channels
        """
        try:
            # If mono, return 0
            if len(audio_data.shape) == 1:
                return 0
            
            # Get left and right channels
            left = audio_data[:, 0]
            right = audio_data[:, 1]
            
            # Calculate the difference (binaural beat signal)
            diff = left - right
            
            # Apply FFT to the difference signal
            n = len(diff)
            fft_vals = np.abs(fft(diff))
            freqs = fftfreq(n, 1/sr)
            
            # Focus on positive frequencies in the binaural range (0.5-40 Hz)
            pos_mask = (freqs > 0.5) & (freqs < 40)
            pos_freqs = freqs[pos_mask]
            pos_fft = fft_vals[pos_mask]
            
            if len(pos_fft) == 0:
                return 0
            
            # Find peak frequency
            peak_idx = np.argmax(pos_fft)
            detected_freq = pos_freqs[peak_idx]
            
            return float(detected_freq)
        except Exception as e:
            print(f"Error detecting frequency: {e}")
            return 0
    
    def create_flash_window(self):
        """Create fullscreen flash window"""
        self.flash_window = tk.Toplevel()
        self.flash_window.attributes('-fullscreen', True)
        self.flash_window.configure(bg='black')
        self.flash_window.attributes('-topmost', True)
        
        # Bind ESC key to stop
        self.flash_window.bind('<Escape>', lambda e: self.stop_flashing())
        self.flash_window.focus_set()
        
    def flash_screen(self, frequency):
        """Flash the screen at the given frequency"""
        if frequency <= 0 or frequency > 50:
            return
        
        period = 1.0 / frequency
        half_period = period / 2
        
        while self.is_playing and self.flash_window:
            try:
                # Flash white
                self.flash_window.configure(bg="white")
                time.sleep(half_period)
                
                # Flash black
                self.flash_window.configure(bg="black")
                time.sleep(half_period)
            except:
                break
    
    def play_audio(self):
        """Play the audio file"""
        try:
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()
            
            # Wait for audio to finish or stop
            while pygame.mixer.music.get_busy() and self.is_playing:
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def process_audio_and_flash(self):
        """Main processing loop for auto mode"""
        try:
            # Load audio file
            self.status_label.config(text="Status: Loading audio...")
            audio_data, sr = librosa.load(self.audio_file, sr=None, mono=False)
            
            # If mono, convert to stereo (though binaural beats need stereo)
            if len(audio_data.shape) == 1:
                messagebox.showwarning("Warning", 
                    "Audio file is mono. Binaural beats require stereo audio.\n"
                    "Using manual frequency mode instead.")
                self.stop_flashing()
                return
            
            # Transpose if needed
            if audio_data.shape[0] == 2:
                audio_data = audio_data.T
            
            self.status_label.config(text="Status: Processing...")
            
            # Create flash window
            self.create_flash_window()
            
            # Start audio playback in separate thread
            self.audio_thread = threading.Thread(target=self.play_audio, daemon=True)
            self.audio_thread.start()
            
            # Process in chunks
            chunk_duration = 2.0  # Analyze every 2 seconds
            chunk_size = int(sr * chunk_duration)
            total_samples = audio_data.shape[0]
            
            current_sample = 0
            flash_thread = None
            
            while self.is_playing and current_sample < total_samples:
                # Get chunk
                end_sample = min(current_sample + chunk_size, total_samples)
                chunk = audio_data[current_sample:end_sample]
                
                # Detect frequency
                detected_freq = self.detect_binaural_frequency(chunk, sr)
                
                # Round to 1 decimal place
                detected_freq = round(detected_freq, 1)
                
                # Update UI
                self.freq_label.config(text=f"Current Frequency: {detected_freq} Hz")
                
                # If frequency changed significantly, restart flashing
                if abs(detected_freq - self.current_frequency) > 0.5:
                    self.current_frequency = detected_freq
                    
                    # Stop old flash thread
                    if flash_thread and flash_thread.is_alive():
                        old_playing = self.is_playing
                        self.is_playing = False
                        time.sleep(0.1)
                        if flash_thread.is_alive():
                            pass  # Thread will exit on next iteration
                        self.is_playing = old_playing
                    
                    # Start new flash thread with new frequency
                    if self.current_frequency > 0 and self.is_playing:
                        flash_thread = threading.Thread(
                            target=self.flash_screen, 
                            args=(self.current_frequency,),
                            daemon=True
                        )
                        flash_thread.start()
                
                # Move to next chunk
                current_sample = end_sample
                
                # Sleep for chunk duration
                time.sleep(chunk_duration)
            
            # Finished
            if self.is_playing:
                self.status_label.config(text="Status: Playback complete")
                self.stop_flashing()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error processing audio: {str(e)}")
            self.stop_flashing()
    
    def manual_flash_mode(self):
        """Manual frequency flashing mode"""
        try:
            # Get manual frequency
            try:
                manual_freq = float(self.freq_entry.get())
                if manual_freq < 0.5 or manual_freq > 40:
                    messagebox.showerror("Invalid Frequency", 
                        "Please enter a frequency between 0.5 and 40 Hz")
                    self.stop_flashing()
                    return
            except ValueError:
                messagebox.showerror("Invalid Input", 
                    "Please enter a valid number for frequency")
                self.stop_flashing()
                return
            
            self.current_frequency = manual_freq
            self.freq_label.config(text=f"Current Frequency: {manual_freq} Hz")
            self.status_label.config(text="Status: Playing with manual frequency")
            
            # Create flash window
            self.create_flash_window()
            
            # Start audio playback in separate thread
            self.audio_thread = threading.Thread(target=self.play_audio, daemon=True)
            self.audio_thread.start()
            
            # Start flashing at manual frequency
            self.flash_screen(manual_freq)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error in manual mode: {str(e)}")
            self.stop_flashing()
    
    def start_flashing(self):
        if not self.audio_file:
            messagebox.showwarning("No File", "Please select an audio file first.")
            return
        
        self.is_playing = True
        self.start_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Running...")
        
        # Hide main window
        self.root.withdraw()
        
        # Start processing based on mode
        if self.mode_var.get() == "auto":
            self.flash_thread = threading.Thread(target=self.process_audio_and_flash, daemon=True)
        else:
            self.flash_thread = threading.Thread(target=self.manual_flash_mode, daemon=True)
        
        self.flash_thread.start()
    
    def stop_flashing(self):
        self.is_playing = False
        self.current_frequency = 0
        
        # Stop audio
        try:
            pygame.mixer.music.stop()
        except:
            pass
        
        # Close flash window
        if self.flash_window:
            try:
                self.flash_window.destroy()
            except:
                pass
            self.flash_window = None
        
        # Show main window
        self.root.deiconify()
        
        self.start_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Stopped")
        self.freq_label.config(text="Current Frequency: 0 Hz")

if __name__ == "__main__":
    root = tk.Tk()
    app = BinauralBeatsFlasher(root)
    root.mainloop()
