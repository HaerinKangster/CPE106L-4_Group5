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
    student = Student("Ken", 5)
    print(student)
    for i in range(1, 6):
        student.setScore(i, 100)
    print(student)
    
    print("\n--- Testing Comparison Methods ---")
    student1 = Student("Alice", 3)
    student2 = Student("Bob", 3)
    student3 = Student("Alice", 3)
    
    print(f"student1 name: {student1.getName()}")
    print(f"student2 name: {student2.getName()}")
    print(f"student3 name: {student3.getName()}")
    
    print(f"\nEquality tests:")
    print(f"student1 == student2: {student1 == student2}")  
    print(f"student1 == student3: {student1 == student3}")  
    
    print(f"\nLess than tests:")
    print(f"student1 < student2: {student1 < student2}")   
    print(f"student2 < student1: {student2 < student1}") 
    
    print(f"\nGreater than or equal to tests:")
    print(f"student1 >= student2: {student1 >= student2}")
    print(f"student2 >= student1: {student2 >= student1}")
    print(f"student1 >= student3: {student1 >= student3}")

if __name__ == "__main__":
    main()