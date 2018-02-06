# Queryable Dictionaries

###### A wrapper to query a list of python dictionaries.

Have you ever wanted to have a SQL-like interface for a list of dictionaries?
No? Well here you go anyway!

I'll admit, I don't know that this is anyone's most serious problem, but I did
find myself thinking that I wish I had a nicer syntax for searching through a
list of dictionaries during work on
[these scripts](https://github.com/bneb/countdown#letters).

## Features

Given a list of dictionaries, say:
```python
d_list = [
    {"id": 1, "name": "Leo", "height": 1.9, "retired": True},
    {"id": 2, "name": "Szymon", "height": 1.72, "retired": False},
    {"id": 3, "name": "Giorgi", "height": 1.77, "retired": False},
    # ...
]
```

You can use two different SQL-like interfaces to query the data.

Example 1:
```python
query_dicts(d_list).select("id", "name").where("retired")
> [{"id": 1, "name": "Leo"}]

query_dicts(d_list).select("id").where("height > 1.75")
> [{"id": 1}, {"id": 3}]

query_dicts(d_list).select("name", "height").where({"id": lambda x: x%2 == 0})
> [{"name": "Szymon", "height": 1.72}]
```

Reading left-to-right, this is easy to understand.
  - "Query dictionaries `<specified list of dictionaries>`."
  - "Select `<specified fields>`, where `<filters are true>`."

Example 2:
```python
select_fields("id", "name").from_dicts(d_list).where("retired")
> [{"id": 1, "name": "Leo"}]

select_fields("id").from_dicts(d_list).where("height > 1.75")
> [{"id": 1}, {"id": 3}]

select_fields(
  "name",
  "height"
).from_dicts(
  d_list
).where(
  {"id": lambda x: x < 3},
  "height < 1.8",
)
> [{"name": "Szymon", "height": 1.72}]
```

Reading left-to-right, this is even easier to understand.
  - "select fields `<specified fields>`"
  - "from dictionaries `<specified list of dictionaries>`"
  - "where "`<filters are true>`"

I kept the parsing very simple for the filter statements. Nested operations are
not supported at this time, but maybe in the future.

## Implementation

Implemented in Python3, but I think it should be compatible with 2.7.
This uses modules `re`, `functools`, and `operator`.

There is nothing further to install. 

`re.finditer` can be a little confusing at first. Please see this
[documentation](https://docs.python.org/3/library/re.html#writing-a-tokenizer).

## Testing

Tests were written to leverage `unittest`.
To run all tests, use `python3 -m unittest discover`.

## Extensions

As mentioned above, the next feature to be included is nested operations in the
filter statements. Once the filter parsing logic is completed, I would like to
extend this interface to Pandas DataFrames, Matrices, and other collections.

---

Thanks ✌️
