def median(numbers):
    if not numbers:
        raise ValueError("Cannot compute median of empty list")
    
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    
    if n % 2 == 1:
        return sorted_nums[n // 2]
    else:
        mid1 = sorted_nums[n // 2 - 1]
        mid2 = sorted_nums[n // 2]
        return (mid1 + mid2) / 2


def mode(numbers):
    if not numbers:
        raise ValueError("Cannot compute mode of empty list")
    
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    
    max_freq = max(frequency.values())
    
    for num in numbers:
        if frequency[num] == max_freq:
            return num


def mean(numbers):
    if not numbers:
        raise ValueError("Cannot compute mean of empty list")
    
    return sum(numbers) / len(numbers)


def main():
    """Main function to get user input and calculate statistics"""
    try:
        user_input = input("Enter numbers separated by spaces: ")
        numbers = [float(x) for x in user_input.split()]
        
        print(f"\nData: {numbers}")
        print(f"Mean: {mean(numbers)}")
        print(f"Median: {median(numbers)}")
        print(f"Mode: {mode(numbers)}")
        
    except ValueError as e:
        if "could not convert" in str(e):
            print("Error: Please enter only valid numbers separated by spaces.")
        else:
            print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()