# Modern Process Viewer

A simple yet powerful tool to monitor running processes and view event logs on Windows systems. This application allows you to:

- List and manage running processes, with the ability to terminate untrusted processes.
- View event logs from various sources such as the system, application, security, and more.
- Handle tasks such as checking if the application is running with administrator privileges and providing feedback to the user.

## Features

- **Process List**: View a list of all running processes, including details such as PID, CPU usage, memory usage, executable path, and status. 
- **Terminate Processes**: Select and terminate untrusted processes directly from the interface.
- **Event Logs**: View event logs of different types (System, Application, Security, etc.) and display event sources and messages.
- **Admin Privileges Check**: Ensure that the application is running with the necessary administrative privileges for proper functionality.
- **User-Friendly Interface**: Built with Tkinter for a clean and intuitive user experience.

## Requirements

- Python 3.x
- `psutil` package (for process management)
- `pywin32` package (for event log access)
- Windows Operating System

## Download

You can download the precompiled `.exe` file from the following link:

[Download Modern Process Viewer (.exe)]([https://github.com/ahmetozer27/SystemTracker/tree/main/exe_format/v1.0](https://github.com/ahmetozer27/SystemTracker/archive/refs/tags/v1.0.zip))

## Installation

### Step 1: Install Dependencies

To get started, first, ensure you have Python installed. Then, install the required dependencies by running:

```bash
pip install psutil pywin32
```




