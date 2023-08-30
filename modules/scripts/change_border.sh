#!/bin/bash

# Initialize variables with default values
input_folder=""
output_folder=""
border_color="#000000"
overwrite_existing=false
bottom_only=false
resize=false
verbose=false

# Function to print usage information
print_usage() {
    echo "Usage: $0 -i <input_folder> -o <output_folder> [-c <border_color>] [-x] [-v]"
    echo "Options:"
    echo "  -i <input_folder>: Specify the input folder."
    echo "  -o <output_folder>: Specify the output folder."
    echo "  -c <border_color>: Specify the border color in hex format (e.g., #RRGGBB). Default: #000000"
    echo "  -x: Optional. Overwrite existing files/folders in the output directory."
    echo "  -b: Optional. keep bottom border only."
    echo "  -r: Optional. resize image when border removed."
    echo "  -v: Optional. Verbose mode. Show detailed output."
}

# Parse command line arguments
while getopts ":i:o:c:xbrv" opt; do
    case $opt in
        i) input_folder="$OPTARG";;
        o) output_folder="$OPTARG";;
        c) border_color="$OPTARG";;
        x) overwrite_existing=true;;
        b) bottom_only=true;;
        r) resize=true;;
        v) verbose=true;;
        \?) echo "Invalid option: -$OPTARG" >&2; print_usage; exit 1;;
        :) echo "Option -$OPTARG requires an argument." >&2; print_usage; exit 1;;
    esac
done

# Function to display verbose output
verbose_echo() {
    if [ "$verbose" = true ]; then
        echo "$1"
    fi
}

# Function to display progress bar
progress_bar() {
    local duration="$1"
    local width=50
    local progress=0
    local step=$((duration / width))
    printf "["

    for ((i = 0; i <= duration; i += step)); do
        printf "#"
        sleep "$step"
    done

    printf "]\n"
}

# Check if required options are provided
if [[ -z "$input_folder" || -z "$output_folder" ]]; then
    echo "Error: Missing required options." >&2
    print_usage
    exit 1
fi

# Process images
total_files=$(find "$input_folder" -type f \( -iname "*.jpg" -o -iname "*.png" \) | wc -l)
processed_files=0

find "$input_folder" -type f \( -iname "*.jpg" -o -iname "*.png" \) | while read -r input_file; do
    # Determine output path
    rel_path="${input_file#"$input_folder"}"
    output_path="$output_folder$rel_path"

    # Check if the output file already exists and overwrite_existing is false
    if [ "$overwrite_existing" = false ] && [ -f "$output_path" ]; then
        verbose_echo "Skipping existing file: $output_path"
        continue
    fi

    # Create output directory if it doesn't exist
    output_dir=$(dirname "$output_path")
    mkdir -p "$output_dir"

    # Clean border color variable
    border_color=`sed -e "s/^'//" -e "s/'$//" <<<$border_color`

    # Process the image using ImageMagick
    if [ "$border_color" == "none" ] && [ "$resize" = true ]; then
      convert "$input_file" -gravity center -crop "$(identify -format '%[fx:w-50]x%[fx:h-50]+0+0' "$input_file")" -bordercolor none -border 0 -resize 1000x1500^ -extent 1000x1500 "$output_path"
    elif [ "$border_color" == "none" ]; then
      convert "$input_file" -gravity center -crop "$(identify -format '%[fx:w-50]x%[fx:h-50]+0+0' "$input_file")" -bordercolor none -border 0 "$output_path"
    elif  [ "$border_color" != "none" ] &&[ "$bottom_only" = true ]; then
      convert "$input_file" -gravity center -crop "$(identify -format '%[fx:w-50]x%[fx:h-50]+0+0' "$input_file")" -bordercolor none -border 0 "$output_path"
      convert "$output_path" -gravity south -background $border_color -splice 0x25 -resize 1000x1500^ "$output_path"
    else
      convert "$input_file" -gravity center -crop "$(identify -format '%[fx:w-50]x%[fx:h-50]+0+0' "$input_file")" -bordercolor $border_color -border 25x25 "$output_path"
    fi
    verbose_echo "Processed: $output_path"

    processed_files=$((processed_files + 1))
    if [ "$verbose" = false ]; then
        progress=$((processed_files * 100 / total_files))
        printf "Processing: [%3d%%]\r" "$progress"
    fi
done

if [ "$verbose" = false ]; then
    echo
fi

echo "Image processing complete."