# Contributing

> Refer to `README.md` on how to run the app.

Here's a list of special actions to take when updating the source code to contribute
to this repository.

## Unit tests

Make sure to run all unit tests before pushing your changes, with:

```shell
python -m unittest discover -s mot/tests
```

## Static checks

This program uses static checking to improve readability and maintainability.  
Since static checks are ignored by the Python interpreter (they are useful only
for developers), they must be validated again before pushing new changes, with:

```shell
mypy mot
```

## Dependencies

The file `requirements.txt` declares all dependencies used by this application.  
When the dependencies change, it's necessary to manually review `requirements.txt`.

In the past, `requirements.txt` used to be generated automatically using `pip freeze`
and `pipreqs`, but both methods have been abandoned, because:

- `pipreqs` fails to detect most packages.
- `pip freeze` lists all installed packages in the current environment, and this
  creates too much bloat.
