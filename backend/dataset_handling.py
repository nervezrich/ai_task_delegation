import pandas as pd

# Function to filter and display rows where match_score is in range [0.8, 1.0]
def filter_match_score(df):
    # Filter the dataframe to get rows where match_score is between 0.8 and 1.0
    filtered_df = df[(df["match_score"] >= 0.8) & (df["match_score"] <= 1.0)]
    
    # Print the relevant columns: title, type_of_task, priority_level, avg_quality_score, match_score
    print(filtered_df[["title", "type_of_task", "priority_level", "avg_quality_score", "match_score"]])

    # Return the filtered DataFrame
    return filtered_df

# Example usage:
# Load the dataset from the CSV file
df = pd.read_csv("backend/data/low.csv")

# Call the function to filter and print the data
filtered_data = filter_match_score(df)
