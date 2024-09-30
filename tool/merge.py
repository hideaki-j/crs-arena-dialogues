import argparse
import json
import os

import pandas as pd


def find_vote(
    votes_df: pd.DataFrame, user_id: str, agent_id: str
) -> pd.DataFrame:
    vote_rows = votes_df[
        (votes_df["user_id"] == user_id)
        & ((votes_df["crs1"] == agent_id) | (votes_df["crs2"] == agent_id))
    ]
    return vote_rows


def determine_vote_result(vote_row: pd.DataFrame, agent_id: str) -> str:
    assert len(vote_row) == 1, "Multiple vote rows found"
    if vote_row["vote"].iloc[0] == "tie":
        return "tie"
    elif vote_row["vote"].iloc[0] == agent_id:
        return "win"
    else:
        return "lose"


def _delete_duplicates(votes_df: pd.DataFrame) -> pd.DataFrame:
    # Delete duplicate votes to avoid "multiple vote rows found" error
    votes_df = votes_df.drop_duplicates(
        subset=["user_id", "crs1", "crs2", "vote"], keep="first"
    )
    return votes_df


def merge_votes_to_dialogues(votes_file: str, dialogues_file: str) -> None:
    votes_df = pd.read_csv(votes_file)
    votes_df = _delete_duplicates(votes_df)
    with open(dialogues_file, "r") as f:
        dialogues = json.load(f)

    # Process each dialogue
    for dialogue in dialogues:
        user_id = dialogue["user"]["id"]
        agent_id = dialogue["agent"]["id"]

        # Find the vote for the dialogue from the votes.csv
        vote_rows = find_vote(votes_df, user_id, agent_id)

        # Error if multiple vote rows found
        if len(vote_rows) > 1:
            print(
                f"Error: Multiple vote rows found for user_id {user_id} and "
                f"agent_id {agent_id}"
            )
            return

        # If no vote found, set vote to None
        if len(vote_rows) == 0:
            dialogue["vote"] = None
        else:  # If vote found, add vote result to the dialogue
            vote_result = determine_vote_result(vote_rows, agent_id)
            dialogue["vote_result"] = {
                "result": vote_result,
                "details": {
                    "crs1": vote_rows["crs1"].iloc[0],
                    "crs2": vote_rows["crs2"].iloc[0],
                    "vote": vote_rows["vote"].iloc[0],
                    "feedback": vote_rows["feedback"].iloc[0],
                },
            }

    # Output the merged dialogues
    output_filename = os.path.basename(dialogues_file).replace(
        ".json", "_with_votes.json"
    )
    output_dir = os.path.join(os.path.dirname(dialogues_file), "merged")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, output_filename)

    with open(output_file, "w") as f:
        json.dump(dialogues, f, indent=4)

    print(f"Merged dialogues written to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge votes into dialogues")
    parser.add_argument(
        "-v",
        "--votes",
        dest="votes_file",
        required=True,
        help="Path to the votes CSV file",
    )
    parser.add_argument(
        "-d",
        "--dialogues",
        dest="dialogues_file",
        required=True,
        help="Path to the dialogues JSON file",
    )

    args = parser.parse_args()

    # Main: merge votes into dialogues
    merge_votes_to_dialogues(args.votes_file, args.dialogues_file)
