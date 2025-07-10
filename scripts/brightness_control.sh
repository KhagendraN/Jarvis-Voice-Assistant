#!/bin/bash

# Brightness Control Script for Jarvis Voice Assistant
# This script handles brightness control for various display systems

# Function to get current brightness
get_brightness() {
    # Try different brightness control methods
    if [ -f "/sys/class/backlight/intel_backlight/brightness" ]; then
        # Intel backlight
        cat /sys/class/backlight/intel_backlight/brightness
    elif [ -f "/sys/class/backlight/nvidia_backlight/brightness" ]; then
        # NVIDIA backlight
        cat /sys/class/backlight/nvidia_backlight/brightness
    elif [ -f "/sys/class/backlight/amdgpu_bl0/brightness" ]; then
        # AMD backlight
        cat /sys/class/backlight/amdgpu_bl0/brightness
    elif [ -f "/sys/class/backlight/acpi_video0/brightness" ]; then
        # ACPI video backlight
        cat /sys/class/backlight/acpi_video0/brightness
    elif command -v brightnessctl &> /dev/null; then
        # brightnessctl
        brightnessctl get
    elif command -v xrandr &> /dev/null; then
        # xrandr (X11)
        xrandr --verbose | grep -i brightness | head -1 | awk '{print $2}'
    else
        echo "No brightness control method found."
        return 1
    fi
}

# Function to get max brightness
get_max_brightness() {
    # Try different brightness control methods
    if [ -f "/sys/class/backlight/intel_backlight/max_brightness" ]; then
        # Intel backlight
        cat /sys/class/backlight/intel_backlight/max_brightness
    elif [ -f "/sys/class/backlight/nvidia_backlight/max_brightness" ]; then
        # NVIDIA backlight
        cat /sys/class/backlight/nvidia_backlight/max_brightness
    elif [ -f "/sys/class/backlight/amdgpu_bl0/max_brightness" ]; then
        # AMD backlight
        cat /sys/class/backlight/amdgpu_bl0/max_brightness
    elif [ -f "/sys/class/backlight/acpi_video0/max_brightness" ]; then
        # ACPI video backlight
        cat /sys/class/backlight/acpi_video0/max_brightness
    elif command -v brightnessctl &> /dev/null; then
        # brightnessctl
        brightnessctl max
    else
        echo "No brightness control method found."
        return 1
    fi
}

# Function to set brightness
set_brightness() {
    local brightness="$1"
    
    # Try different brightness control methods
    if [ -f "/sys/class/backlight/intel_backlight/brightness" ]; then
        # Intel backlight
        echo "$brightness" | sudo tee /sys/class/backlight/intel_backlight/brightness > /dev/null
    elif [ -f "/sys/class/backlight/nvidia_backlight/brightness" ]; then
        # NVIDIA backlight
        echo "$brightness" | sudo tee /sys/class/backlight/nvidia_backlight/brightness > /dev/null
    elif [ -f "/sys/class/backlight/amdgpu_bl0/brightness" ]; then
        # AMD backlight
        echo "$brightness" | sudo tee /sys/class/backlight/amdgpu_bl0/brightness > /dev/null
    elif [ -f "/sys/class/backlight/acpi_video0/brightness" ]; then
        # ACPI video backlight
        echo "$brightness" | sudo tee /sys/class/backlight/acpi_video0/brightness > /dev/null
    elif command -v brightnessctl &> /dev/null; then
        # brightnessctl
        brightnessctl set "$brightness"
    elif command -v xrandr &> /dev/null; then
        # xrandr (X11) - convert to percentage
        local max_brightness=$(get_max_brightness)
        if [ $? -eq 0 ]; then
            local percentage=$(echo "scale=2; $brightness / $max_brightness" | bc)
            xrandr --output $(xrandr | grep " connected" | awk '{print $1}' | head -1) --brightness "$percentage"
        else
            echo "Failed to get max brightness for xrandr"
            return 1
        fi
    else
        echo "No brightness control method found."
        return 1
    fi
    
    echo "Brightness set to $brightness"
}

