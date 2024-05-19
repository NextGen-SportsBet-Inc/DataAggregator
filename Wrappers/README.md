# Wrappers

## Installing

```bash
cd path/to/DataAggregator/
virtualenv .venv
source .venv/bin/activate
python install -r requirements.txt
```

## Running

```bash
cd path/to/DataAggregator/
source .venv/bin/activate
python Wrappers/main.py
```

or 

```bash
cd path/to/DataAggregator/Wrappers/
source .venv/bin/activate
python main.py
```

## Testing

```bash
cd path/to/DataAggregator/
source .venv/bin/activate
cd Wrappers/
python -m unittest discover
```
