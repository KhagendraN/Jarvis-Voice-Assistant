#!/bin/bash

# Wallpaper Selector Script for Jarvis Voice Assistant
# This script allows users to select and set wallpapers

# Function to set wallpaper using feh (for X11) or swaybg (for Wayland)
set_wallpaper() {
    local wallpaper_path="$1"
    
    if [ ! -f "$wallpaper_path" ]; then
        echo "Error: Wallpaper file not found: $wallpaper_path"
        return 1
    fi

    # Detect display server
    if [ -n "$WAYLAND_DISPLAY" ]; then
        # Wayland - try swaybg first, then wbg
        if command -v swaybg &> /dev/null; then
            pkill swaybg 2>/dev/null
            swaybg -i "$wallpaper_path" -m fill &
            echo "Wallpaper set using swaybg"
        elif command -v wbg &> /dev/null; then
            wbg "$wallpaper_path" &
            echo "Wallpaper set using wbg"
        else
            echo "No Wayland wallpaper setter found. Install swaybg or wbg."
            return 1
        fi
    else
        # X11 - try feh first, then nitrogen
        if command -v feh &> /dev/null; then
            feh --bg-fill "$wallpaper_path"
            echo "Wallpaper set using feh"
        elif command -v nitrogen &> /dev/null; then
            nitrogen --set-zoom-fill "$wallpaper_path"
            echo "Wallpaper set using nitrogen"
        else
            echo "No X11 wallpaper setter found. Install feh or nitrogen."
            return 1
        fi
    fi
}

# Function to select wallpaper using rofi
select_wallpaper() {
    # Wallpaper directories (user can customize these)
    WALLPAPER_DIRS=(
        "$HOME/Pictures/Wallpapers"
        "$HOME/.local/share/wallpapers"
        "/usr/share/wallpapers"
        "/usr/share/backgrounds"
    )

    # Find all wallpaper files
    WALLPAPER_FILES=""
    for dir in "${WALLPAPER_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            WALLPAPER_FILES+=$(find "$dir" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.bmp" -o -name "*.gif" \) 2>/dev/null)
            WALLPAPER_FILES+=$'\n'
        fi
    done

    if [ -z "$WALLPAPER_FILES" ]; then
        echo "No wallpaper files found in common directories."
        echo "Please add wallpapers to one of these directories:"
        printf '%s\n' "${WALLPAPER_DIRS[@]}"
        return 1
    fi

    # Use rofi to select wallpaper
    if command -v rofi &> /dev/null; then
        SELECTED_WALLPAPER=$(echo "$WALLPAPER_FILES" | rofi -dmenu -i -p "Select wallpaper:" -theme-str 'listview { lines: 15; }')
    else
        echo "rofi not found. Please install rofi for wallpaper selection."
        return 1
    fi

    if [ -n "$SELECTED_WALLPAPER" ] && [ -f "$SELECTED_WALLPAPER" ]; then
        set_wallpaper "$SELECTED_WALLPAPER"
        echo "Wallpaper set: $(basename "$SELECTED_WALLPAPER")"
    else
        echo "No wallpaper selected or file not found."
        return 1
    fi
}

# Function to set random wallpaper
set_random_wallpaper() {
    # Wallpaper directories
    WALLPAPER_DIRS=(
        "$HOME/Pictures/Wallpapers"
        "$HOME/.local/share/wallpapers"
        "/usr/share/wallpapers"
        "/usr/share/backgrounds"
    )

    # Find all wallpaper files
    WALLPAPER_FILES=""
    for dir in "${WALLPAPER_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            WALLPAPER_FILES+=$(find "$dir" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.bmp" -o -name "*.gif" \) 2>/dev/null)
            WALLPAPER_FILES+=$'\n'
        fi
    done

    if [ -z "$WALLPAPER_FILES" ]; then
        echo "No wallpaper files found."
        return 1
    fi

    # Select random wallpaper
    RANDOM_WALLPAPER=$(echo "$WALLPAPER_FILES" | shuf -n 1)
    
    if [ -n "$RANDOM_WALLPAPER" ] && [ -f "$RANDOM_WALLPAPER" ]; then
        set_wallpaper "$RANDOM_WALLPAPER"
        echo "Random wallpaper set: $(basename "$RANDOM_WALLPAPER")"
    else
        echo "Failed to set random wallpaper."
        return 1
    fi
}

# Main script logic
case "${1:-select}" in
    "select")
        select_wallpaper
        ;;
    "random")
        set_random_wallpaper
        ;;
    "set")
        if [ -n "$2" ]; then
            set_wallpaper "$2"
        else
            echo "Usage: $0 set <wallpaper_path>"
            exit 1
        fi
        ;;
    *)
        echo "Usage: $0 {select|random|set <path>}"
        echo "  select     - Select wallpaper using rofi"
        echo "  random     - Set random wallpaper"
        echo "  set <path> - Set specific wallpaper"
        exit 1
        ;;
esac 