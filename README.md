# Aurum - Student Assistant Application

  Aurum is a student assistant application designed to streamline learning and productivity for students at all levels. With features such as note-taking, task management, collaboration tools, and AI-driven capabilities, Aurum aims to enhance your study experience and keep you organized.

---

## Features

### 1. **Note-Taking & Categorization**
   - **Sticky Notes**: Easily jot down thoughts, reminders, goals, and logs. You can categorize your notes under 'Reminders', 'Goals', 'Thoughts', 'Logs', or 'Miscellaneous'.

   - **Lecture Notes**: Capture detailed notes during lectures, attach files, and organize them by course. Supports rich text formatting and real-time collaboration.


### 2. **Task Management**
   - **To-Do List**: Stay on top of your tasks by adding, editing, or deleting items. Mark tasks as completed and set deadlines for reminders.


### 3. **AI-Powered Features**
   - **Note Generation**: Automatically generate lecture notes or summaries based on audio, text, or images using the Gemini API.

   - **Transcription & Content Summarization**: Convert audio files into text or summarize long documents for easier study sessions.

### 4. **Collaboration Tools**
   - **Study Groups**: Create study groups for online communication and collaboration on lecture notes.

   - **Real-Time Editing**: Collaborate with others in real-time on lecture notes or sticky notes.

### 5. **Calendar & Reminder Integration**
   - **Calendar Sync**: Integrate with Google Calendar to manage your academic events, deadlines, and reminders seamlessly.

   - **Task and Note Integration**: Convert sticky notes or lecture notes into tasks with deadlines and reminders.

### 6. **Offline Functionality**
   - Notes and tasks are stored locally for offline access, ensuring you can always stay productive, regardless of internet connectivity.

---

## Getting Started

### Installation

1. **Clone the Repository**:
     ```bash
     git clone https://github.com/yourusername/aurum.git
     cd aurum
  
2. Set up a Virtual Environment:

      ```bash
      Copy code
      python3 -m venv venv
      source venv/bin/activate  # For Linux/macOS
      venv\Scripts\activate     # For Windows
      
3. Install Dependencies:

    ```bash
      Copy code
      pip install -r requirements.txt
4. Set Up the Database: Run the following command to apply database migrations:

      ```bash
      Copy code
      python manage.py migrate

5. Create a Superuser (optional, for accessing the admin panel):

      ```bash
      Copy code
      python manage.py createsuperuser

  6. Run the Development Server:

      ```bash
      Copy code
      python manage.py runserver

  7. Open your browser and visit http://127.0.0.1:8000 to access the application.

**Usage**

 - **Login & Registration:** Create an account using your email, and log in to access your dashboard. You can manage your notes, tasks, and     calendar events.

  - **Creating and Managing Notes:** Navigate to the Sticky Notes or Lecture Notes sections to create, edit, and organize your notes.

  - **To-Do List:** Track tasks and manage them by adding new tasks and marking them as complete when done.


  Aurum was created by:
  
     -divineinyang7@gmail.com - Divine Inyang.
     -sesethu.ngqwaru752@gmail.com - Zuri ngqwaru.
     -ethansevenster5@gmail.com - Ethan Sevenster.

  We are passionate about helping students stay organized, efficient, and focused


License
This project is licensed under the MIT License - see the LICENSE file for details

