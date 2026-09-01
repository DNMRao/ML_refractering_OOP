#!/usr/bin/env python
# coding: utf-8

# # **Pydantic**
# 
# **Pydantic** is the most widely used **data validation library** for Python.
# 
# Based on the [official documentation](https://docs.pydantic.dev/):
# 
# > "Pydantic is used for data validation and settings management using Python type annotations.  
# > Pydantic enforces type hints at runtime, and provides user-friendly errors when data is invalid.  
# > Define how data should be in pure, canonical Python; validate it with Pydantic."
# 
# ### **What does this mean?**
# The working principle of the library is very simple:  
# 
# We define classes with **type annotations** that reflect how the data should be structured. Then, when we receive some data that we don’t trust (e.g. the JSON body of an HTTP request), we simply use the classes we defined for parsing and validation.
# 
# One advantage of using Pydantic is that **the parsed data structures will be instances of the classes we defined**.
# 
# For more information about type hints in Python, you can check this [cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html).
# 
# 
# #### Example
# 
# In order to define an object in Pydantic we can create **models**. The term model in this case has nothing to do with our well-known ML models. Models in the context of Pydantic are simply classes which inherit from a `BaseModel` class.  
# 
# When you create a new object from the class, Pydantic guarantees that the fields of the resultant model instance will conform to the field types defined on the model.
# 
# Let's define a new class which inherits from the `BaseModel`.
# 

# ### **Pydantic Validation Flow**
# 
# ```mermaid
# flowchart TD
#     A[Incoming raw dictionary] --> B[Define BaseModel + field types]
#     B --> C[Run model_validate]
#     C --> D{Valid input?}
#     D -- Yes --> E[Use typed model instance]
#     D -- No --> F[Handle ValidationError]
# ```
# 

# In[ ]:


# Standard library imports
from datetime import datetime
from typing import Annotated

# Pydantic imports used throughout this notebook
from pydantic import (
    BaseModel,
    Field,
    NegativeInt,
    PositiveInt,
    StrictBool,
    StringConstraints,
    ValidationError,
    field_validator,
    model_validator,
)


class User(BaseModel):
    # Required fields
    id: int
    username: str
    password: str
    confirm_password: str

    # Optional field with default value
    timestamp: datetime | None = None

    # Use default_factory for mutable defaults
    friends: list[int] = Field(default_factory=list)


# `User` in our case is a model with six fields. Pydantic uses the **built-in type hinting syntax** to determine the data type of each variable.  
# 
# Let’s explore one by one what happens behind the scenes:
# 
# - `id` — An integer variable representing an ID. Since no default value is provided, this field is required and must be specified during object creation. Strings, bytes or floats will be coerced to integer if possible; otherwise, an exception will be raised.
# 
# - `username` — A string variable representing a username. It is required.
# 
# - `password` — A string variable representing a password. It is required.
# 
# - `confirm_password` — A string variable representing a confirmation password. It is required and will be used for **data validation** later on.
# 
# - `timestamp` — A date/time field, which is not required (defaults to `None`). Pydantic will process either a Unix timestamp (`int`) or a string representing the date/time.
# 
# - `friends` — A list of integer inputs.
# 
# ##### **Object instantiation**
# 
# The next step is to **instantiate** a new object from the `User` class:
# 

# In[ ]:


# Simulate raw external input (e.g. from an API request body)
external_data = {
    "id": "123",  # String input will be coerced to int
    "username": "John Doe",
    "password": "Password1234",
    "confirm_password": "Password1234",
    "timestamp": "2026-06-01 12:22",  # Parsed into datetime
    "friends": [1, "2", b"3"],  # Mixed inputs coerced to ints
}

# Validate + parse into a typed `User` instance
user = User.model_validate(external_data)


# You should get the following output when you print out the `user` variable:
# 

# In[ ]:


# Observe parsed values and their runtime types
print(user.id)
print(type(user.id))

print(repr(user.timestamp))

print(user.friends)
print(type(user.friends[1]))
print(type(user.friends[2]))

# Convert model back to a standard dictionary
print(user.model_dump())


