#!/bin/sh

directory="ocr_girls/"
feh_pid=0

# kill `feh` on script exit
cleanup() {
    [ "$feh_pid" -ne 0 ] && kill "$feh_pid" 2>/dev/null
}
trap cleanup EXIT

find "$directory" -type f -name "*.txt" -print | while IFS= read -r file; do
    if [ "$feh_pid" -ne 0 ]; then
        kill "$feh_pid" 2>/dev/null || true
    fi

    printf "File: %s\n" "$(basename "$file")"
    echo "----- File Contents Start -----"
    cat "$file"
    echo "----- File Contents End -------"
    echo ""

    while true; do
        echo "y. Yes (Continue to next file)"
        echo "d. Delete"
        echo "e. View and Edit (View .png and replace the content of this .txt file)"

        printf "Choose an option [y/d/e]: "
        read option </dev/tty

        case $option in
        [yY])
            break
            ;;
        [dD])
            rm "$file"
            echo "Deleted $file."
            break
            ;;
        [eE])
            image_path="${file%.txt}.png"
            if [ -f "$image_path" ]; then
                feh "$image_path" &
                feh_pid=$!
            else
                echo "No corresponding .png file found for $file"
                feh_pid=0
            fi

            cp "$file" "$file.bak"
            echo "Editing $file (use Ctrl+D to finish):"
            cat >"$file" </dev/tty
            break
            ;;
        *)
            echo "Invalid option. Please choose again."
            ;;
        esac
    done
done
