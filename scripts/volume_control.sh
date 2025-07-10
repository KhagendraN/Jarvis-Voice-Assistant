#!/bin/bash

# Volume Control Script for Jarvis Voice Assistant
# This script handles volume control using various audio systems

# Function to get current volume
get_volume() {
    if command -v pactl &> /dev/null; then
        # PulseAudio
        pactl get-sink-volume @DEFAULT_SINK@ | grep -o '[0-9]*%' | head -1 | sed 's/%//'
    elif command -v amixer &> /dev/null; then
        # ALSA
        amixer get Master | grep -o '[0-9]*%' | head -1 | sed 's/%//'
    elif command -v wpctl &> /dev/null; then
        # PipeWire
        wpctl get-volume @DEFAULT_AUDIO_SINK@ | grep -o '[0-9]*' | head -1
    else
        echo "No volume control tool found. Install pulseaudio-utils, alsa-utils, or wireplumber."
        return 1
    fi
}

# Function to set volume
set_volume() {
    local volume="$1"
    
    # Ensure volume is between 0 and 100
    if [ "$volume" -lt 0 ]; then
        volume=0
    elif [ "$volume" -gt 100 ]; then
        volume=100
    fi
    
    if command -v pactl &> /dev/null; then
        # PulseAudio
        pactl set-sink-volume @DEFAULT_SINK@ "$volume%"
    elif command -v amixer &> /dev/null; then
        # ALSA
        amixer set Master "$volume%"
    elif command -v wpctl &> /dev/null; then
        # PipeWire
        wpctl set-volume @DEFAULT_AUDIO_SINK@ "$volume"
    else
        echo "No volume control tool found. Install pulseaudio-utils, alsa-utils, or wireplumber."
        return 1
    fi
    
    echo "Volume set to $volume%"
}

# Function to increase volume
increase_volume() {
    local increment="${1:-5}"
    local current_volume=$(get_volume)
    
    if [ $? -eq 0 ]; then
        local new_volume=$((current_volume + increment))
        set_volume "$new_volume"
    else
        echo "Failed to get current volume"
        return 1
    fi
}

# Function to decrease volume
decrease_volume() {
    local decrement="${1:-5}"
    local current_volume=$(get_volume)
    
    if [ $? -eq 0 ]; then
        local new_volume=$((current_volume - decrement))
        set_volume "$new_volume"
    else
        echo "Failed to get current volume"
        return 1
    fi
}

# Function to mute/unmute
toggle_mute() {
    if command -v pactl &> /dev/null; then
        # PulseAudio
        pactl set-sink-mute @DEFAULT_SINK@ toggle
        local muted=$(pactl get-sink-mute @DEFAULT_SINK@ | grep -o 'yes\|no')
        if [ "$muted" = "yes" ]; then
            echo "Audio muted"
        else
            echo "Audio unmuted"
        fi
    elif command -v amixer &> /dev/null; then
        # ALSA
        amixer set Master toggle
        local muted=$(amixer get Master | grep -o '\[off\]\|\[on\]')
        if [ "$muted" = "[off]" ]; then
            echo "Audio muted"
        else
            echo "Audio unmuted"
        fi
    elif command -v wpctl &> /dev/null; then
        # PipeWire
        wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
        local muted=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | grep -o 'MUTED\|UNMUTED')
        if [ "$muted" = "MUTED" ]; then
            echo "Audio muted"
        else
            echo "Audio unmuted"
        fi
    else
        echo "No volume control tool found. Install pulseaudio-utils, alsa-utils, or wireplumber."
        return 1
    fi
}

# Function to get mute status
get_mute_status() {
    if command -v pactl &> /dev/null; then
        # PulseAudio
        pactl get-sink-mute @DEFAULT_SINK@ | grep -o 'yes\|no'
    elif command -v amixer &> /dev/null; then
        # ALSA
        amixer get Master | grep -o '\[off\]\|\[on\]' | sed 's/\[//;s/\]//'
    elif command -v wpctl &> /dev/null; then
        # PipeWire
        wpctl get-volume @DEFAULT_AUDIO_SINK@ | grep -o 'MUTED\|UNMUTED' | tr '[:upper:]' '[:lower:]'
    else
        echo "No volume control tool found. Install pulseaudio-utils, alsa-utils, or wireplumber."
        return 1
    fi
}

# Function to show volume status
show_status() {
    local current_volume=$(get_volume)
    local mute_status=$(get_mute_status)
    
    if [ $? -eq 0 ] && [ $? -eq 0 ]; then
        if [ "$mute_status" = "yes" ] || [ "$mute_status" = "off" ] || [ "$mute_status" = "muted" ]; then
            echo "Volume: $current_volume% (MUTED)"
        else
            echo "Volume: $current_volume%"
        fi
    else
        echo "Failed to get volume status"
        return 1
    fi
}

# Function to set volume with notification
set_volume_with_notify() {
    local volume="$1"
    set_volume "$volume"
    
    # Show notification if available
    if command -v notify-send &> /dev/null; then
        notify-send "Volume Control" "Volume set to $volume%" -t 1000
    fi
}

# Main script logic
case "${1:-status}" in
    "get")
        get_volume
        ;;
    "set")
        if [ -n "$2" ]; then
            set_volume "$2"
        else
            echo "Usage: $0 set <volume>"
            exit 1
        fi
        ;;
    "increase"|"up")
        increment="${2:-5}"
        increase_volume "$increment"
        ;;
    "decrease"|"down")
        decrement="${2:-5}"
        decrease_volume "$decrement"
        ;;
    "mute"|"toggle")
        toggle_mute
        ;;
    "status")
        show_status
        ;;
    "notify")
        if [ -n "$2" ]; then
            set_volume_with_notify "$2"
        else
            echo "Usage: $0 notify <volume>"
            exit 1
        fi
        ;;
    *)
        echo "Usage: $0 {get|set <volume>|increase [amount]|decrease [amount]|mute|status|notify <volume>}"
        echo "  get                    - Get current volume"
        echo "  set <volume>           - Set volume to specific value (0-100)"
        echo "  increase [amount]      - Increase volume by amount (default: 5)"
        echo "  decrease [amount]      - Decrease volume by amount (default: 5)"
        echo "  mute                   - Toggle mute/unmute"
        echo "  status                 - Show current volume and mute status"
        echo "  notify <volume>        - Set volume with notification"
        exit 1
        ;;
esac 