# ### **Type Coercion: Converting input to match field types**
# 
# Notice something important happened: **Pydantic automatically converted data types** to match what the `User` model declared.
# 
# #### **What is type coercion?**
# 
# Type coercion is the process of **automatically converting a value from one type to another**. In the example above:
# 
# - `"123"` (string) → `123` (integer) for the `id` field
# - `"2"` (string) → `2` (integer) in the `friends` list  
# - `b"3"` (bytes) → `3` (integer) in the `friends` list
# - `"2026-06-01 12:22"` (string) → `datetime(2026, 6, 1, 12, 22)` for the `timestamp` field
# 
# #### **Why does Pydantic do this?**
# 
# External data—like JSON from an API request or a CSV file—almost always arrives as **strings**. Rather than forcing you to convert everything manually before validation, **Pydantic intelligently coerces compatible types**.
# 
# Here's the workflow:
# 
# 1. Pydantic reads your field type declaration (e.g. `id: int`)
# 2. Raw input arrives (e.g. `{"id": "123", ...}`)
# 3. Pydantic tries to convert the input to match the declared type
#    - String `"123"` → Can be converted to int `123`? Yes! ✓
#    - String `"random string"` → Can be converted to int? No! ✗ → Raises `ValidationError`
# 4. If successful, you get a typed model instance with the correct types
# 
# #### **The benefit:**
# 
# You never have to write boilerplate code like `int(data["id"])` or `datetime.fromisoformat(data["timestamp"])`. Pydantic handles this automatically and consistently across all fields.
# 

# ### **Methods and Attributes under `BaseModel`**
# 
# Classes that inherit the `BaseModel` will have the following methods and attributes:
# 
# - `model_dump()` — Returns a dictionary of the model’s fields and values.  
# - `model_dump_json()` — Returns a JSON string representation of the model’s fields and values.  
# - `model_copy()` — Returns a (by default shallow) copy of the model.  
# - `model_validate()` — A utility for loading any object into a model with error handling if the object is not a dictionary.  
# - `model_validate_json()` — Parses and validates data from a JSON string.  
# - `model_json_schema()` — Returns a dictionary representing the model as JSON schema.  
# - `model_construct()` — A class method for creating models without running validation.  
# - `model_fields_set` — Set of names of fields which were set when the model instance was initialized.
# - `model_fields` — A dictionary of the model’s fields.
# 
# 
# Let’s change the input for `id` to a string as follows:
# 

# In[ ]:


external_data = {
    "id": "random string",
    "username": "John Doe",
    "password": "Password1234",
    "confirm_password": "Password1234",
    "timestamp": "2026-06-01 12:22",
    "friends": [1, "2", b"3"],
}

try:
    user = User.model_validate(external_data)
except ValidationError as error:
    print(error)


# You should get a **ValidationError** when you run the previous code.
# 
# ### **ValidationError**
# 
# To inspect the error details in a cleaner format, wrap validation in a **try–except** block:

# In[ ]:


# Invalid payload: `id` cannot be parsed as int
external_data = {
    "id": "random string",
    "username": "John Doe",
    "password": "Password1234",
    "confirm_password": "Password1234",
    "timestamp": "2019-06-01 12:22",
    "friends": [1, "2", b"3"],
}

# Catch and inspect structured Pydantic validation output
try:
    user = User.model_validate(external_data)
except ValidationError as error:
    print(error.json())


# It will print out a JSON object with the **error message**, which indicates that the input for `id` is not a valid integer.

# ### **Field Types**
# 
# Pydantic provides support for most of the common types from the Python standard library, but it also provides a variety of other useful types.  
# 
# The full list can be found in the [documentation](https://docs.pydantic.dev/latest/concepts/types/).

# ### **Constrained Types**
# 
# You can enforce your own **restrictions** via the `Constrained Types`.  
# 
# Let’s have a look at the following example:

# In[ ]:


class Model(BaseModel):
    # String with minimum length of 2 and maximum length of 10
    short_str: Annotated[str, StringConstraints(min_length=2, max_length=10)]

    # Regex
    regex_str: Annotated[
        str,
        StringConstraints(pattern=r"^apple (pie|tart|sandwich)$"),
    ]

    # Remove whitespace from string
    strip_str: Annotated[str, StringConstraints(strip_whitespace=True)]

    # Value must be greater than 1000 and less than 1024
    big_int: Annotated[int, Field(gt=1000, lt=1024)]

    # Value is multiple of 5
    mod_int: Annotated[int, Field(multiple_of=5)]

    # Must be a positive integer
    pos_int: PositiveInt

    # Must be a negative integer
    neg_int: NegativeInt

    # List of integers that contains 1 to 4 items
    short_list: Annotated[list[int], Field(min_length=1, max_length=4)]


# ### **Exercise 1: Validate constrained model input**
# 
# Create a dictionary with values for all fields in the `Model` class and instantiate a valid model instance.
# Then create one invalid input and confirm that validation raises an error.

# In[ ]:


# Bad example
bad_model_data = {
    "short_str": "h",  # Too short (min_length=2)
    "regex_str": "banana pie",  # Does not match required pattern
    "strip_str": "  keep me  ",
    "big_int": 999,  # Must be >1000
    "mod_int": 14,  # Must be a multiple of 5
    "pos_int": -5,
    "neg_int": 3,
    "short_list": [],
}

try:
    Model.model_validate(bad_model_data)
except ValidationError as error:
    print("Expected validation errors:")
    print(error)


