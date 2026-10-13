# Student Grade Management System

A simple command-line program in Python to store student marks and get each student's average, grade and rank. Data is saved in `students.json`, so it is kept between runs.

## Features

- Add students with their subjects and marks
- View a student's marks, average, grade and rank
- Show a ranking of all students
- Delete a student

## Requirements

Python 3 (no extra libraries needed)

## How to Run

```bash
python main.py
```

## Menu

```
1. Add student
2. View student
3. Show rankings
4. Delete student
5. Exit
```

## Example Output

```
Rank  Name           Average   Grade
1     Ankit          94.33     A
2     Abhik          88.33     B
3     Rohan          71.67     C
4     Kabin          66.67     D
5     Ronit          58.33     E
```

## Grading Scale

| Average | Grade |
|---------|-------|
| 90+     | A     |
| 80-89   | B     |
| 70-79   | C     |
| 60-69   | D     |
| Below 60 | E    |
