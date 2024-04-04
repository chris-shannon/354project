import sqlite3
import os #lines 5 and 6
database_name = "grant.db"

if os.path.exists(database_name):
    os.remove(database_name)  # Delete the database file
    print("Old database deleted successfully.")
    # Create a new database
connection = sqlite3.connect(database_name)
print("New database created successfully.")
print(connection.total_changes)
cursor = connection.cursor()
#------------   TABLES  ----------------

#create researcher table
cursor.execute("""CREATE TABLE IF NOT EXISTS Researcher (
               Email TEXT PRIMARY KEY,
               first_name TEXT, 
               last_name TEXT, 
               organization TEXT)""")

#create meating_date relation
cursor.execute("""CREATE TABLE IF NOT EXISTS Meeting (
                Mid INTEGER PRIMARY KEY,
                date DATE)""")

#assume application deadline is 7 days before and review deadline is on the meeting 
#create competition table
cursor.execute("""CREATE TABLE IF NOT EXISTS Competitions (
                Cid INTEGER PRIMARY KEY,
                topic TEXT CHECK(topic IN ('Biology', 'Computer Science', 'Chemistry')),
                title TEXT,
                description TEXT, 
                status TEXT CHECK(status IN ('open', 'closed')),
                Mid INTEGER, 
                FOREIGN KEY (Mid) REFERENCES Meeting(Mid))""")

#create application table
cursor.execute("""CREATE TABLE IF NOT EXISTS Applications (
                Aid INTEGER PRIMARY KEY,
                Cid INTEGER, 
                principal_email TEXT,
                status TEXT CHECK(status IN ('Submitted', 'Not Awarded', 'Awarded')), 
                submission_date DATE,
                requested_amount NUMERIC CHECK(requested_amount >= 0),
                awarded_Amount Numeric CHECK(awarded_Amount > 0 OR awarded_Amount = 0),
                FOREIGN KEY (Cid) REFERENCES Competitions(Cid),
                FOREIGN KEY (principal_email) REFERENCES Researcher(Email))""")

#create Application_Collab relation
cursor.execute("""CREATE TABLE IF NOT EXISTS Application_Collabs (
                Aid INTEGER,
                collaborator_email TEXT, 
                PRIMARY KEY (Aid, collaborator_email), 
                FOREIGN KEY (Aid) REFERENCES Applications(Aid),
                FOREIGN KEY (collaborator_email) REFERENCES Researcher(Email) )""")

#create Application_Reviewers relation
cursor.execute("""CREATE TABLE IF NOT EXISTS Application_Reviewers (
                aid INTEGER,
                reviewer_email TEXT,
                PRIMARY KEY (Aid, reviewer_email),
                FOREIGN KEY (Aid) REFERENCES Applications(Aid),
                FOREIGN KEY (reviewer_email) REFERENCES Researcher(Email))""")


#------------   TRIGGERS  ----------------

#Delete Meeting Trigger
cursor.execute("""CREATE TRIGGER IF NOT EXISTS delete_meeting_trigger
               AFTER DELETE ON Meeting
               FOR EACH ROW
               BEGIN
                   UPDATE Competitions
                   SET Mid = NULL
                   WHERE Mid = OLD.Mid;
               END;""")

#Delete Competition Trigger
cursor.execute("""CREATE TRIGGER IF NOT EXISTS delete_competition_trigger
               AFTER DELETE ON Competitions
               FOR EACH ROW
               BEGIN
                   DELETE FROM Applications
                   WHERE Cid = OLD.Cid;
               END;""")

#Delete Application Trigger
cursor.execute("""CREATE TRIGGER IF NOT EXISTS delete_application_trigger
               AFTER DELETE ON Applications
               FOR EACH ROW
               BEGIN
                   DELETE FROM Application_Collabs
                   WHERE Aid = OLD.Aid; 
                   DELETE FROM Application_Reviewers
                   WHERE Aid = OLD.Aid;
               END;""")

