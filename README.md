# AWS Lambda Demo

This is a demo application tha runs on AWS Lambda. See [this repo](https://github.com/diegosogari/aws-infra) for details on the infrastructure.

## Examples

### Unauthenticated

```shell
curl -X POST 'https://demo.sogari.dev' --data '{"name": "My Name"}' ^
    --header 'Content-Type: application/json'
```

Result:

```json
{"message": "Hello My Name!"}
```

### Authenticated

1. Sign-up or sign-in at https://demo.sogari.dev/login.
2. Get the cookie values obtained by your browser: `chrome://settings/cookies/detail?site=demo.sogari.dev`
3. Set cookies in HTTP header.

```shell
$COOKIE0='...'
$COOKIE1='...'
curl -X POST 'https://demo.sogari.dev' --data '{"name": "My Name"}' ^
    --header 'Content-Type: application/json' ^
    --header "Cookie: AWSELBAuthSessionCookie-0=$COOKIE0;AWSELBAuthSessionCookie-1=$COOKIE1"
```

Result:

```json
{"message": "Hello My Name!", "email": "<your email>"}
```

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

- [`request_handler.py`](request_handler.py): inbound adapter for the public API
- [`command_handler.py`](command_handler.py): inbound adapter for internal commands
- [`event_consumer.py`](event_consumer.py): inbound adapter for consuming domain events
- [`event_publisher.py`](event_publisher.py): outbound adapter for publishing domain events

Most of the business logic is contained in the subdirectories:

- [Model](model/README.md): classes that implement the domain model.
- [Proxies](proxies/README.md): outbound adapters for interacting with other services.
- [Repositories](repositories/README.md): outbound adapters for interacting with the database.
- [Sagas](sagas/README.md): classes that implement the saga pattern.
- [Services](services/README.md): classes that implement the application features.
