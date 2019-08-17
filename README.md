# openapi-SQLAlchemy
Translates an openapi schema to SQLAlchemy models. For example, given the following openapi specification:

```yaml
# example-spec.yml
openapi: "3.0.0"

info:
  title: Test Schema
  description: API to illustrate openapi-SQLALchemy MVP.
  version: "0.1"

paths:
  /employee:
    get:
      summary: Used to retrieve all employees.
      responses:
        200:
          description: Return all employees from the database.
          content:
            application/json:
              schema:
                type: array
                items:
                  "$ref": "#/components/schemas/Employee"

components:
  schemas:
    Employee:
      description: Person that works for a company.
      type: object
      x-tablename: employee
      properties:
        id:
          type: integer
          description: Unique identifier for the employee.
          example: 0
          x-primary-key: true
          x-autoincrement: true
        name:
          type: string
          description: The name of the employee.
          example: David Andersson.
          x-index: true
        division:
          type: string
          description: The part of the company the employee works in.
          example: Engineering
          x-index: true
        salary:
          type: number
          description: The amount of money the employee is paid.
          example: 1000000.00
      required:
        - id
        - name
        - division
```

The SQLALchemy models file then becomes:
```python
# models.py
from yaml import load, Loader
from sqlalchemy.ext.declarative import declarative_base
from openapi_sqlalchemy import init_model_factory


Base = declarative_base()
with open("example-spec.yml") as spec_file:
    SPEC = load(spec_file, Loader=Loader)
MODEL_FACTORY = init_model_factory(base=Base, spec=SPEC)


Employee = MODEL_FACTORY(name="Employee")

```

## Features
### Supported
The following features are supported:
- `integer ` (32 and 64 bit),
- `number` (float only),
- `boolean` and
- `string`.

### Not Supported
The following features are on the backlog:
- `allOf` inheritance,
- `$ref` references for columns,
- `$ref` references for models,
- foreign keys and
- relationships.

## Contributing
Fork and checkout the repository. To install:
```bash
python -m venv venv
python -m pip install -e .
```
To run tests:
```bash
tox
```
Make your changes and raise a pull request.
