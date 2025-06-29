def main():
    filename = input("Enter the filename: ")
    
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        lines = [line.rstrip('\n') for line in lines]
        print(f"File '{filename}' loaded successfully!")
        print()
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    while True:
        print(f"The file has {len(lines)} lines.")
        
        try:
            line_number = int(input("Enter a line number (1-{}) or 0 to quit: ".format(len(lines))))
        except ValueError:
            print("Please enter a valid number.")
            print()
            continue
        
        if line_number == 0:
            print("Goodbye!")
            break
        
        if line_number < 1 or line_number > len(lines):
            print(f"Invalid line number. Please enter a number between 1 and {len(lines)}.")
            print()
            continue
        
        print(f"Line {line_number}: {lines[line_number - 1]}")
        print()

if __name__ == "__main__":
    main()