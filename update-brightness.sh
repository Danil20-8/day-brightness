cd "$(dirname "$0")"

brightness=$(python3 get-nice-brightness.py $(cat /sys/class/backlight/intel_backlight/brightness) $(cat /sys/class/backlight/intel_backlight/max_brightness))

# echo $brightness

with_sudo=""

if [ "$EUID" -ne 0 ]
then
  with_sudo=sudo
fi

echo $brightness | $with_sudo tee /sys/class/backlight/intel_backlight/brightness