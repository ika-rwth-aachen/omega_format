** make changes in `.py` files and always run `generate_enums` afterwards **

# Input Format Types Specification

Type specification of Reference and Perception format


## Updating to the latest version of the format specification
gi
- Only the `{reference|perception}_types.py` files should be edited manually.
- The script `generate_enums.py` automatically generates the lookup tables in `.h` and `.json` formats.
- Only the original `.py` or the generated `.h` and `.json` files should be used in any other code. No manual re-coding of this information!
