import sqlite3
connection =sqlite3.connect("grant.db")
print(connection.total_changes)
cursor = connection.cursor()

#create researcher table
cursor.execute("CREATE TABLE IF NOT EXISTS Researcher (\
               Email TEXT PRIMARY KEY,\
               first_name TEXT, \
               last_name TEXT, \
               organization TEXT)")

#create meating_date relation
cursor.execute("CREATE TABLE IF NOT EXISTS Meeting (\
                Mid INTEGER PRIMARY KEY,\
                date DATE)")

#assume application deadline is 7 days before and review deadline is on the meeting 
#create competition table
cursor.execute("CREATE TABLE IF NOT EXISTS Competions (\
                Cid INTEGER PRIMARY KEY,\
                topic TEXT, title TEXT,\
                description TEXT, \
                status TEXT, Mid INTEGER, \
                FOREIGN KEY (Mid) REFERENCES Meeting(Mid))")

#create application table
cursor.execute("CREATE TABLE IF NOT EXISTS Applications (\
                Aid INTEGER PRIMARY KEY,\
                Cid INTEGER, \
                principal_email TEXT,\
                status TEXT, \
                submission_date DATE,\
                requested_amount NUMERIC,\
                awarded_Amount NUMERIC,\
                FOREIGN KEY (Cid) REFERENCES Competition(Cid),\
                FOREIGN KEY (principal_email) REFERENCES Researcher(Email))")

#create Application_Collab relation
cursor.execute("CREATE TABLE IF NOT EXISTS Application_Collabs (\
                Aid INTEGER,\
                collaborator_email TEXT, \
                PRIMARY KEY (Aid, collaborator_email), \
                FOREIGN KEY (Aid) REFERENCES Applications(Aid),\
                FOREIGN KEY (collaborator_email) REFERENCES Researcher(Email) )")

#create Application_Reviewers relation
cursor.execute("CREATE TABLE IF NOT EXISTS Application_Reviewers (\
                aid INTEGER,\
                reviewer_email TEXT,\
                PRIMARY KEY (Aid, reviewer_email),\
                FOREIGN KEY (Aid) REFERENCES Applications(Aid),\
                FOREIGN KEY (reviewer_email) REFERENCES Researcher(Email))")

#inserting into researchers
researcher_data = [
    ('1@UBC.com', 'John', 'Doe', 'UBC'),
    ('2@SFU.com', 'Jane', 'Smith', 'SFU'),
    ('3@Langara.com', 'Alice', 'Johnson', 'Langara'),
    ('4@TRU.com', 'Bob', 'Williams', 'TRU'),
    ('5@Harvard.com', 'Emily', 'Brown', 'Harvard'),
    ('6@UBC.com', 'Michael', 'Jones', 'UBC'),
    ('7@SFU.com', 'Emma', 'Davis', 'SFU'),
    ('8@Langara.com', 'James', 'Miller', 'Langara'),
    ('9@TRU.com', 'Olivia', 'Wilson', 'TRU'),
    ('10@Harvard.com', 'William', 'Taylor', 'Harvard'),
    ('11@UBC.com', 'Sophia', 'Anderson', 'UBC'),
    ('12@SFU.com', 'Daniel', 'Thomas', 'SFU'),
    ('13@Langara.com', 'Chloe', 'Jackson', 'Langara'),
    ('14@TRU.com', 'Benjamin', 'White', 'TRU'),
    ('15@Harvard.com', 'Ava', 'Harris', 'Harvard'),
    ('16@UBC.com', 'Mason', 'Martin', 'UBC'),
    ('17@SFU.com', 'Harper', 'Thompson', 'SFU'),
    ('18@Langara.com', 'Ethan', 'Garcia', 'Langara'),
    ('19@TRU.com', 'Evelyn', 'Martinez', 'TRU'),
    ('20@Harvard.com', 'Alexander', 'Lopez', 'Harvard'),
    ('21@UBC.com', 'Mia', 'Hernandez', 'UBC'),
    ('22@SFU.com', 'Charlotte', 'Young', 'SFU'),
    ('23@Langara.com', 'Liam', 'King', 'Langara'),
    ('24@TRU.com', 'Isabella', 'Lee', 'TRU'),
    ('25@Harvard.com', 'Lucas', 'Scott', 'Harvard')
]
sql_insert = '''INSERT INTO Researcher (Email, first_name, last_name, organization) VALUES (?, ?, ?, ?)'''
cursor.executemany(sql_insert, researcher_data)