# Function to increase brightness
increase_brightness() {
    local increment="${1:-100}"
    local current_brightness=$(get_brightness)
    local max_brightness=$(get_max_brightness)
    
    if [ $? -eq 0 ] && [ $? -eq 0 ]; then
        local new_brightness=$((current_brightness + increment))
        
        # Ensure brightness doesn't exceed maximum
        if [ "$new_brightness" -gt "$max_brightness" ]; then
            new_brightness="$max_brightness"
        fi
        
        set_brightness "$new_brightness"
    else
        echo "Failed to get current or max brightness"
        return 1
    fi
}

# Function to decrease brightness
decrease_brightness() {
    local decrement="${1:-100}"
    local current_brightness=$(get_brightness)
    
    if [ $? -eq 0 ]; then
        local new_brightness=$((current_brightness - decrement))
        
        # Ensure brightness doesn't go below 0
        if [ "$new_brightness" -lt 0 ]; then
            new_brightness=0
        fi
        
        set_brightness "$new_brightness"
    else
        echo "Failed to get current brightness"
        return 1
    fi
}

# Function to set brightness percentage
set_brightness_percentage() {
    local percentage="$1"
    local max_brightness=$(get_max_brightness)
    
    if [ $? -eq 0 ]; then
        # Ensure percentage is between 0 and 100
        if [ "$percentage" -lt 0 ]; then
            percentage=0
        elif [ "$percentage" -gt 100 ]; then
            percentage=100
        fi
        
        # Calculate brightness value
        local brightness=$((max_brightness * percentage / 100))
        set_brightness "$brightness"
    else
        echo "Failed to get max brightness"
        return 1
    fi
}

# Function to get brightness percentage
get_brightness_percentage() {
    local current_brightness=$(get_brightness)
    local max_brightness=$(get_max_brightness)
    
    if [ $? -eq 0 ] && [ $? -eq 0 ]; then
        local percentage=$((current_brightness * 100 / max_brightness))
        echo "$percentage%"
    else
        echo "Failed to get brightness values"
        return 1
    fi
}

# Function to show brightness status
show_status() {
    local current_brightness=$(get_brightness)
    local max_brightness=$(get_max_brightness)
    
    if [ $? -eq 0 ] && [ $? -eq 0 ]; then
        local percentage=$((current_brightness * 100 / max_brightness))
        echo "Brightness: $current_brightness/$max_brightness ($percentage%)"
    else
        echo "Failed to get brightness status"
        return 1
    fi
}

# Function to set brightness with notification
set_brightness_with_notify() {
    local brightness="$1"
    set_brightness "$brightness"
    
    # Show notification if available
    if command -v notify-send &> /dev/null; then
        local percentage=$(get_brightness_percentage)
        notify-send "Brightness Control" "Brightness set to $percentage" -t 1000
    fi
}

# Main script logic
case "${1:-status}" in
    "get")
        get_brightness
        ;;
    "get-percent")
        get_brightness_percentage
        ;;
    "set")
        if [ -n "$2" ]; then
            set_brightness "$2"
        else
            echo "Usage: $0 set <brightness>"
            exit 1
        fi
        ;;
    "set-percent")
        if [ -n "$2" ]; then
            set_brightness_percentage "$2"
        else
            echo "Usage: $0 set-percent <percentage>"
            exit 1
        fi
        ;;
    "increase"|"up")
        increment="${2:-100}"
        increase_brightness "$increment"
        ;;
    "decrease"|"down")
        decrement="${2:-100}"
        decrease_brightness "$decrement"
        ;;
    "status")
        show_status
        ;;
    "notify")
        if [ -n "$2" ]; then
            set_brightness_with_notify "$2"
        else
            echo "Usage: $0 notify <brightness>"
            exit 1
        fi
        ;;
    *)
        echo "Usage: $0 {get|get-percent|set <brightness>|set-percent <percentage>|increase [amount]|decrease [amount]|status|notify <brightness>}"
        echo "  get                    - Get current brightness value"
        echo "  get-percent            - Get current brightness percentage"
        echo "  set <brightness>       - Set brightness to specific value"
        echo "  set-percent <percent>  - Set brightness to percentage (0-100)"
        echo "  increase [amount]      - Increase brightness by amount (default: 100)"
        echo "  decrease [amount]      - Decrease brightness by amount (default: 100)"
        echo "  status                 - Show current brightness status"
        echo "  notify <brightness>    - Set brightness with notification"
        exit 1
        ;;
esac 