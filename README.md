# HR Demo

## Description

HR backend with APIs for Applicants and Notes. Includes endpoints for viewing all applicants, applicants by id, creating applicants, updating applicant status, deleting applicants, leaving notes on specific applicants, and viewing an applicant's notes.

## Getting Started

### Building/Running

* Run `./scripts/up` from the root directory. This will pull/build the Postgres and Django container, and run migrations.
* Run `./scripts/teardown` from the root directory to stop and remove the containers.

### Tests

* Run `./scripts/test` from the root directory to run automated tests. 

* Manual testing
    * Run `./scripts/createtestusers` to create test users with different permissions for manual testing of API endpoints. This command will create the following users:
        |username       |password|permission      |
        |---------------|--------|----------------|
        |allperms       |password|all             |
        |viewapplicant  |password|view_applicant  |
        |createapplicant|password|create_applicant|
        |updateapplicant|password|update_applicant|
        |deleteapplicant|password|delete_applicant|
        |viewnote       |password|view_note       |
        |createnote     |password|view_note       |
    * Run `./scripts/deletetestusers` to remove these users from the DB when done testing.

### API Usage

* Applicant endpoints
    * List all applicants
        * GET `/api/applicant/`
        * Requires authenticated user with the `view_applicant` permission
    * List applicant by ID
        * GET `/api/applicant/<id>/`
        * Requires authenticated user with the `view_applicant` permission
    * Create an applicant
        * POST `/api/applicant/`
        * Requires authenticated user with the `create_applicant` permission
        * Body
            * `first_name`: `string`
            * `last_name`: `string`
            * `email`: `string`
            * `phone_number`: `string`
            * `address`: `string`
            * `zipcode`: `string`
            * `state`: `string`
    * Update an applicant's status
        * PUT `/api/applicant/<id>/`
        * Requires authenticated user with the `update_applicant` permission
        * Body
            * `status`: `string`
            * Valid values are `PENDING` `ACCEPTED` `REJECTED`
    * Delete an applicant
        * DELETE `/api/applicant/<id>/`
        * Requires authenticated user with the `delete_applicant` permission

* Note endpoints
    * List all notes on an applicant
        * GET `/api/applicant/<applicant_id>/note`
        * Requires authenticated user with the `view_note` permission
    * Create note on an applicant
        * POST `/api/applicant/<applicant_id>/note`
        * Requires authenticated user with the `create_note` permission
        * Body
            * `title`: `string`
            * `content`: `string`

