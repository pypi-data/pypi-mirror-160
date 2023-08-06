# Klein Util

Module to contain some basic utility components


### klein_util.dict
`traverse_dict()` - function for traversing nested dicts using a list of keys

*Example:* get a field from a mongo `doc` using dot notation:
```
from klein_util.dict import traverse_dict

property = 'ner.chemicalentities.found'
entities_found = traverse_dict(doc, property.split('.'))
```

## Tests
To run tests, run the following command in the project root directory:

```
python -m pytest
```

### License
This project is licensed under the terms of the Apache 2 license, which can be found in the repository as `LICENSE.txt`