#insert meeting data
meeting_data = [
    (1, '2020-04-15'),
    (2, '2021-07-22'),
    (3, '2022-09-05'),
    (4, '2023-01-18'),
    (5, '2023-06-30'),
    (6, '2021-11-11'),
    (7, '2020-08-03'),
    (8, '2022-03-25'),
    (9, '2024-05-09'),
    (10, '2023-10-14')
]
sql_insert = '''INSERT INTO Meeting (Mid, date) VALUES (?, ?)'''
cursor.executemany(sql_insert, meeting_data)

#insert Competition data
competitions_data = [
    (1,"1, Biology", "Biology Competition 1", "Description of Biology Competition 1", "Active", 1),
    (2,"2,Chemistry", "Chemistry Competition 1", "Description of Chemistry Competition 1", "Inactive", 2),
    (3, "Computer Science", "Computer Science Competition 1", "Description of CS Competition 1", "Active", 3),
    (4,"Biology", "Biology Competition 2", "Description of Biology Competition 2", "Active", 4),
    (5,"Chemistry", "Chemistry Competition 2", "Description of Chemistry Competition 2", "Inactive", 5),
    (6,"Computer Science", "Computer Science Competition 2", "Description of CS Competition 2", "Active", 3),  
    (7,"Biology", "Biology Competition 3", "Description of Biology Competition 3", "Active", 7),
    (8,"Chemistry", "Chemistry Competition 3", "Description of Chemistry Competition 3", "Inactive", 8),
    (9,"Computer Science", "Computer Science Competition 3", "Description of CS Competition 3", "Active", 9),
    (10,"Biology", "Biology Competition 4", "Description of Biology Competition 4", "Active", 10),
    (11,"Biology", "Biology Competition 5", "Description of Biology Competition 5", "Active", 11)   
]
sql_insert = "INSERT INTO Competions (Cid, topic, title, description, status, Mid) VALUES (?,?, ?, ?, ?, ?)"
cursor.executemany(sql_insert, competitions_data)

#insert applications

application_data = [
    (1,1, '22@SFU.com', "Pending", "2020-04-02", 1000.00, 0.00),
    (2,1, '20@Harvard.com', "Pending", "2020-04-03", 4000, 0.00),
    (3,3, "email3@example.com", "Pending", "2021-05-03", 2500, 0.00),
    (4,4, "email4@example.com", "Pending", "2023-05-15", 1000.00, 0.00),
    (5,5, "email5@example.com", "Pending", "2023-04-03", 1000.00, 0.00),
    (6,3, "email6@example.com", "Pending", "2020-04-03", 1000.00, 0.00),
    (7,4, "email7@example.com", "Pending", "2023-01-01", 1000.00, 0.00),
    (8,8, "email8@example.com", "Pending", "2022-03-25", 1000.00, 0.00),
    (9,9, "email9@example.com", "Pending", "2024-02-03", 1000.00, 0.00),
    (10,9, "email10@example.com", "Pending", "2024-01-03", 1000.00, 0.00),
    (11,11, "email11@example.com", "Pending", "2023-04-03", 1000.00, 0.00)
]
#error at requested amount : sqlite3.OperationalError: table Applications has no column named requested_amount
sql_insert = "INSERT INTO Applications (Aid, Cid, principal_email, status, submission_date, requested_amount, awarded_amount)VALUES (?, ?, ?, ?, ?, ?, ?)"
cursor.executemany(sql_insert, application_data)
