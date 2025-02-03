# Tests of OMEGA Format Library

[pytest](https://docs.pytest.org/en/stable/) is used for testing. Install it by running `pip install pytest`.
To run all test run `pytest` from the root of the package.
You need to have installed the package into the system with `pip install -e .`.
## Read Write Consistency Checks

The read/write consistency checks require you to put a `ReferenceRecording` file with the name `reference_rec.hdf5` and and `PerceptionRecording` file with the name `perception_rec.hdf5` into this folder. After you have done that simply run `pytest` from the parent directory.

```python
>>> x = 4 + 3
>>> x
8
```