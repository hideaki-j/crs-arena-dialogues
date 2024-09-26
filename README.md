CRSArena Dialogues
===

This repository contains dialogues collected from CRSArena, along with the tool to process them.


## Contents

### Data

The `data` directory contains the following files:

- `crs_arena_dialogues_open.json`: Dialogues collected from the open crowdsource settings.
- `crs_arena_dialogues_closed.json`: Dialogues collected from the closed crowdsource settings.
- `feedback_open.csv`: User feedback data from the open setting.
- `feedback_closed.csv`: User feedback data from the closed setting.
- `votes_open.csv`: Voting data from the open crowdsource settings.
- `votes_closed.csv`: Voting data from the closed crowdsource settings.

where, open corresponds to public access while closed means that access is restricted to a selected group of crowd-workers (Prolific).

### Tools

The `tool` directory contains:

- `merge.py`: A Python script to merge votes into dialogues.

## Usage

### Merging Votes with Dialogues

To merge votes into dialogues, use the `merge.py` script:
```sh
# For dialogues from open crowdsource settings
python tool/merge.py --votes data/votes_open.csv --dialogue data/crs_arena_dialogues_open.json
```

```sh
# For dialogues from closed crowdsource settings
python tool/merge.py --votes data/votes_closed.csv --dialogue data/crs_arena_dialogues_closed.json
```

The results are stored in `data/merged` directory.