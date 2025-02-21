# Data Submission Portal

A Django-based web application for collecting and managing training data entries, built as an internship task. This project leverages Django for backend logic, HTMX for dynamic frontend updates, and Tailwind CSS for styling. It includes a submission form, a data table with filtering and pagination, a review workflow, and category reporting.

## Features

- **Data Submission**: Add new entries via a form (text or image URLs).
- **Data Table**: View entries with pagination (10 per page), category filtering, and search.
- **Review Workflow**: Toggle "Reviewed" status for entries using HTMX for seamless updates.
- **Reporting**: Displays total entries per category (e.g., "Text: 30, Image: 20").
- **Bonus Features**: Search bar, pagination, and full HTMX integration.

## Setup Instructions

### Clone the Repository

```sh
git clone <repository-url>
cd data-submission-portal
```

### Create a Virtual Environment

It's recommended to create a virtual environment to manage dependencies.

```sh
python -m venv venv
```

### Activate the Virtual Environment

#### On Windows:

```sh
venv\Scripts\activate
```

#### On macOS/Linux:

```sh
source venv/bin/activate
```

### Install Dependencies

Install the required Python packages using pip.

```sh
pip install -r requirements.txt
```

### Run Migrations

Apply the database migrations to set up the necessary tables.
```sh
python manage.py makemigrations
```

```sh
python manage.py migrate
```

### Seed the Database (Optional)

If you want to populate the database with sample data, you can use the `seed_data.py` script.

```sh
python manage.py seed_data.py
```

### Run the Development Server

Start the Django development server to run the application locally.

```sh
python manage.py runserver
```

