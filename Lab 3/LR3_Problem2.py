import random

class Student(object):
    def __init__(self, name, number):
        self.name = name
        self.scores = []
        for count in range(number):
            self.scores.append(0)
    
    def getName(self):
        return self.name
  
    def setScore(self, i, score):
        self.scores[i - 1] = score
    
    def getScore(self, i):
        return self.scores[i - 1]
   
    def getAverage(self):
        return sum(self.scores) / len(self.scores)
    
    def getHighScore(self):
        return max(self.scores)
 
    def __str__(self):
        return "Name: " + self.name  + "\nScores: " + \
               " ".join(map(str, self.scores))
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __ge__(self, other):
        return self.name >= other.name

def main():
    
    students = [
        Student("Alice", 3),
        Student("Bob", 3),
        Student("Charlie", 3),
        Student("Diana", 3),
        Student("Eve", 3),
        Student("Frank", 3),
        Student("Grace", 3),
        Student("Henry", 3)
    ]
    
    sample_scores = [
        [85, 92, 78],
        [90, 88, 95],
        [76, 84, 82],
        [95, 89, 91],
        [88, 86, 90],
        [82, 79, 85],
        [93, 96, 88],
        [87, 91, 84]
    ]
    
    for i, student in enumerate(students):
        for j in range(3):
            student.setScore(j + 1, sample_scores[i][j])
    
    print("Original list of students:")
    print("=" * 40)
    for student in students:
        print(student)
        print(f"Average: {student.getAverage():.2f}")
        print(f"High Score: {student.getHighScore()}")
        print("-" * 30)
    
    random.shuffle(students)
    
    print("\nAfter shuffling:")
    print("=" * 40)
    for student in students:
        print(f"Name: {student.getName()}")
    
    students.sort()
    
    print("\nAfter sorting (alphabetically by name):")
    print("=" * 40)
    for student in students:
        print(student)
        print(f"Average: {student.getAverage():.2f}")
        print(f"High Score: {student.getHighScore()}")
        print("-" * 30)
    
    print("\nSorted names only:")
    print("=" * 40)
    for student in students:
        print(student.getName())

if __name__ == "__main__":
    main()