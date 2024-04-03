import sqlite3
connection =sqlite3.connect("grant.db")
print(connection.total_changes)
cursor = connection.cursor()

#create researcher table
cursor.execute("CREATE TABLE IF NOT EXISTS Researcher (Email TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, organization TEXT)")

#create meating_date relation
cursor.execute("CREATE TABLE IF NOT EXISTS Meeting (Mid INTEGER PRIMARY KEY, date DATE)")

#create competition table
cursor.execute("CREATE TABLE IF NOT EXISTS Competions (Cid INTEGER PRIMARY KEY, topic TEXT, title TEXT, description TEXT, application_deadline DATE, status TEXT, Mid INTEGER, FOREIGN KEY (Mid) REFERENCES Meeting(Mid))")

#create application table
cursor.execute("CREATE TABLE IF NOT EXISTS Applications (Aid INTEGER PRIMARY KEY, Cid INTEGER, principal_email TEXT, status TEXT, submission_date DATE, review_deadline DATE, requested_amout NUMERIC, awarded_Amout NUMERIC,FOREIGN KEY (Cid) REFERENCES Competition(Cid), FOREIGN KEY (principal_email) REFERENCES Researcher(Email))")

#create Application_Collab relation
cursor.execute("CREATE TABLE IF NOT EXISTS Application_Collabs (Aid INTEGER, collaborator_email TEXT, PRIMARY KEY (Aid, collaborator_email), FOREIGN KEY (Aid) REFERENCES Applications(Aid), FOREIGN KEY (collaborator_email) REFERENCES Researcher(Email) )")

#create Application_Reviewers relation
cursor.execute("CREATE TABLE IF NOT EXISTS Application_Reviewers (aid INTEGER, reviewer_email TEXT, PRIMARY KEY (Aid, reviewer_email), FOREIGN KEY (Aid) REFERENCES Applications(Aid), FOREIGN KEY (reviewer_email) REFERENCES Researcher(Email))")
