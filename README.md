# Banking System Simulation

This project is a simulation of a banking system designed to demonstrate essential features like user authentication, account management, transaction processing, and report generation, with a focus on learning system design fundamentals.

---

## Features

### Core Components:
- **User Authentication**: Supports secure internal and external user authentication with role-based access control.
- **Account Management**: Users can create, edit, and view accounts. Deletion of accounts is not supported to maintain integrity.
- **Transaction Processing**: Enables transactions between accounts owned by the same person, with validation to prevent unauthorized transfers.
- **Report Generation**: Provides reports on client transactions and registration history.

### Technologies Used:
- **MariaDB**: Relational database for storing user and transaction data.
- **Flask**: Backend web framework.
- **Redis**: Cache for storing lists of user accounts for quick access.
- **Docker Compose**: For orchestrating application services.

---

## Project Structure

### Key Directories & Files:
- **`compose.yml`**: Defines the Docker Compose configuration for the system.
- **`app/config/`**: Contains configuration files for the application.
  - `cache.toml`: Cache settings for Redis.
  - `db.toml`: Database connection settings for various modules.
  - `permissions.toml`: Role-based access permissions for endpoints.
  - `reports.toml`: Configuration for generating reports.
  - `security.toml`: Security settings, including the option to generate a random `SECRET_KEY`.
- **`app/src/`**: Contains the source code for various modules, including authentication, clients, external services, reports, and utilities.
- **`external-auth-service/`**: Mock external authentication service.

---

## Setup Instructions

### Prerequisites:
- [Docker](https://www.docker.com/) installed.
- [Docker Compose](https://docs.docker.com/compose/) installed.

### Steps to Run:
1. Clone this repository.
2. Navigate to the project directory.
3. Run the following command to start the application:
   ```bash
   docker-compose up --build
   ```
4. Access the application at `http://127.0.0.1:5000`.

---

## Configuration Details

### Role-Based Permissions:
Permissions are defined in `permissions.toml`. For example:
- Admins have full access to manage clients, generate reports, and view statistics.
- Managers have limited access to transaction-related data.
- Regular users can perform account transfers and view their own account details.

### Reports:
Reports are configured in `reports.toml`. Examples include:
- **Client History Report**: Monthly transaction details.
- **Client Registered Report**: Number of clients registered in a given month.

---

## Dependencies

The project requires the following Python packages:
- `mariadb`
- `flask`
- `gunicorn`
- `redis`
- `simplejson`
- `requests`

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## Security Notice

- The project allows the generation of a random `SECRET_KEY` during runtime to enhance security.
- External authentication is securely implemented through a dedicated service but communication between the monolith and the service is not encrypted.
- Database credentials in configuration files are not encrypted and are solely for demonstration purposes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