#Delete Researcher Trigger
cursor.execute("""CREATE TRIGGER IF NOT EXISTS delete_researcher_trigger
               AFTER DELETE ON Researcher
               FOR EACH ROW
               BEGIN
                   DELETE FROM Application_Collabs
                   WHERE collaborator_email = OLD.Email;
                    
                   DELETE FROM Application_Reviewers
                   WHERE reviewer_email = OLD.Email;
               END;""")

#Delete Application_Collabs Trigger
cursor.execute("""CREATE TRIGGER IF NOT EXISTS delete_collab_application_trigger
               AFTER DELETE ON Application_Collabs
               FOR EACH ROW
               BEGIN
                   DELETE FROM Applications
                   WHERE Aid = OLD.Aid
                   AND principal_email = OLD.collaborator_email;
               END;""")
#Add principal to collab Trigger
cursor.execute("""CREATE TRIGGER IF NOT EXISTS add_principal_collab_trigger
               After INSERT ON Applications
               BEGIN
                   INSERT INTO Application_Collabs (Aid,collaborator_email)  VALUES (NEW.Aid, NEW.principal_email);
               END;""")

#Check For Conflict of Interest trigger
cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS check_reviewer_conflict
    AFTER INSERT ON Application_Reviewers
    FOR EACH ROW
    BEGIN
        DELETE FROM Application_Reviewers
        WHERE reviewer_email = NEW.reviewer_email AND Aid = NEW.Aid
        AND (SELECT organization
             FROM Researcher
             WHERE Email = NEW.reviewer_email) IN (
                SELECT organization
                FROM Researcher
                JOIN Application_Collabs ON collaborator_email = Researcher.email
                WHERE Application_Collabs.Aid = NEW.aid);
    END;
