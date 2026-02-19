import sqlite3

# Connect to SQLite (in memory for testing)
conn = sqlite3.connect(':memory:')

# this is important because foreign keys are OFF by default in SQLite
conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

# Helper function to inspect table contents
def print_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"\nTable: {table_name}")
    print(" | ".join(columns))
    print("-" * 30)

    for row in rows:
        print(" | ".join(str(value) for value in row))

# Create tables
cursor.execute("""
CREATE TABLE student (
    student_id INT PRIMARY KEY,
    name TEXT NOT NULL,
    age INT
)
""")

cursor.execute("""
CREATE TABLE registered_courses  (
    student_id INT,
    course_id INT,
    PRIMARY KEY(student_id,course_id),
    FOREIGN KEY(student_id) REFERENCES student(student_id)
               
)
""")

cursor.execute("""
CREATE TABLE grades (
    student_id INT,
    course_id INT,
    grade INT,
    PRIMARY KEY(student_id,course_id),
    FOREIGN KEY(student_id,course_id) REFERENCES registered_courses(student_id,course_id)
)
""")


students = [
    (1, 'Alice', 20),
    (2, 'Bob', 22),
    (3, 'Charlie', 21)
]

cursor.executemany("INSERT INTO student VALUES (?, ?, ?)", students)

conn.commit()

print_table(cursor, "student")


# Example SELECT query
cursor.execute("SELECT * FROM student")
print("\nResult of: SELECT * FROM student")
for row in cursor.fetchall():
    print(row)

print()

courses = [
    (1,101),
    (1,102),
    (2,101),
    (2,103),
    (3,103),
    (3,107)
]
cursor.executemany("INSERT INTO registered_courses VALUES (?, ?)", courses)

conn.commit()

print_table(cursor, "registered_courses")

print()

grades= [
    (1,101,90),
    (1,102,93),
    (2,101,72),
    (2,103,77),
    (3,103,68),
    (3,107,88)
]
cursor.executemany("INSERT INTO grades VALUES (?, ?, ?)", grades)

conn.commit()

print_table(cursor, "grades")

print()

cursor.execute("""
SELECT g.student_id, g.course_id, g.grade AS max_grade 
FROM grades g 
JOIN (
    SELECT student_id, MAX(grade) AS max_grade 
    FROM grades 
    GROUP BY student_id
) mg 
ON g.student_id = mg.student_id AND g.grade =mg.max_grade; 
""")
print("\nResult of part 1:")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT student_id, AVG (grade) FROM grades GROUP BY student_id")

print("\nResult of part 2:")
for row in cursor.fetchall():
    print(row)


conn.close()
