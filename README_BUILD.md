# Build Instructions for Motion-Based-Game-Control

## Current Build Status

This project requires **MediaPipe** for pose detection, which is not compatible with Python 3.13 (current version in this environment).

### Requirements

1. **Python Version**: 3.8, 3.9, 3.10, 3.11, or 3.12 (MediaPipe doesn't support 3.13 yet)
2. **Webcam**: Required for gesture recognition
3. **Dependencies**:
   - opencv-python
   - mediapipe==0.10.9
   - pynput
   - pygame
   - PyQt5
   - vgamepad

### Build Options

#### Option 1: Use a Compatible Python Version

```bash
# Using conda
conda create -n motion-game python=3.11
conda activate motion-game
pip install -r requirements.txt
```

```bash
# Using pyenv
pyenv install 3.11.8
pyenv local 3.11.8
pip install -r requirements.txt
```

#### Option 2: Use Docker (Recommended)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libevdev2 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

CMD ["python", "src/__init__.py"]
```

Build and run:
```bash
docker build -t motion-game .
docker run -it --device=/dev/video0 motion-game
```

### Project Structure

- `src/__init__.py` - Main gesture recognition application
- `src/integrator.py` - Translates gestures to keyboard inputs
- `src/mapper.py` - Manual command mapper for testing
- `src/actions/` - Individual action implementations (dodge, jump, attack, move, turn)
- `src/util.py` - Utility functions for angle calculations

### Running the Application

Once dependencies are installed with a compatible Python version:

1. **Main Application** (requires webcam):
   ```bash
   python src/__init__.py
   ```
   This will:
   - Open your webcam
   - Detect body poses using MediaPipe
   - Translate gestures to game controls
   - Write actions to `command_flag.txt`

2. **Integrator** (reads actions and sends keyboard inputs):
   ```bash
   python src/integrator.py
   ```

3. **Manual Testing**:
   ```bash
   python src/mapper.py
   ```

### Gesture Controls

The application recognizes:
- **Attack**: Arm movements (left/right)
- **Movement**: Leg angles for walking/running
- **Jump**: Hip position changes
- **Dodge**: Shoulder position shifts
- **Turn**: Head/shoulder orientation

### Currently Installed (without MediaPipe)

✅ opencv-python
✅ pynput
✅ pygame
✅ PyQt5
✅ vgamepad
❌ mediapipe (requires Python < 3.13)

### Troubleshooting

If you encounter `libevdev.so.2` errors on Linux:
```bash
sudo apt-get install libevdev2
```

For other issues, ensure:
1. Webcam permissions are granted
2. Display is available for OpenCV windows
3. Correct Python version is being used