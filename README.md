# CRSArena-Dial

CRSArena-Dial is a dataset comprising conversations between users and conversational recommendation systems (CRSs) and feedback collected via the [CRS Arena](https://iai-group-crsarena.hf.space). Feedback relates to user satisfaction with a CRS and pairwise comparison of CRSs through side-by-side battles. The data collection was conducted in two crowdsource settings: open and closed. In the open setting, all users could access the system, while in the closed setting, access was restricted to a selected group of crowd-workers (Prolific). CRSArena-Dial is a resource for the evaluation of CRSs and the study of user behavior with CRSs.

## Data

The dataset is stored in the `data` directory, which contains the following files:

  * `crs_arena_dial_open.json`: Dialogues collected from the open crowdsource settings.
  * `crs_arena_dial_closed.json`: Dialogues collected from the closed crowdsource settings.
  * `votes_open.csv`: Votes and feedback from the open crowdsource settings.
  * `votes_closed.csv`: Votes and feedback from the closed crowdsource settings.

An analysis of the data is provided [here](DataAnalysis.md).

### Dialogues

CRSArena-Dial comprises 474 dialogues between users and nine conversational recommendation systems.

#### Dialogue format

Dialogues are saved in JSON format. Each dialogue is represented as a dictionary with the following keys:

  * `conversation ID`: A unique identifier for the dialogue, formatted as {CRS name}_{user ID}.
  * `agent`: CRS information.
  * `user`: User information.
  * `conversation`: Utterances exchanged between the user and the CRS.
    - An utterance is represented as a dictionary with the following keys:
      * `participant`: Speaker, i.e., USER or AGENT.
      * `utterance`: Text of the utterance.
      * `utterance ID`: A unique identifier for the utterance, formatted as {conversation ID}_{utterance number}.
  * `metadata`: Additional information about the dialogue, including user sentiment regarding their experience with the CRS (i.e., satisfaction or frustration).

Example of dialogue:

```json
{
    "conversation ID": "barcor_redial_03368a16-93bd-4b21-885d-b9a21e3498ba",
    "agent": {
        "id": "barcor_redial",
        "type": "AGENT"
    },
    "user": {
        "id": "03368a16-93bd-4b21-885d-b9a21e3498ba",
        "type": "USER"
    },
    "conversation": [
        {
            "participant": "USER",
            "utterance": "Recommend me r movi in the science fiction genre ",
            "utterance ID": "barcor_redial-03368a16-93bd-4b21-885d-b9a21e3498ba_0"
        },
        {
            "participant": "AGENT",
            "utterance": "Have you seen Blade Runner 2049 (2017)?",
            "utterance ID": "barcor_redial-03368a16-93bd-4b21-885d-b9a21e3498ba_1"
        },
        ...
    ],
    "metadata": {
        "sentiment": "frustrated"
    }
}
```

### Votes and feedback

CRSArena-Dial includes votes and feedback collected from 187 pairwise comparisons of CRSs. The data is stored in CSV format, with the following columns:

  * `session_id`: Identifier for the session (timestamp).
  * `user_id`: User identifier.
  * `crs1`: Name of CRS 1.
  * `crs2`: Name of CRS 2.
  * `vote`: Name of the CRS selected by the user or "tie" if the user could not decide.
  * `feedback`: Optional feedback provided by the user.

A script to integrate vote and feedback information into dialogues is provided in the `tool` directory. Use the script as follows:

```sh
python tool/merge.py --votes {VOTES_FILE} --dialogue {DIALOGUES_FILE}
```

The script generates a JSON file with an additional key `vote_result` for dialogue entries that have a corresponding vote in the votes file. The file is saved in the directory `data/merged`.

## Contact

Should you have any questions, please contact Nolwenn Bernard (<nolwenn.m.bernard@uis.no>) or Hideaki Joko (<hideaki.joko@ru.nl>).
