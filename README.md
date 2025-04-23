# Lotto Report Generator

A command-line application that generates detailed reports for lotto game draws (6/42, 6/45, 6/49). This tool processes lotto entries, validates inputs, and produces reports such as all entries, tulog entries, winners, and wrong inputs.

---

## Features

- Parse and validate lotto entries from multiple owners
- Generate limited entries reports
- Generate "tulog" entries reports
- Identify and report winners based on winning numbers
- Report invalid or wrong input entries
- Supports multiple lotto game types (6/42, 6/45, 6/49)

---

## Setup

### Prerequisites

- Python 3.7 or higher
- `pip` package manager

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/514sh/lottov8.git
   cd lottov8
   ```

2. **Create a `.env` file in the project root directory**

   This file configures your environment variables. Add the following key-value pairs(Note! example values only):

   ```bash
   BASE_DIR=C:\Users\DIR
   PROJECT_DIR=C:\Users\lottov8
   OWNERS=user01,user02  # Comma-separated list of owners
   LIMIT=10              # Integer limit for entries
   ```

   - `BASE_DIR`: The base directory where input files reside and output reports will be saved.
   - `PROJECT_DIR`: The absolute path to the root directory of the lottov8 project
   - `OWNERS`: Comma-separated list of owners whose entries will be processed.
   - `LIMIT`: Maximum allowed bet for an entry.

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the application from the project root directory:

```bash
python app.py
```

You will be prompted with the following commands:

- **1** - Generate all entries list
- **2** - Generate tulog entries list
- **3** - Generate draw and winners entries list (you will be asked to input winning numbers)
- **4** - Report wrong input entries

Follow the on-screen instructions to generate the desired reports.

## Optional: Setup Base Directory and Input Files

If you need to set up the base directory or generate input filenames (for example, if they don’t exist yet), you can run:

```bash
python setup.py
```

---

## Project Structure

- `app.py` — Main CLI application entry point
- `setup.py` — setup the base directory.
- `lotto/` — Core modules handling interfaces, configuration, utilities, and lotto entries processing
- `requirements.txt` — Python dependencies
