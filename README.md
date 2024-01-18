# CSHR (Codescalers HR Management System)

A comprehensive management system that provides a range of services, including the ability to submit vacation requests. This system seamlessly integrates with a global calendar, allowing users across all offices to view approved vacations collectively. Additionally, the calendar showcases Birthdates, Events, Meetings, and Holidays, offering a centralized and accessible overview for all users within the organization.

## Core Objectives

1. **Global Overview:**
   - Display a centralized calendar featuring approved vacations, holidays, events, meetings, and birthdays.
   - Search for users, view their public information, and identify their office affiliation.
   - Search for specific skillsets and identify users with those skills.

2. **Local Management:**
   - Appoint an admin for each location.
   - Restrict admin rights to the respective location without sharing across different locations.

## Access Levels

- **User:** Any individual affiliated with the organization.
- **TeamLead:** Each user has a designated teamLead.
- **Admin:** Location-specific administrators with defined responsibilities.

## Key Features

- **Global Calendar:** Track approved vacations and key events.
- **Vacation Requests:** Users can apply for vacations.
- **Approval/Denial Process:** Admins can manage and approve/deny vacation requests.
- **Document Requests:** Users can request documents from HR.
- **Evaluation Reminders:** Receive reminders for various evaluations.
- **Reporting:** Automatically generate comprehensive reports on-demand.

## Development Tools

Various tools are available for development:

- **Terraform Script:** Deploy two machines in the Threefold grid for frontend/backend. Refer to the script in [./terraform](./terraform/main.tf).
- **Testing Site Deployment:** Execute `make deploy` to deploy and `make destroy` to destroy the testing site.
- **Poetry environment:** After pressing `make install` Poetry will be installed. However, to complete the setup, it's crucial to add the Poetry executable to the system's PATH by running the command `export PATH="/root/.local/bin:$PATH"`

## Development Mode Commands

When in development mode, use the following Makefile commands:

- `make migrate`: Apply migration and migrate.
- `make user`: Create a superuser.
- `make runserver`: Run the server.
- `make lint`: Perform linting on both server and client.
- `make install`: Install dependencies in both client and server.
- `make data`: Create dummy data for testing e.g., users/offices.

## Implementation Details

- **Client:** Developed using Svelte. Note that the UI will transition to Vue3 in the future.
- **Server:** Implemented using Django.
- **Notification Service:** Requires a running Redis server for notification functionality.

## Project Configuration

After executing

```sh
make install && make migrate
```

Please refer to [.env.template](./config/.env.template) for all required values. Ensure all values are populated in the `.env` file within the [config](./config/) directory.
