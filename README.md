# AWS Lambda Demo

This is a demo application tha runs on AWS Lambda.

## Stack

- `Python`: the programming language used for the code.
- `AWS Lambda`: serverless computing platform that runs the code.
- `Amazon DynamoDB`: NoSQL database that stores domain events and resource snapshots.
- `Amazon SNS`: publish/subscribe topics where domain events are published.
- `Amazon S3`: object storage that stores the packaged code and dependencies.
- `Amazon ELB`: load-balancing solution that serves as entry-point for the public API.
- `Amazon CloudWatch`: monitoring platform that collects and tracks metrics and logs.
- `Amazon Cognito`: customer identity platform that keeps user sign-in info and provides authentication flows.
- `OAuth` and `JWT`: standards used for delegating access and representing user claims in the authentication flow.

## Structure

The top-level directory is where the lambda functions live:

- `request_handler`: inbound adapter for the public API
- `command_handler`: inbound adapter for internal commands
- `event_consumer`: inbound adapter for consuming domain events
- `event_publisher`: outbound adapter for publishing domain events

Most of the business logic is contained in the subdirectories:

- [Model](model/README.md): classes that implement the domain model.
- [Proxies](proxies/README.md): outbound adapters for interacting with other services.
- [Repositories](repositories/README.md): outbound adapters for interacting with the database.
- [Sagas](sagas/README.md): classes that implement the saga pattern.
- [Services](services/README.md): classes that implement the application features.