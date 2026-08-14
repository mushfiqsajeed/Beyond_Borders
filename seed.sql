-- ==========================================
-- BEYOND BORDERS INITIAL DATA SEED
-- ==========================================

INSERT INTO Country (country_name, climate, student_lifestyle, visa_information, accommodation_cost, grocery_cost, transportation_cost, healthcare_info, work_opportunities) VALUES
('USA', 'Varied, mostly temperate', 'Vibrant campus life, highly active', 'F-1 Student Visa required', 1200.00, 400.00, 100.00, 'Private health insurance mandatory', '20 hrs/week on-campus only'),
('UK', 'Temperate oceanic', 'Historic and culturally diverse', 'Tier 4 Student Visa', 900.00, 300.00, 80.00, 'IHS fee covers National Health Service', '20 hrs/week during term'),
('Canada', 'Cold winters, warm summers', 'Inclusive and multicultural', 'Study Permit required', 800.00, 350.00, 110.00, 'Provincial health coverage varies', '20 hrs/week off-campus'),
('Australia', 'Mostly warm and dry', 'Outdoorsy and relaxed', 'Subclass 500 Visa', 1100.00, 400.00, 130.00, 'Overseas Student Health Cover (OSHC) mandatory', '48 hrs per fortnight'),
('Singapore', 'Tropical hot and humid', 'Fast-paced, modern, safe', 'Student Pass required', 1000.00, 350.00, 70.00, 'University group insurance provided', '16 hrs/week during term'),
('South Korea', 'Four distinct seasons', 'Tech-forward, rigorous academic culture', 'D-2 Visa required', 600.00, 250.00, 60.00, 'National Health Insurance (NHIS)', '20 hrs/week with permission'),
('China', 'Diverse, regional variations', 'Traditional mixed with high-tech', 'X1/X2 Visa', 400.00, 200.00, 40.00, 'Comprehensive Medical Insurance needed', 'Limited; requires university approval'),
('Germany', 'Temperate seasonal', 'Independent and travel-friendly', 'Student Visa for non-EU', 550.00, 250.00, 90.00, 'Public health insurance required', '120 full days or 240 half days/year'),
('Finland', 'Cold snowy winters', 'Quiet, nature-focused, high quality of life', 'Residence Permit for Studies', 650.00, 280.00, 65.00, 'Private insurance required if < 2 years', '30 hrs/week in related fields'),
('Netherlands', 'Maritime, mild winters', 'Bicycle culture, very international', 'Residence Permit (VVR)', 800.00, 300.00, 80.00, 'Standard Dutch health insurance', '16 hrs/week max'),
('Sweden', 'Temperate to Sub-Arctic', 'Egalitarian, sustainable lifestyle', 'Residence Permit', 750.00, 320.00, 90.00, 'Comprehensive coverage if studying > 1 yr', 'Unlimited hours (must maintain grades)'),
('Switzerland', 'Alpine climate', 'High standard of living, scenic', 'National Visa D', 1300.00, 500.00, 120.00, 'Mandatory Swiss health insurance', '15 hrs/week after 6 months');

INSERT INTO University (university_name, country_name, tuition_fee, application_deadline, world_ranking) VALUES
('Massachusetts Institute of Technology (MIT)', 'USA', 57500.00, '2026-12-15', 1),
('University of Oxford', 'UK', 38000.00, '2026-10-15', 3),
('University of Toronto', 'Canada', 45000.00, '2026-11-07', 21),
('University of Melbourne', 'Australia', 35000.00, '2026-10-31', 14),
('National University of Singapore (NUS)', 'Singapore', 22000.00, '2026-02-28', 8),
('Seoul National University', 'South Korea', 6500.00, '2026-09-10', 41),
('Tsinghua University', 'China', 5500.00, '2026-12-01', 25),
('Technical University of Munich (TUM)', 'Germany', 3000.00, '2026-07-15', 37),
('University of Helsinki', 'Finland', 15000.00, '2026-01-05', 115),
('Delft University of Technology', 'Netherlands', 19500.00, '2026-04-01', 47),
('KTH Royal Institute of Technology', 'Sweden', 16000.00, '2026-01-15', 73),
('ETH Zurich', 'Switzerland', 1500.00, '2026-12-15', 7);

