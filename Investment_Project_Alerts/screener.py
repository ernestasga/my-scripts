import sqlite3
import requests
from datetime import datetime
import smtplib
import email.message
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

class ProfitusProjectScreener:
    url = "https://api.profitus.com/api/v1/landing/projects?limit=2&page=1"

    def get_featured_projects(self) -> List[dict]:
        response = requests.get(self.url)
        raw_projects = response.json()['data']
        projects = [{
            'name': project['project_name'],
            'status': project['status'],
            'interest_rate': project['basic_interest'],
            'percentage_invested': project['invested_amount'] / project['required_amount'] * 100,
            'preview_url': project['preview_url'],
            'platform': 'Profitus',
            'last_updated': datetime.now().timestamp()
        } for project in raw_projects]
        return projects

class NewInvestmentProjectScreener:
    conn = None
    smtp_config = None
    mailer_recipients = []

    def __init__(self):
        load_dotenv()
        self.smtp_config = {
            "host": os.environ.get('MAILER_HOST'),
            "port": os.environ.get('MAILER_PORT'),
            "username": os.environ.get('MAILER_USERNAME'),
            "password": os.environ.get('MAILER_PASSWORD')
        }
        self.mailer_recipients = os.environ.get('EMAIL_RECIPIENTS')
        self.conn = self.setup_database_connection()

    def setup_database_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect('projects.db')
        # create table if not exists
        conn.execute('''
            CREATE TABLE IF NOT EXISTS PROJECTS (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                status TEXT,
                interest_rate REAL,
                percentage_invested REAL,
                preview_url TEXT,
                platform TEXT,
                last_updated TIMESTAMP
            )
        ''')
        return conn

    def fetch_database_projects(self) -> List[dict]:
        cursor = self.conn.execute("SELECT * from PROJECTS")
        projects = cursor.fetchall()
        projects_list = []
        for project in projects:
            project_dict = {
                "id": project[0],
                "name": project[1],
                "status": project[2],
                "interest_rate": project[3],
                "percentage_invested": project[4],
                "preview_url": project[5],
                "platform": project[6],
                "last_updated": project[7]
            }
            projects_list.append(project_dict)
        return projects_list

    def save_projects_to_database(self, projects: List[dict]) -> None:
        for project in projects:
            self.conn.execute(
                "INSERT INTO PROJECTS (name, status, interest_rate, percentage_invested, preview_url, platform, last_updated) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (project['name'], project['status'], project['interest_rate'], project['percentage_invested'], project['preview_url'], project['platform'], project['last_updated'])
            )
            self.send_alert(project)
        self.conn.commit()

    def build_email_message(self, project: dict) -> email.message.Message:
        msg = MIMEMultipart('alternative')
        text = f"""
            A new project has been added to {project['platform']}.\n
            Hurry up and invest before you miss it.\n\n
            Platform:             {project['platform']}\n  
            Project name:         {project['name']}\n
            Base interest rate:   {project['interest_rate']}%\n
            Percentage invested:  {project['percentage_invested']}%\n
        """
        html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>New Project Alert</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                    }}
                    .project-table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin-top: 20px;
                    }}
                    .project-table th, .project-table td {{
                        border: 1px solid #ccc;
                        padding: 8px;
                        text-align: left;
                    }}
                    .project-table th {{
                        background-color: #f5f5f5;
                    }}
                </style>
            </head>
            <body>
                <h2>New Project Alert</h2>
                <p>A new project has been added to <strong>{project['platform']}</strong>.</p>
                <p>Hurry up and invest before you miss it.</p>
                
                <table class="project-table">
                    <tr>
                        <th>Platform</th>
                        <td>{project['platform']}</td>
                    </tr>
                    <tr>
                        <th>Project name</th>
                        <td><a href="{project['preview_url']}">{project['name']}</a></td>
                    </tr>
                    <tr>
                        <th>Base interest rate</th>
                        <td>{project['interest_rate']}%</td>
                    </tr>
                    <tr>
                        <th>Percentage invested</th>
                        <td>{project['percentage_invested']}%</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))
        msg['From'] = f"Investment Alert <{self.smtp_config['username']}>"
        msg['To'] = self.mailer_recipients
        msg['Subject'] = f"New project on {project['platform']}"

        return msg

    def setup_email_connection(self) -> smtplib.SMTP:
        connection = smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port'])
        connection.starttls()
        connection.login(self.smtp_config['username'], self.smtp_config['password'])
        return connection
    
    def send_alert(self, project: dict) -> None:
        try:
            msg = self.build_email_message(project)
            connection = self.setup_email_connection()
            connection.send_message(msg)
            connection.quit()
            print("Sent email")
        except Exception as e:
            print("Failed to send email")
            print(e)

if __name__ == "__main__":
    investment_screener = NewInvestmentProjectScreener()
    profitus_screener = ProfitusProjectScreener()

    profitus_projects = profitus_screener.get_featured_projects()
    # Check current databased records
    database_projects = investment_screener.fetch_database_projects()
    # Combine all projects
    projects = profitus_projects
    # Check if new projects appeared
    new_projects = [project for project in projects if project['name'] not in [project['name'] for project in database_projects]]
    # New projects found. Insert into database and send an alert
    if len(new_projects) > 0:
        print(f"{len(new_projects)} new projects found")
        investment_screener.save_projects_to_database(new_projects)
    # No new projects
    if len(new_projects) == 0:
        print("No new projects")

