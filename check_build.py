#!/usr/bin/env python3
"""
Build checker and setup script for Motion-Based-Game-Control
"""

import sys
import subprocess
import importlib

def check_python_version():
    """Check if Python version is compatible with MediaPipe"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 13:
        return False, "Python 3.13+ is not supported by MediaPipe"
    elif version.major == 3 and version.minor >= 8:
        return True, "Python version is compatible"
    else:
        return False, "Python 3.8 or higher (but less than 3.13) is required"

def check_installed_packages():
    """Check which required packages are installed"""
    required_packages = {
        'cv2': ('opencv-python', 'OpenCV for video processing'),
        'mediapipe': ('mediapipe', 'MediaPipe for pose detection'),
        'pynput': ('pynput', 'PyInput for keyboard/mouse control'),
        'pygame': ('pygame', 'Pygame for game integration'),
        'PyQt5': ('PyQt5', 'PyQt5 for GUI (optional)'),
        'vgamepad': ('vgamepad', 'Virtual gamepad support')
    }
    
    installed = []
    missing = []
    
    for module_name, (package_name, description) in required_packages.items():
        try:
            importlib.import_module(module_name)
            installed.append(f"✓ {package_name}: {description}")
        except ImportError:
            missing.append(f"✗ {package_name}: {description}")
    
    return installed, missing

def main():
    print("=" * 60)
    print("Motion-Based-Game-Control Build Check")
    print("=" * 60)
    print()
    
    # Check Python version
    compatible, message = check_python_version()
    if compatible:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")
        print("\nMediaPipe Installation Issue:")
        print("-" * 30)
        print("MediaPipe is essential for this project as it provides")
        print("human pose detection capabilities.")
        print()
        print("Solutions:")
        print("1. Use Python 3.8, 3.9, 3.10, 3.11, or 3.12")
        print("2. Create a virtual environment with a compatible Python version:")
        print("   - Install pyenv or use conda")
        print("   - Create environment with Python 3.11:")
        print("     conda create -n motion-game python=3.11")
        print("     conda activate motion-game")
        print("   - Then run: pip install -r requirements.txt")
        print()
    
    # Check installed packages
    print("\nPackage Status:")
    print("-" * 30)
    installed, missing = check_installed_packages()
    
    for item in installed:
        print(item)
    
    for item in missing:
        print(item)
    
    print()
    print("Project Structure:")
    print("-" * 30)
    print("• src/__init__.py - Main gesture recognition and control")
    print("• src/integrator.py - Translates gestures to keyboard inputs")
    print("• src/mapper.py - Manual command mapping for testing")
    print("• src/actions/ - Individual action implementations")
    print("• src/util.py - Utility functions")
    
    print()
    print("Usage (once all dependencies are installed):")
    print("-" * 30)
    print("1. Run the main application:")
    print("   python3 src/__init__.py")
    print()
    print("2. The app will:")
    print("   - Open your webcam")
    print("   - Detect body poses using MediaPipe")
    print("   - Translate gestures to game controls")
    print("   - Send keyboard inputs to control games")
    
    if not compatible:
        print()
        print("⚠️  Cannot proceed with full build due to Python version incompatibility")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())