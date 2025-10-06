# 🎵 Binaural Beats Screen Flasher

A Python-based GUI application that synchronizes fullscreen visual flashing with binaural beats audio frequencies. The app can automatically detect binaural beat frequencies in real-time or flash at a user-defined static frequency.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 🎧 **Audio Playback**: Plays your binaural beats audio while flashing
- 🔄 **Auto-Detection Mode**: Automatically detects binaural frequency from stereo audio and adjusts flashing dynamically
- 🎯 **Manual Mode**: Set a static frequency (0.5-40 Hz) for consistent flashing
- 🖥️ **Fullscreen Experience**: Pure white/black flashing covers entire screen
- ⌨️ **ESC Key Control**: Quick exit from fullscreen mode
- 📊 **Real-time Frequency Display**: See current frequency being used
- 🎨 **User-Friendly Interface**: Clean, modern GUI with status updates

## 🎬 How It Works

### Auto-Detect Mode
1. Analyzes stereo audio in 2-second chunks
2. Detects binaural frequency by examining the difference between left and right channels
3. Dynamically adjusts screen flash rate as frequency changes
4. Example: If audio has 10Hz for 30 minutes then switches to 4Hz, the flashing automatically adjusts

### Manual Mode
1. User sets desired frequency (0.5-40 Hz)
2. Screen flashes at that exact rate throughout audio playback
3. Perfect for testing specific frequencies or using with mono audio

## 📋 Prerequisites

- Python 3.7 or higher
- Audio file in supported format (WAV, MP3, OGG, FLAC)
- For auto-detection: **Stereo audio file** with binaural beats

## 🚀 Installation

### Step 1: Clone or Download

```bash
git clone https://github.com/Shivamsharda/SLEB.git
cd binaural-beats-flasher
```

### Step 2: Install Dependencies

```bash
pip install numpy librosa soundfile scipy pygame
```

Or use requirements.txt:

```bash
pip install -r requirements.txt
```

### Requirements File Contents
Create a `requirements.txt` file with:
```
numpy>=1.20.0
librosa>=0.9.0
soundfile>=0.10.0
scipy>=1.7.0
pygame>=2.0.0
```

## 💻 Usage

### Running the Application

```bash
python binaural_flasher.py
```

### Auto-Detect Mode (Recommended for Binaural Beats)

1. **Select Mode**: Choose "Auto-Detect Frequency" (default)
2. **Load Audio**: Click "Browse Audio File" and select your stereo binaural beats file
3. **Start**: Click the "▶ Start" button
4. **Experience**: Main window hides, fullscreen flashing begins with audio playback
5. **Stop**: Press **ESC** key anytime to return to control panel

**Note**: Auto-detect mode requires **stereo audio** files with actual binaural beats (different frequencies in left/right channels).

### Manual Mode (Static Frequency)

1. **Select Mode**: Choose "Manual Frequency"
2. **Set Frequency**: Enter desired frequency in Hz (0.5 - 40)
   - **Delta waves**: 0.5-4 Hz (deep sleep)
   - **Theta waves**: 4-8 Hz (meditation)
   - **Alpha waves**: 8-13 Hz (relaxation)
   - **Beta waves**: 13-30 Hz (focus)
   - **Gamma waves**: 30-40 Hz (cognitive enhancement)
3. **Load Audio**: Select any audio file (can be mono or stereo)
4. **Start**: Click "▶ Start"
5. **Stop**: Press **ESC** key to exit

## 🎯 Use Cases

- **Meditation & Relaxation**: Use theta/alpha frequencies for deep relaxation
- **Focus & Study**: Beta frequencies for enhanced concentration
- **Sleep Aid**: Delta frequencies for better sleep
- **Brainwave Entrainment**: Synchronize visual and auditory stimuli
- **Research**: Test effects of different frequencies

## ⚠️ Important Notes

### Health & Safety

- **Photosensitive Epilepsy Warning**: This application uses rapid screen flashing that may trigger seizures in people with photosensitive epilepsy. Do NOT use if you have epilepsy or are sensitive to flashing lights.
- **Start Slow**: Begin with lower frequencies and shorter sessions
- **Take Breaks**: Do not use for extended periods without rest
- **Consult Healthcare Provider**: If you have any medical conditions, consult a doctor before use

### Technical Notes

- **Stereo Required for Auto-Detection**: Auto-detect mode needs stereo audio with genuine binaural beats
- **Frequency Range**: Limited to 0.5-40 Hz for safety and effectiveness
- **Screen Refresh**: Flashing accuracy depends on your monitor's refresh rate
- **Audio Formats**: Supports WAV, MP3, OGG, and FLAC files

## 🔧 Troubleshooting

### "Audio file is mono" Warning
**Solution**: Use Manual Mode or convert audio to stereo with actual binaural beats in left/right channels

### Audio Not Playing
**Solution**: 
- Ensure pygame mixer is properly installed: `pip install --upgrade pygame`
- Check that audio file format is supported
- Verify audio file is not corrupted

### Flashing Seems Irregular
**Solution**:
- Lower frequencies (< 2 Hz) may appear irregular due to long periods
- Ensure system isn't under heavy load
- Close other applications using significant resources

### ESC Key Not Working
**Solution**:
- Click on the fullscreen window to ensure it has focus
- Wait for application to fully load before pressing ESC
- If stuck, use Alt+Tab (Windows/Linux) or Cmd+Tab (Mac) to switch windows

## 📊 Technical Details

### Frequency Detection Algorithm
- Uses Fast Fourier Transform (FFT) on channel difference signal
- Analyzes 2-second audio chunks for real-time detection
- Focuses on 0.5-40 Hz range (binaural beats frequency spectrum)
- Identifies peak frequency in the spectrum

### Flashing Mechanism
- Calculates period from frequency: `period = 1/frequency`
- Alternates between white and black at half-period intervals
- Uses threading for smooth audio playback and visual rendering
- Fullscreen tkinter window for distraction-free experience

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.


## ⚖️ Disclaimer

This software is provided for educational and experimental purposes only. The developers are not responsible for any adverse effects, including but not limited to seizures, headaches, or discomfort. Use at your own risk and always consult with healthcare professionals before using brainwave entrainment technologies.

## 🙏 Acknowledgments

- Built with Python, Tkinter, Pygame, Librosa, and NumPy
- Inspired by binaural beats research and brainwave entrainment studies
- Thanks to the open-source community



**Remember**: Press **ESC** to stop fullscreen flashing at any time! 🛑

Made with ❤️ for binaural beats enthusiasts
