Nexus Appointment Checker ✈️

This application is designed for anyone looking to snag an earlier Nexus appointment without refreshing the TTP portal all day. Whether you're a seasoned dev or just installed your first terminal, this guide is for you.

🛠 Prerequisites

1. Get a Linux Environment

On Mac: You're already set.

On Windows: You'll need WSL 2 (Windows Subsystem for Linux).

Open PowerShell as Administrator.

Run wsl --install.

Pro-tip: If it feels stuck, give it 15 minutes. Good things take time.

2. Install Python & Dependencies

Open your terminal and run:

sudo apt update && sudo apt install python3 python3-pip
pip install requests python-dotenv


🚀 Getting Started

1. Configure your Credentials

The script needs to know who you are and what date you're trying to beat. Create a file named .env in the root folder:

NEXUS_PASSWORD=your_gmail_app_password
NOTIFICATION_EMAIL=your_email@gmail.com
MAX_DATE=2099-12-31T12:00:00


Note: If you are using Gmail, you MUST use an "App Password," not your regular login password.

2. Run the Script

Execute the following in your terminal:

python3 nexus_checker.py


If successful, you’ll see:
{'message': 'Notification sent.'}

⏲ Running on a Schedule

You probably don't want to click "run" every 10 minutes. The best way to automate this is via Crontab:

Type crontab -e in your terminal.

Add this line to run it every 15 minutes:

*/15 * * * * /usr/bin/python3 /path/to/your/nexus_checker.py


🤝 Contributing

I may be missing some things! If you have ideas (like adding a default while loop or better error handling), please feel free to open a Pull Request.
