#!/bin/bash

# Music Player Script for Jarvis Voice Assistant
# This script handles music playback using rofi and mpv

# Function to play music using rofi
play_music() {
    # Check if mpv is installed
    if ! command -v mpv &> /dev/null; then
        echo "mpv is not installed. Please install it first."
        exit 1
    fi

    # Check if rofi is installed
    if ! command -v rofi &> /dev/null; then
        echo "rofi is not installed. Please install it first."
        exit 1
    fi

    # Music directory (user can customize this)
    MUSIC_DIR="$HOME/Music"
    
    # Create music directory if it doesn't exist
    if [ ! -d "$MUSIC_DIR" ]; then
        mkdir -p "$MUSIC_DIR"
        echo "Created music directory: $MUSIC_DIR"
        echo "Please add your music files to this directory."
        exit 0
    fi

    # Find all music files
    MUSIC_FILES=$(find "$MUSIC_DIR" -type f \( -name "*.mp3" -o -name "*.flac" -o -name "*.wav" -o -name "*.m4a" -o -name "*.ogg" \) 2>/dev/null)

    if [ -z "$MUSIC_FILES" ]; then
        echo "No music files found in $MUSIC_DIR"
        echo "Please add music files to this directory."
        exit 1
    fi

    # Use rofi to select music file
    SELECTED_FILE=$(echo "$MUSIC_FILES" | rofi -dmenu -i -p "Select music:" -theme-str 'listview { lines: 10; }')

    if [ -n "$SELECTED_FILE" ] && [ -f "$SELECTED_FILE" ]; then
        # Kill any existing mpv process
        pkill -f "mpv.*$SELECTED_FILE" 2>/dev/null
        
        # Play the selected file
        mpv "$SELECTED_FILE" &
        echo "Playing: $(basename "$SELECTED_FILE")"
    else
        echo "No file selected or file not found."
    fi
}

# Function to stop music
stop_music() {
    # Kill all mpv processes
    pkill mpv 2>/dev/null
    echo "Music stopped."
}

# Main script logic
case "${1:-play}" in
    "play")
        play_music
        ;;
    "stop")
        stop_music
        ;;
    "toggle")
        if pgrep mpv > /dev/null; then
            stop_music
        else
            play_music
        fi
        ;;
    *)
        echo "Usage: $0 {play|stop|toggle}"
        echo "  play   - Start music player"
        echo "  stop   - Stop music"
        echo "  toggle - Toggle music on/off"
        exit 1
        ;;
esac 