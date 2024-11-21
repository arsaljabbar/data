import sys

# Open the file in append mode
with open("output.txt", "a") as file:
    buffer = ""
    print("Start typing (press Enter to save, Ctrl+C to exit):")
    try:
        while True:
            char = sys.stdin.read(1)  # Read one character at a time
            if char == "\n":          # If Enter is pressed
                file.write(buffer + "\n")  # Save the current buffer to the file
                file.flush()          # Ensure data is written to disk
                buffer = ""           # Clear the buffer
            else:
                buffer += char        # Append the character to the buffer
    except KeyboardInterrupt:
        print("\nExiting. Data saved.")