# In[ ]:


# @TODO: Build a dictionary that satisfies `Model` and instantiate it.
# 1) Create `model_data` with valid values for every field in `Model`.
# 2) Instantiate: `valid_model = Model.model_validate(model_data)`.
# 3) Create one invalid example and observe the validation error.

# Write your refactor below.


# #### Example Solution

# In[ ]:


# Difference vs bad example: valid data passes cleanly; invalid data is handled explicitly.
# 1) Build a valid payload for all constrained fields.
model_data = {
    "short_str": "hello",
    "regex_str": "apple pie",
    "strip_str": "  trimmed  ",
    "big_int": 1010,
    "mod_int": 15,
    "pos_int": 5,
    "neg_int": -3,
    "short_list": [1, 2, 3],
}

# 2) Validate and get a typed model instance.
valid_model = Model.model_validate(model_data)
print(valid_model)

# 3) Mutate one field to an invalid value and show the error.
invalid_model_data = dict(model_data)
invalid_model_data["big_int"] = 999

try:
    Model.model_validate(invalid_model_data)
except ValidationError as error:
    print("Expected validation error:")
    print(error)


# ### **Strict Types**
# 
# If you are looking for **rigid restrictions** that pass validation only if the value is already of the expected type (or a subtype), you can use strict types:
# 
# - `StrictStr`
# - `StrictInt`
# - `StrictFloat`
# - `StrictBool`
# 
# The following example illustrates how to enforce `StrictBool` in a model:

# In[ ]:


# StrictBool forbids coercion from strings like "True"
class StrictBoolModel(BaseModel):
    strict_bool: StrictBool


# In[ ]:


# This fails because the value is a string, not a real boolean
try:
    strictboolmodel = StrictBoolModel.model_validate({"strict_bool": "True"})
except ValidationError as error:
    print(error)


# The string `"True"` will raise a `ValidationError` because `StrictBool` accepts only `True` or `False` as real boolean values. Try writing the same model without `StrictBool` and compare the behavior.
# 

# ### **Validator (Pydantic v2)**
# 
# You can create **custom validators** using `@field_validator` and `@model_validator` in your model class.  
# 
# The following example validates that:
# 
# - `id` is exactly four digits
# - `confirm_password` matches `password`

# In[ ]:


class User(BaseModel):
    id: int
    username: str
    password: str
    confirm_password: str
    timestamp: datetime | None = None
    friends: list[int] = Field(default_factory=list)

    # Field-level validator: runs for `id` after parsing
    @field_validator("id")
    @classmethod
    def id_must_be_4_digits(cls, user_id: int) -> int:
        if len(str(user_id)) != 4:
            raise ValueError("Must be 4 digits")
        return user_id

    # Model-level validator: checks relationships between fields
    @model_validator(mode="after")
    def check_passwords_match(self) -> "User":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


# ### **Exercise 2: Build and validate a `Person` model**
# 
# Create a Pydantic model called `Person` with the following fields:
# 
# - `name`: a string with a maximum length of 50 characters
# - `age`: an integer between 18 and 120 (inclusive)
# - `email`: a value matching an email-like format
# 
# Then create a function called `create_person` that takes a dictionary with keys `name`, `age` and `email`, and returns a validated `Person` object.
# 
# Expected behavior:
# - Valid input returns a `Person` instance.
# - Invalid input raises a validation error.

# In[ ]:


# Bad example
# No structured validation: plain dict can contain invalid values unnoticed.
person_data = {"name": "A" * 70, "age": 12, "email": "not-an-email"}
print(person_data)


# In[ ]:


# @TODO: Implement the `Person` model and `create_person` function.
# 1) Define `Person` with `name`, `age` and `email` constraints.
# 2) Implement `create_person(data: dict) -> Person` using model validation.
# 3) Test with one valid dictionary and one invalid dictionary.

# Write your refactor below.


# #### Example Solution

# In[ ]:


# Difference vs bad example: schema constraints make invalid input fail early.
class Person(BaseModel):
    # Keep names concise and capped in length
    name: Annotated[str, StringConstraints(max_length=50)]
    # Allow only adult ages in a realistic range
    age: Annotated[int, Field(ge=18, le=120)]
    # Basic email pattern check for teaching purposes
    email: Annotated[
        str,
        StringConstraints(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$"),
    ]


def create_person(data: dict) -> Person:
    # Centralize model creation + validation in one function
    return Person.model_validate(data)


valid_person = create_person(
    {"name": "Taylor", "age": 32, "email": "taylor@example.com"}
)
print(valid_person)

invalid_person_data = {"name": "x" * 60, "age": 15, "email": "invalid-email"}
try:
    create_person(invalid_person_data)
except ValidationError as error:
    print("Expected validation error:")
    print(error)