""")

#Check Valid Application Trigger
cursor.execute("""CREATE TRIGGER IF NOT EXISTS valid_application_trigger
                AFTER INSERT ON Applications
                FOR EACH ROW
                BEGIN
                    DELETE FROM Applications
                WHERE Applications.submission_date >
                    (SELECT Meeting.Date 
                    FROM Applications 
                    JOIN Competitions ON Applications.Cid = Competitions.Cid 
                    JOIN Meeting ON Competitions.Mid = Meeting.Mid
                    WHERE Applications.Aid = NEW.Aid)
                    AND Applications.Aid = NEW.Aid;
               END;""")
#------------   DATA  ----------------

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
    (4, '2023-08-18'),
    (5, '2023-06-30'),
    (6, '2021-11-11'),
    (7, '2020-08-03'),
    (8, '2022-03-25'),
    (9, '2024-09-09'),
    (10, '2023-10-14')
]
sql_insert = '''INSERT INTO Meeting (Mid, date) VALUES (?, ?)'''
cursor.executemany(sql_insert, meeting_data)

#insert Competition data
competitions_data = [
    (1,"Biology", "Biology Competition 1", "Description of Biology Competition 1", "open", 1),
    (2,"Chemistry", "Chemistry Competition 1", "Description of Chemistry Competition 1", "closed", 2),
    (3, "Computer Science", "Computer Science Competition 1", "Description of CS Competition 1", "open", 3),
    (4,"Biology", "Biology Competition 2", "Description of Biology Competition 2", "open", 4),
    (5,"Chemistry", "Chemistry Competition 2", "Description of Chemistry Competition 2", "closed", 5),
    (6,"Computer Science", "Computer Science Competition 2", "Description of CS Competition 2", "open", 3),  
    (7,"Biology", "Biology Competition 3", "Description of Biology Competition 3", "open", 7),
    (8,"Chemistry", "Chemistry Competition 3", "Description of Chemistry Competition 3", "closed", 8),
    (9,"Computer Science", "Computer Science Competition 3", "Description of CS Competition 3", "open", 9),
    (10,"Biology", "Biology Competition 4", "Description of Biology Competition 4", "open", 10),
    (11,"Biology", "Biology Competition 5", "Description of Biology Competition 5", "open", 10)   
]
sql_insert = "INSERT INTO Competitions (Cid, topic, title, description, status, Mid) VALUES (?,?, ?, ?, ?, ?)"
cursor.executemany(sql_insert, competitions_data)

#insert applications
application_data = [
    (1,1, '22@SFU.com', "Awarded", "2020-04-02", 1000, 500),
    (2,1, '20@Harvard.com', "Awarded", "2020-02-13", 50000, 25000),
    (3,3, '2@SFU.com', "Awarded", "2021-05-03", 2500, 1000),
    (4,4, '4@TRU.com', "Awarded", "2023-05-15", 100000,50000),
    (5,5, '20@Harvard.com', "Not Awarded", "2023-04-03", 1000.00, 0),
    (6,3, '21@UBC.com', "Awarded", "2020-12-25", 55000, 50000),
    (7,4, '7@SFU.com', "Not Awarded", "2023-01-01", 20000, 0),
    (8,8, '21@UBC.com', "Not Awarded", "2022-03-25", 1000.00, 0),
    (9,9, '23@Langara.com', "Submitted", "2024-02-03", 20000, 0),
    (10,9, '25@Harvard.com', "Submitted", "2024-01-03", 25000, 0),
    (11,11, '9@TRU.com', "Not Awarded", "2025-04-03", 1000.00, 0) #an invalid entry
]
sql_insert = "INSERT INTO Applications (Aid, Cid, principal_email, status, submission_date, requested_amount, awarded_amount)VALUES (?, ?, ?, ?, ?, ?, ?)"
cursor.executemany(sql_insert, application_data)

#insert Collabs
application_collabs_data = [
    ('1@UBC.com',1),
    ('3@Langara.com',2),
    ('4@TRU.com',2),
    ('5@Harvard.com',5),
    ('8@Langara.com',6),
    ('10@Harvard.com',1),
    ('12@SFU.com',3),
    ('13@Langara.com',3),
    ('17@SFU.com',4),
    ('25@Harvard.com',9),
]
sql_insert = "INSERT INTO Application_Collabs (collaborator_email,Aid)VALUES (?, ?)"
cursor.executemany(sql_insert, application_collabs_data)

#insert Reviewer
application_reviewers_data = [
    ('8@Langara.com',1),
    ('12@SFU.com',5),
    ('8@Langara.com',6),
    ('9@TRU.com',1),
    ('5@Harvard.com',3),
    ('8@Langara.com',4),
    ('9@TRU.com',5),
    ('8@Langara.com',7),
    ('16@UBC.com',7),
    ('16@UBC.com',5),
    ('23@Langara.com',1)
]
sql_insert = "INSERT INTO Application_Reviewers (reviewer_email,Aid)VALUES (?, ?)"
cursor.executemany(sql_insert, application_reviewers_data)


##--------------testing stuff remove later------------------
# #prints finds aids with awarded_amount > 20000
# cursor.execute("""SELECT Applications.Aid, Applications.submission_date, Meeting.Date 
#             FROM Applications 
#             JOIN Competitions ON Applications.Cid = Competitions.Cid 
#             JOIN Meeting ON Competitions.Mid = Meeting.Mid
#             WHERE Applications.awarded_amount > 20000
#             """)
# rows = cursor.fetchall()
# for row in rows:
#    print(row)
# print("reviewer organization")
# cursor.execute("""SELECT *
#                 FROM Application_Reviewers
#                """)
# rows = cursor.fetchall()
# for row in rows:
#    print(row)
# #finds organizations that reviewer can not be a part of 
# print("schools reviewer cannot be a part of")
# cursor.execute("""SELECT organization
#                 FROM Application_Reviewers
#                 JOIN Application_Collabs on Application_Collabs.Aid = Application_Reviewers.Aid
#                 JOIN Researcher on Application_Collabs.collaborator_email = Researcher.email
#                """)
# rows = cursor.fetchall()
# for row in rows:
#    print(row)