# CSHR (Codescalers HR Management System)

CSHR is designed to be a comprehensive HR management system that seamlessly integrates both localized management and global oversight. The system caters to organizations with multiple offices, facilitating a unified approach for the entire organization, while also allowing for location-specific administrative controls.

## Key Objectives

1. **Global Overview:**
   - Share a centralized calendar displaying approved vacations, holidays, events, meetings and birthdays.
   - Search for users and view their public information and which office they belong to.
   - Search for a specific skillset and identify all users possessing that skill.

2. **Local Management:**
   - Appoint an admin for each location.
   - Admin rights are restricted to the respective location and are not shared across different locations.

## Access Levels

- **User:** Any individual affiliated with the organization.
- **Supervisor:** Each user has a designated supervisor.
- **Admin:** Location-specific administrators with defined responsibilities.

## CSHR Features

- **Global Calendar:** Track approved vacations and key events.
- **Vacation Requests:** Users can apply for vacations.
- **Approval/Denial Process:** Admins can approve or deny vacation requests.
- **Document Requests:** Users can request documents from HR.
- **Evaluation Reminders:** Receive reminders for various evaluations.
- **Reporting:** Automatically and on-demand generate comprehensive reports.

## Development Tools

Several tools are available for development:

- **Terraform Script:** Deploy two machines in the Threefold grid for frontend/backend. Refer to the script in [./terraform](./terraform/main.tf).
- **Testing Site Deployment:** Execute `make deploy` to deploy and `make destroy` to destroy the testing site.

## Development Mode Commands

In development mode, use the following Makefile commands:

- `make migrate`: Apply migration and migrate.
- `make user`: Create a super user.
- `make runserver`: Run the server.
- `make lint`: Perform linting on both server and client.
- `make install`: Install dependencies in both client and server.
- `make data`: Create a dummy data for testing e.g. users/offices.

## Implementation Details

- **Client:** Developed using Svelte. Note that the UI will transition to Vue3 in the future.
- **Server:** Implemented using Django.
- **Notification Service:** Requires a running Redis server for notification functionality.
