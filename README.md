# Django Online Course Application

This repository contains the final project for the Django Application Development with SQL and Databases course. The project extends an existing online course platform by implementing a new assessment and exam evaluation feature.

## Features Implemented
* **Exam Models:** Added `Question`, `Choice`, and `Submission` models to the database schema to support multiple-choice assessments.
* **Admin Integration:** Registered the new models in the Django admin site using `StackedInline` to allow instructors to easily create and manage courses, lessons, and exams.
* **Assessment Views:** Developed views to handle exam submissions, calculate grades, and determine pass/fail status based on a passing threshold.
* **User Interface:** Updated the course detail templates using Django template tags and Bootstrap to display exam questions and render the final mock exam results.

## Technology Stack
* Python
* Django
* SQLite
* HTML / Bootstrap
