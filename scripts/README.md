# Scripts Directory

This directory contains bash scripts used by Jarvis Voice Assistant for various system operations.

## Available Scripts

### 1. `music_player.sh`
Handles music playback using rofi and mpv.

**Usage:**
```bash
./scripts/music_player.sh [play|stop|toggle]
```

**Features:**
- Browse and select music files from `~/Music` directory
- Play music using mpv
- Stop currently playing music
- Toggle play/stop

**Dependencies:**
- mpv (media player)
- rofi (application launcher)

### 2. `wallpaper_selector.sh`
Manages wallpaper selection and setting.

**Usage:**
```bash
./scripts/wallpaper_selector.sh [select|random|set <path>]
```

**Features:**
- Select wallpapers using rofi
- Set random wallpaper
- Support for X11 (feh/nitrogen) and Wayland (swaybg/wbg)
- Automatic display server detection

**Dependencies:**
- rofi (for selection)
- feh/nitrogen (X11) or swaybg/wbg (Wayland)

### 3. `screenshot.sh`
Takes screenshots using various tools.

**Usage:**
```bash
./scripts/screenshot.sh [full|area|window|delayed [seconds]|copy]
```

**Features:**
- Full screen, area, and window screenshots
- Delayed screenshots
- Copy to clipboard
- Support for X11 (maim/scrot) and Wayland (grim+slurp)
- Automatic tool detection

**Dependencies:**
- grim+slurp (Wayland) or maim/scrot (X11)
- xclip/wl-copy (for clipboard)

### 4. `volume_control.sh`
Controls system volume.

**Usage:**
```bash
./scripts/volume_control.sh [get|set <volume>|increase [amount]|decrease [amount]|mute|status|notify <volume>]
```

**Features:**
- Get/set volume levels
- Increase/decrease volume
- Mute/unmute
- Support for PulseAudio, ALSA, and PipeWire
- Desktop notifications

**Dependencies:**
- pulseaudio-utils, alsa-utils, or wireplumber

### 5. `brightness_control.sh`
Controls display brightness.

**Usage:**
```bash
./scripts/brightness_control.sh [get|get-percent|set <brightness>|set-percent <percentage>|increase [amount]|decrease [amount]|status|notify <brightness>]
```

**Features:**
- Get/set brightness levels
- Percentage-based control
- Support for various backlight systems (Intel, NVIDIA, AMD, ACPI)
- Desktop notifications

**Dependencies:**
- brightnessctl (optional)
- sudo access for backlight control

## Installation

### 1. Make Scripts Executable
```bash
chmod +x scripts/*.sh
```

### 2. Install Dependencies

**For Arch Linux:**
```bash
sudo pacman -S mpv rofi grim slurp maim scrot xclip brightnessctl
```

**For Ubuntu/Debian:**
```bash
sudo apt install mpv rofi grim slurp maim scrot xclip brightnessctl
```

### 3. Configure Scripts

Update the script paths in `main.py` and `utils.py` to use relative paths:

```python
# Example script paths
MUSIC_SCRIPT = "scripts/music_player.sh"
WALLPAPER_SCRIPT = "scripts/wallpaper_selector.sh"
SCREENSHOT_SCRIPT = "scripts/screenshot.sh"
VOLUME_SCRIPT = "scripts/volume_control.sh"
BRIGHTNESS_SCRIPT = "scripts/brightness_control.sh"
```

## Customization

### Music Directory
Edit `music_player.sh` to change the music directory:
```bash
MUSIC_DIR="$HOME/Music"  # Change this line
```

### Wallpaper Directories
Edit `wallpaper_selector.sh` to add/remove wallpaper directories:
```bash
WALLPAPER_DIRS=(
    "$HOME/Pictures/Wallpapers"
    "$HOME/.local/share/wallpapers"
    "/usr/share/wallpapers"
    "/usr/share/backgrounds"
)
```

### Screenshot Directory
Edit `screenshot.sh` to change the screenshot save location:
```bash
local output_dir="$HOME/Pictures/Screenshots"  # Change this line
```

## Troubleshooting

### Permission Denied
```bash
chmod +x scripts/*.sh
```

### Script Not Found
Ensure the script paths in your Python code are correct and relative to the project root.

### Dependencies Missing
Install the required packages for your distribution (see Installation section).

### Audio/Video Issues
- Check if your audio/video system is properly configured
- Ensure the required tools are installed and working
- Test the scripts manually before using them with Jarvis

## Adding New Scripts

To add a new script:

1. Create the script in the `scripts/` directory
2. Make it executable: `chmod +x scripts/your_script.sh`
3. Add usage documentation to this README
4. Update the Python code to use the new script
5. Test thoroughly

## Security Notes

- Some scripts require sudo access (brightness control)
- Be careful with scripts that modify system settings
- Test scripts in a safe environment first
- Consider user permissions and security implications 