INSERT INTO Scholarship (university_name, Scholarship_Name, Degree_level, Amount, Minimum_cgpa, Application_deadline) VALUES
('Massachusetts Institute of Technology (MIT)', 'MIT Presidential Fellowship', 'Ph.D.', 85000.00, 3.80, '2026-12-01'),
('University of Oxford', 'Clarendon Fund', 'Master''s', 45000.00, 3.75, '2026-01-20'),
('University of Toronto', 'Lester B. Pearson International Scholarship', 'Bachelor''s', 60000.00, 3.90, '2026-01-15'),
('University of Melbourne', 'Melbourne Research Scholarship', 'Ph.D.', 34000.00, 3.50, '2026-10-31'),
('National University of Singapore (NUS)', 'NUS Global Merit Scholarship', 'Bachelor''s', 25000.00, 3.85, '2026-02-15'),
('Seoul National University', 'SNU Global Scholarship', 'Master''s', 12000.00, 3.30, '2026-09-15'),
('Tsinghua University', 'Chinese Government Scholarship', 'Master''s', 15000.00, 3.20, '2026-03-01'),
('Technical University of Munich (TUM)', 'DAAD Excellence Scholarship', 'Master''s', 11000.00, 3.40, '2026-08-31'),
('University of Helsinki', 'Finland Scholarship', 'Master''s', 15000.00, 3.50, '2026-01-05'),
('Delft University of Technology', 'Justus & Louise van Effen Excellence', 'Master''s', 30000.00, 3.70, '2026-12-01'),
('KTH Royal Institute of Technology', 'KTH Scholarship', 'Master''s', 16000.00, 3.60, '2026-01-15'),
('ETH Zurich', 'Excellence Scholarship & Opportunity Program', 'Master''s', 24000.00, 3.80, '2026-12-15');

INSERT INTO Mentor (Mentor_Email, Full_Name, Current_Institution, Field_of_Study, Highest_Degree) VALUES
('dr.ahmed.ee@mentor.com', 'Dr. Ahmed Rahman', 'Massachusetts Institute of Technology', 'Electrical Engineering', 'Ph.D.'),
('sarah.chen.cs@mentor.com', 'Sarah Chen', 'University of Toronto', 'Computer Science', 'MSc'),
('david.miller.ds@mentor.com', 'Dr. David Miller', 'National University of Singapore', 'Data Science', 'Ph.D.'),
('elena.rostov@mentor.com', 'Elena Rostov', 'Technical University of Munich', 'Mechanical Engineering', 'MSc'),
('fatima.hossain@mentor.com', 'Dr. Fatima Hossain', 'University of Oxford', 'Artificial Intelligence', 'Ph.D.'),
('james.wilson@mentor.com', 'James Wilson', 'University of Melbourne', 'Software Engineering', 'MSc');

-- ==========================================
-- 5. POPULATE ADMISSION_REQUIREMENTS TABLE (12 Universities)
-- ==========================================
INSERT INTO Admission_Requirements (
    university_name, 
    minimum_cgpa, 
    IELTS_score_required, 
    TOEFL_score_required, 
    PTE_score_required, 
    GRE_score_required, 
    GMAT_score_required, 
    SAT_score_required, 
    documents_required
) VALUES
('Massachusetts Institute of Technology (MIT)', 3.80, 7.5, 100, 70, 325, 720, 1520, 'SOP, 3 LORs, Official Transcripts, CV, Research Proposal'),
('University of Oxford', 3.75, 7.5, 110, 76, 320, 690, 1480, 'SOP, 3 LORs, Official Transcripts, Academic Writing Sample'),
('University of Toronto', 3.50, 7.0, 100, 65, 310, 650, 1380, 'SOP, 2 LORs, Academic Transcripts, Resume'),
('University of Melbourne', 3.30, 6.5, 79, 58, 305, 630, 1300, 'SOP, 2 LORs, Academic Transcripts, Passport Copy'),
('National University of Singapore (NUS)', 3.60, 6.5, 85, 62, 320, 680, 1450, 'SOP, 2 LORs, Official Transcripts, CV'),
('Seoul National University', 3.20, 6.0, 80, 55, 300, 600, 1250, 'SOP, 2 LORs, Academic Transcripts, Personal Statement'),
('Tsinghua University', 3.30, 6.5, 85, 60, 305, 620, 1300, 'SOP, 2 Recommendation Letters, Academic Transcripts, Passport'),
('Technical University of Munich (TUM)', 3.20, 6.5, 88, 65, 310, 640, 1320, 'Motivation Letter, 2 LORs, VPD Document, Transcripts, CV'),
('University of Helsinki', 3.00, 6.5, 92, 62, 300, 600, 1280, 'Motivation Letter, Degree Certificate, Official Transcripts, Passport Copy'),
('Delft University of Technology', 3.40, 7.0, 100, 65, 315, 650, 1350, 'SOP, Summary of BSc Thesis, 2 LORs, Transcripts, Resume'),
('KTH Royal Institute of Technology', 3.10, 6.5, 90, 62, 305, 610, 1290, 'Cover Sheet, Summary Sheet, Degree Certificate, Transcripts, Passport'),
('ETH Zurich', 3.70, 7.0, 100, 68, 320, 700, 1450, 'SOP, 2 LORs, Official Course Descriptions, Transcripts, CV');