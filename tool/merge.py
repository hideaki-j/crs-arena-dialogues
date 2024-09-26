import pandas as pd
import json
import os
import argparse  # Add this import

def find_vote(votes_df, user_id, agent_id):
    vote_rows = votes_df[(votes_df['user_id'] == user_id) & 
                         ((votes_df['crs1'] == agent_id) | (votes_df['crs2'] == agent_id))]
    return vote_rows

def determine_vote_result(vote_row, agent_id):
    if vote_row['vote'].iloc[0] == 'tie':
        return 'tie'
    elif vote_row['vote'].iloc[0] == agent_id:
        return 'win'
    else:
        return 'lose'

def _delete_duplicates(votes_df):
    votes_df = votes_df.drop_duplicates(subset=['user_id', 'crs1', 'crs2', 'vote'], keep='first')
    return votes_df

def merge_votes_to_dialogues(votes_file, dialogues_file):
    # Read votes CSV and dialogues JSON
    votes_df = pd.read_csv(votes_file)
    votes_df = _delete_duplicates(votes_df)
    with open(dialogues_file, 'r') as f:
        dialogues = json.load(f)

    for dialogue in dialogues:
        user_id = dialogue['user']['id']
        agent_id = dialogue['agent']['id']

        vote_rows = find_vote(votes_df, user_id, agent_id)

        if len(vote_rows) > 1:
            print(f"Error: Multiple vote rows found for user_id {user_id} and agent_id {agent_id}")
            return

        if len(vote_rows) == 0:
            dialogue['vote'] = None
        else:
            vote_result = determine_vote_result(vote_rows, agent_id)
            dialogue['vote_result'] = {
                "result": vote_result,
                "details": {
                    "crs1": vote_rows['crs1'].iloc[0],
                    "crs2": vote_rows['crs2'].iloc[0],
                    "vote": vote_rows['vote'].iloc[0]
                }
            }

    # Write updated dialogues to output file
    output_filename = os.path.basename(dialogues_file).replace('.json', '_with_votes.json')
    output_dir = os.path.join(os.path.dirname(dialogues_file), 'merged')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, output_filename)
    
    with open(output_file, 'w') as f:
        json.dump(dialogues, f, indent=4)

    print(f"Updated dialogues written to {output_file}")

if __name__ == "__main__":
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description="Merge votes into dialogues")
    parser.add_argument("-v", "--votes", dest="votes_file", required=True, help="Path to the votes CSV file")
    parser.add_argument("-d", "--dialogues", dest="dialogues_file", required=True, help="Path to the dialogues JSON file")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call merge_votes_to_dialogues with parsed arguments
    merge_votes_to_dialogues(args.votes_file, args.dialogues_file)
