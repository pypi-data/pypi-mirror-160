# DataWhys Dashboard Python SDK

DataWhys Dashboard SDK allows users to create a DataWhys Dashboard directly within their Python notebooks.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install datawhys-dashboard.

```bash
pip install datawhys-dashboard
```

## Usage

```python
import datawhys_dashboard as dwdash

# Set your credentials
dwdash.api_key = "<API_KEY>" # Ask your datawhys rep for this key
dwdash.api_base = "https://emea.datawhys.ai/api/v0.2/"

# Build a pandas dataframe and store in `df` (not shown)

# Create a dashboard
from datawhys_dashboard import create_dashboard
create_dashboard(df, outcome="Risk")
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Take a look at `CONTRIBUTING.md` for more info

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
