#!/bin/bash

echo "Motion-Based-Game-Control Build Script"
echo "======================================"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Detected Python version: $PYTHON_VERSION"

# Check if Python version is 3.13
if [[ $PYTHON_VERSION == 3.13.* ]]; then
    echo ""
    echo "WARNING: Python 3.13 detected!"
    echo "MediaPipe does not currently support Python 3.13."
    echo ""
    echo "To run this project, you need:"
    echo "1. Python 3.8, 3.9, 3.10, 3.11, or 3.12"
    echo "2. Install dependencies with: pip install -r requirements.txt"
    echo ""
    echo "Alternatively, you can use a virtual environment with a compatible Python version."
    echo ""
    echo "Installed other dependencies (without MediaPipe):"
    pip list | grep -E "opencv-python|pynput|pygame|PyQt5|vgamepad"
else
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "Build successful!"
        echo ""
        echo "To run the project:"
        echo "1. Main gesture control: python3 src/__init__.py"
        echo "2. Keyboard mapper test: python3 src/mapper.py"
        echo "3. Integrator: python3 src/integrator.py"
        echo ""
        echo "Make sure to have a webcam connected for gesture recognition."
    else
        echo "Build failed! Please check the error messages above."
    fi
fi