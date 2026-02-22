# Home App -- Architecture Convention

## Overview

This app follows a clean, layered architecture inside Django.

Directory structure:

apps/home/ ├── presentation/ ├── application/ ├── persistence/ ├──
infrastructure/ ├── admin.py ├── apps.py └── migrations/

------------------------------------------------------------------------

1)  Presentation Layer (presentation/)

Purpose: Handles HTTP requests and responses.

Allowed: - Read request data - Validate forms - Call application
services - Return templates or API responses

Not allowed: - Direct ORM usage - External API calls - Business logic

------------------------------------------------------------------------

2)  Application Layer (application/)

Purpose: Contains use cases and business orchestration.

Allowed: - Call repositories - Call infrastructure clients - Coordinate
workflows - Return DTOs

Not allowed: - Direct ORM usage - HTTP-specific logic - Template
rendering

------------------------------------------------------------------------

3)  Persistence Layer (persistence/)

Purpose: Database access only.

Allowed: - Django ORM - QuerySets - update_or_create - Migrations

Not allowed: - Business rules - External API calls

------------------------------------------------------------------------

4)  Infrastructure Layer (infrastructure/)

Purpose: External system integrations and technical adapters.

Examples: - API clients - Authentication handlers - Message queues -
File connectors

Not allowed: - Business decisions - ORM access

------------------------------------------------------------------------

Data Flow Rule

View -\> Service (Use Case) -\> Repository / External Client -\> Service
-\> View

Never:

View -\> ORM View -\> External API

------------------------------------------------------------------------

Decision Table

Question -\> Layer -------------------------------------- -\>
------------- How do I render this? -\> presentation What should happen?
-\> application How do I store this? -\> persistence How do I call
system X? -\> infrastructure

------------------------------------------------------------------------

Feature Workflow

1)  Define DTO in application/dto.py
2)  Implement use case in application/services.py
3)  Extend repository if needed
4)  Extend infrastructure client if needed
5)  Connect via presentation layer

------------------------------------------------------------------------

This structure ensures maintainability, testability, and clear
separation of concerns.
