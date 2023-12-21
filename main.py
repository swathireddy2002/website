from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:swathi2002@localhost:3306/demodb"  # Replace with your database URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Nam(Base):
    __tablename__ = "nam"

    student_name = Column(String(100), primary_key=True, index=True)

class Details(Base):
    __tablename__ = "details"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(100))


Base.metadata.create_all(bind=engine)

certificate_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Course Completion Certificate</title>
    <style>
        /* Add some styles for the certificate */
        body {
            font-family: Arial, sans-serif;
            text-align: center;
        }
        .certificate {
            border: 10px solid orange; /* Add an additional 5px solid orange border */
            padding: 140px;
            width: 60%;
            margin: 20px auto 50px;
            position: relative;
            box-sizing: border-box; /* Include padding and border in the total width and height */
        }


        .logo {
            position: absolute;
            top: 10px;
            right: 10px;
            max-width: 100px; /* Set the maximum width for the logo */
            height: auto; /* Maintain the aspect ratio */
            margin-bottom: 10px; /* Add some space below the logo */
            display: inline-block;
        }


        .course {
            font-size: 24px;
            margin-bottom: 20px;
            color: darkblue; /* Set dark blue color for course name */
            font-weight: bold; /* Make course name bold */
        }
        .student {
            font-size: 20px;
            /* Highlight only the name "Gunda" in red */
            color: black;
        }
        .date-signature {
            display: flex; /* Use flexbox for layout */
            justify-content: space-between; /* Space between date and signature */
            margin-top: 20px; /* Add some space between sections */
        }
        .date, .signature {
            width: 45%; /* Set the width for date and signature */
            /* Add a border between date and signature */
            padding-top: 10px; /* Add some space above text */
            margin-right: 50px;
            color: black; /* Set date and signature color to black */
        }
        .certificate img {
            max-width: 100px; /* Set the maximum width for the logo */
            height: auto; /* Maintain the aspect ratio */
            margin-bottom: 10px; /* Add some space below the logo */
        }
    </style>
</head>
<body>
    <div class="certificate">
        <!-- Use the correct path for the image -->
        <img class="logo" src="/static/logo.png" alt="Logo">


        <h2>Certificate of Completion</h2>


        <div class="student">
            This is to certify that <br/><br/>
            <span style="color: red;">Gunda</span> <br/><br/> <!-- Highlight only the name "Gunda" in red -->
            has successfully completed <br/><br/>
            <span class="course">Full Stack Developer</span> <!-- Set dark blue color for course name -->
        </div>
        <br/>
        <br/>
        <br/>


        <!-- Add date and signature -->
        <div class="date-signature">
            <div class="date">
                Date: <!-- Replace with the actual date -->
            </div>
            <div class="signature">
                Signature: <!-- Add a line for a signature -->
            </div>
        </div>
    </div>
</body>
</html>
"""


@app.get("/certificate/{student_name}")
async def generate_certificate(student_name: str):
    db = SessionLocal()
    student = db.query(Nam).filter(Nam.student_name == student_name).first()
    db.close()

    if student:
        # Replace placeholders in the certificate template with the fetched student name
        certificate = certificate_template.replace("Gunda", student.student_name)

        # Return the HTML response with the updated certificate
        return HTMLResponse(content=certificate)
    else:
        return HTMLResponse(content="No student found in the database")
    
@app.get("/student_names/", response_model=List[str])
async def get_student_names():
    db = SessionLocal()
    # Fetch all student names from the 'details' table
    students = db.query(Details.student_name).all()
    db.close()

    # Extract the student names from the query result and return as a list
    student_names = [student.student_name for student in students]
    return student_names