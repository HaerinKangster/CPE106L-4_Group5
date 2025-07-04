def mean(numbers):
    if not numbers:
        return 0
    
    total = sum(numbers)
    return total / len(numbers)


def median(numbers):
    if not numbers:
        return 0
    
    sorted_numbers = sorted(numbers)
    length = len(sorted_numbers)
    midpoint = length // 2
    
    if length % 2 == 1:
        return sorted_numbers[midpoint]
    else:
        return (sorted_numbers[midpoint - 1] + sorted_numbers[midpoint]) / 2


def mode(numbers):
    if not numbers:
        return 0

    frequency_count = {}
    for number in numbers:
        if number in frequency_count:
            frequency_count[number] += 1
        else:
            frequency_count[number] = 1
    
    max_frequency = max(frequency_count.values())
    
    for number, frequency in frequency_count.items():
        if frequency == max_frequency:
            return number


def main():
    test_numbers = [1, 2, 3, 3, 4, 5, 6]
    
    print("Test numbers:", test_numbers)
    print("Mean:", mean(test_numbers))
    print("Median:", median(test_numbers))
    print("Mode:", mode(test_numbers))
    
    print("\n" + "="*30)
    
    empty_list = []
    print("Empty list:", empty_list)
    print("Mean:", mean(empty_list))
    print("Median:", median(empty_list))
    print("Mode:", mode(empty_list))
    
    print("\n" + "="*30)
    
    test_numbers2 = [10, 20, 20, 30, 40]
    print("Test numbers 2:", test_numbers2)
    print("Mean:", mean(test_numbers2))
    print("Median:", median(test_numbers2))
    print("Mode:", mode(test_numbers2))


if __name__ == "__main__":
    main()