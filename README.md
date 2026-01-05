# Local Ticketing System (Python + Tkinter)

## Overview
The **Local Ticketing System** is a lightweight, desktop-based application built with **Python** and **Tkinter** that enables individuals or small teams to manage tickets locally without relying on internet connectivity or external services.

The application is designed to be **simple, adaptable, and extensible**, making it suitable for use cases such as IT helpdesks, customer support desks, internal service requests, or small business issue tracking.

---

## Key Features
- Create and manage tickets through a graphical user interface
- Store tickets **locally** using SQLite (no external database required)
- Auto-generated ticket IDs
- Ticket attributes:
  - Title
  - Description
  - Category
  - Priority
  - Status (Open, In Progress, Closed)
  - Creation timestamp
- Update ticket status
- Delete tickets with confirmation
- Persistent storage across application restarts

---

## Technology Stack
- **Python 3**
- **Tkinter** – desktop graphical user interface
- **SQLite3** – embedded local database

All technologies used are included with standard Python installations.

---

## Installation & Setup

### Prerequisites
- Python 3.9 or later

### Steps
1. Clone or download the project files.
2. Ensure the main Python file is in a writable directory.
3. Run the application:

```bash
python ticketing_system.py
