-- ==========================================
-- BEYOND BORDERS DATABASE SCHEMA
-- ==========================================

CREATE TABLE Country (
    country_name VARCHAR(100) PRIMARY KEY,
    climate VARCHAR(100),
    student_lifestyle TEXT,
    visa_information TEXT,
    accommodation_cost DECIMAL(10,2),
    grocery_cost DECIMAL(10,2),
    transportation_cost DECIMAL(10,2),
    healthcare_info TEXT,
    work_opportunities TEXT
);

CREATE TABLE University (
    university_name VARCHAR(255) PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    tuition_fee DECIMAL(12,2),
    application_deadline DATE,
    world_ranking INT,
    FOREIGN KEY (country_name)
        REFERENCES Country(country_name)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE Scholarship (
    university_name VARCHAR(255),
    Scholarship_Name VARCHAR(255),
    Degree_level VARCHAR(100),
    Amount DECIMAL(10,2),
    Minimum_cgpa DECIMAL(3,2),
    Application_deadline DATE,
    PRIMARY KEY (university_name, Scholarship_Name), 
    FOREIGN KEY (university_name) REFERENCES University(university_name) ON DELETE CASCADE
);

CREATE TABLE Admission_Requirements (
    university_name VARCHAR(255) PRIMARY KEY,
    minimum_cgpa DECIMAL(3,2),
    IELTS_score_required DECIMAL(2,1),
    TOEFL_score_required INT,
    PTE_score_required INT,
    GRE_score_required INT,
    GMAT_score_required INT,
    SAT_score_required INT,
    documents_required TEXT,
    FOREIGN KEY (university_name) REFERENCES University(university_name) ON DELETE CASCADE
);

CREATE TABLE Student (
    Email VARCHAR(255) PRIMARY KEY,
    Full_Name VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Nationality VARCHAR(100),
    Phone VARCHAR(20),
    Profile_photo VARCHAR(255),
    Current_institution VARCHAR(255),
    Current_degree VARCHAR(100),
    cgpa DECIMAL(3,2),
    degree_level_sought VARCHAR(100),
    Field_of_study VARCHAR(100)
);

CREATE TABLE Saved_University (
    Email VARCHAR(255),
    university_name VARCHAR(255),
    PRIMARY KEY (Email, university_name),
    FOREIGN KEY (Email) REFERENCES Student(Email) ON DELETE CASCADE,
    FOREIGN KEY (university_name) REFERENCES University(university_name) ON DELETE CASCADE
);

CREATE TABLE Saved_Scholarship (
    Email VARCHAR(255),
    university_name VARCHAR(255),
    Scholarship_Name VARCHAR(255),
    PRIMARY KEY (Email, university_name, Scholarship_Name),
    FOREIGN KEY (Email) REFERENCES Student(Email) ON DELETE CASCADE,
    FOREIGN KEY (university_name, Scholarship_Name) REFERENCES Scholarship(university_name, Scholarship_Name) ON DELETE CASCADE
);

CREATE TABLE Standardized_Test (
    Email VARCHAR(255),
    Test_Name VARCHAR(100),
    Score DECIMAL(6,2),
    PRIMARY KEY (Email, Test_Name),
    FOREIGN KEY (Email) REFERENCES Student(Email) ON DELETE CASCADE
);

CREATE TABLE Mentor (
    Mentor_Email VARCHAR(255) PRIMARY KEY,
    Full_Name VARCHAR(150) NOT NULL,
    Current_Institution VARCHAR(150),
    Field_of_Study VARCHAR(150),
    Highest_Degree VARCHAR(100)
);

CREATE TABLE UPLOADED_DOCUMENT (
    Email VARCHAR(255),
    file_name VARCHAR(255),
    Document_type VARCHAR(100),
    Upload_date DATE,
    Feedback TEXT,
    Mentor_Email VARCHAR(255),
    Rating DECIMAL(3,2),
    Feedback_date DATE,
    PRIMARY KEY (Email, file_name),
    FOREIGN KEY (Email) REFERENCES Student(Email) ON DELETE CASCADE,
    FOREIGN KEY (Mentor_Email) REFERENCES Mentor(Mentor_Email) ON DELETE SET NULL
);