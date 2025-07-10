#!/bin/bash

# Screenshot Script for Jarvis Voice Assistant
# This script handles taking screenshots using various tools

# Function to take full screenshot
take_full_screenshot() {
    local output_dir="$HOME/Pictures/Screenshots"
    mkdir -p "$output_dir"
    
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local filename="screenshot_full_${timestamp}.png"
    local filepath="$output_dir/$filename"
    
    # Try different screenshot tools
    if command -v grim &> /dev/null && [ -n "$WAYLAND_DISPLAY" ]; then
        # Wayland - use grim
        grim "$filepath"
        echo "Full screenshot saved: $filepath"
    elif command -v maim &> /dev/null; then
        # X11 - use maim
        maim "$filepath"
        echo "Full screenshot saved: $filepath"
    elif command -v scrot &> /dev/null; then
        # X11 - use scrot
        scrot "$filepath"
        echo "Full screenshot saved: $filepath"
    elif command -v gnome-screenshot &> /dev/null; then
        # GNOME screenshot tool
        gnome-screenshot -f "$filepath"
        echo "Full screenshot saved: $filepath"
    else
        echo "No screenshot tool found. Install grim (Wayland) or maim/scrot (X11)."
        return 1
    fi
    
    echo "$filepath"
}

# Function to take area screenshot
take_area_screenshot() {
    local output_dir="$HOME/Pictures/Screenshots"
    mkdir -p "$output_dir"
    
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local filename="screenshot_area_${timestamp}.png"
    local filepath="$output_dir/$filename"
    
    # Try different screenshot tools
    if command -v grim &> /dev/null && command -v slurp &> /dev/null && [ -n "$WAYLAND_DISPLAY" ]; then
        # Wayland - use grim with slurp for area selection
        grim -g "$(slurp)" "$filepath"
        echo "Area screenshot saved: $filepath"
    elif command -v maim &> /dev/null; then
        # X11 - use maim with area selection
        maim -s "$filepath"
        echo "Area screenshot saved: $filepath"
    elif command -v scrot &> /dev/null; then
        # X11 - use scrot with area selection
        scrot -s "$filepath"
        echo "Area screenshot saved: $filepath"
    else
        echo "No area screenshot tool found. Install grim+slurp (Wayland) or maim/scrot (X11)."
        return 1
    fi
    
    echo "$filepath"
}

# Function to take window screenshot
take_window_screenshot() {
    local output_dir="$HOME/Pictures/Screenshots"
    mkdir -p "$output_dir"
    
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local filename="screenshot_window_${timestamp}.png"
    local filepath="$output_dir/$filename"
    
    # Try different screenshot tools
    if command -v grim &> /dev/null && command -v slurp &> /dev/null && [ -n "$WAYLAND_DISPLAY" ]; then
        # Wayland - use grim with slurp for window selection
        grim -g "$(slurp -o)" "$filepath"
        echo "Window screenshot saved: $filepath"
    elif command -v maim &> /dev/null; then
        # X11 - use maim with window selection
        maim -i "$(xdotool getactivewindow)" "$filepath"
        echo "Window screenshot saved: $filepath"
    elif command -v scrot &> /dev/null; then
        # X11 - use scrot with window selection
        scrot -u "$filepath"
        echo "Window screenshot saved: $filepath"
    else
        echo "No window screenshot tool found. Install grim+slurp (Wayland) or maim/scrot (X11)."
        return 1
    fi
    
    echo "$filepath"
}

# Function to take delayed screenshot
take_delayed_screenshot() {
    local delay="${1:-5}"
    local output_dir="$HOME/Pictures/Screenshots"
    mkdir -p "$output_dir"
    
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local filename="screenshot_delayed_${timestamp}.png"
    local filepath="$output_dir/$filename"
    
    echo "Taking screenshot in $delay seconds..."
    sleep "$delay"
    
    # Try different screenshot tools
    if command -v grim &> /dev/null && [ -n "$WAYLAND_DISPLAY" ]; then
        grim "$filepath"
        echo "Delayed screenshot saved: $filepath"
    elif command -v maim &> /dev/null; then
        maim "$filepath"
        echo "Delayed screenshot saved: $filepath"
    elif command -v scrot &> /dev/null; then
        scrot -d "$delay" "$filepath"
        echo "Delayed screenshot saved: $filepath"
    else
        echo "No screenshot tool found. Install grim (Wayland) or maim/scrot (X11)."
        return 1
    fi
    
    echo "$filepath"
}

# Function to open screenshot in default viewer
open_screenshot() {
    local filepath="$1"
    
    if [ -f "$filepath" ]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open "$filepath"
        elif command -v open &> /dev/null; then
            open "$filepath"
        else
            echo "Screenshot saved: $filepath"
        fi
    else
        echo "Screenshot file not found: $filepath"
    fi
}

# Function to copy screenshot to clipboard
copy_to_clipboard() {
    local filepath="$1"
    
    if [ -f "$filepath" ]; then
        if command -v wl-copy &> /dev/null && [ -n "$WAYLAND_DISPLAY" ]; then
            wl-copy < "$filepath"
            echo "Screenshot copied to clipboard"
        elif command -v xclip &> /dev/null; then
            xclip -selection clipboard -t image/png -i "$filepath"
            echo "Screenshot copied to clipboard"
        else
            echo "No clipboard tool found. Install wl-copy (Wayland) or xclip (X11)."
        fi
    else
        echo "Screenshot file not found: $filepath"
    fi
}

# Main script logic
case "${1:-area}" in
    "full")
        filepath=$(take_full_screenshot)
        if [ $? -eq 0 ]; then
            open_screenshot "$filepath"
        fi
        ;;
    "area")
        filepath=$(take_area_screenshot)
        if [ $? -eq 0 ]; then
            open_screenshot "$filepath"
        fi
        ;;
    "window")
        filepath=$(take_window_screenshot)
        if [ $? -eq 0 ]; then
            open_screenshot "$filepath"
        fi
        ;;
    "delayed")
        delay="${2:-5}"
        filepath=$(take_delayed_screenshot "$delay")
        if [ $? -eq 0 ]; then
            open_screenshot "$filepath"
        fi
        ;;
    "copy")
        filepath=$(take_area_screenshot)
        if [ $? -eq 0 ]; then
            copy_to_clipboard "$filepath"
        fi
        ;;
    *)
        echo "Usage: $0 {full|area|window|delayed [seconds]|copy}"
        echo "  full           - Take full screenshot"
        echo "  area           - Take area screenshot (default)"
        echo "  window         - Take active window screenshot"
        echo "  delayed [sec]  - Take delayed screenshot"
        echo "  copy           - Take area screenshot and copy to clipboard"
        exit 1
        ;;
esac 