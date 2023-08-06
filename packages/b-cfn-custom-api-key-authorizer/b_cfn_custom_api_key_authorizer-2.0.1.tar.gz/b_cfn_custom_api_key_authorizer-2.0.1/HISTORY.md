# Release history

### 2.0.1

* Dollar sign excluded from API secret.

### 2.0.0

* Restructured project.
* All lambda functions are under `functions` directory.
* Add `deleter` function to revoke api keys.
* Add `exists` function to check whether given api key exists.
* Add `validator` function to validate api key and api secret.
* Increase the length of api key (15) and api secret (30).
* Move authentication checking logic to a lambda layer.
* Add more lambda-level logging.
* Add more integrations tests (total 11 as of now).
* **Very important security improvement** - api secrets are now hashed, to avoid
  leaks if the database is pawned. This is a standard password-level storage security.
* Greatly improve documentation.

### 1.1.0

* Create a dedicated lambda function to generate
  api keys. You should not interact with the database directly.

### 1.0.0

* Prod-ready version.
* Added documentation.
* Added more tests.
* Some code improvements.

### 0.1.0

* Initial testing done. Authorizer works.
* Need more tests and edge case handling before promoting to 1.0.0.

### 0.0.1

* Initial build.
