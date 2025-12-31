import pandas as pd
import ollama

# Load the filtered grants CSV
df = pd.read_csv("grants_data_filtered2.csv")

# Define the keyword generation function
def generate_keywords(grant_title, filtered_description):
    prompt = f"""
You are an assistant that extracts 3 to 8 relevant keywords or key phrases for indexing grants.

Grant Title: "{grant_title}"

Description:
\"\"\"
{filtered_description}
\"\"\"

Only return the most meaningful keywords that describe the subject, purpose, or domain of this grant. 
Return them as a comma-separated list with no extra text.
"""

    try:
        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": "You generate crisp, relevant keywords for search and tagging."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"

# Prepare new lists for output CSV
titles = []
keywords_list = []

# Loop through rows
for index, row in df.iterrows():
    title = row.get("grant_title", "")
    desc = row.get("filtered_description", "")
    
    if pd.isna(title) or pd.isna(desc) or desc.strip() == "":
        continue  # skip rows with missing info

    print(f"Generating keywords for row {index + 1}: {title}")
    keywords = generate_keywords(title, desc)

    titles.append(title)
    keywords_list.append(keywords)

# Create new DataFrame with only title and keywords
output_df = pd.DataFrame({
    "grant_title": titles,
    "keywords": keywords_list
})

# Save to new CSV
output_df.to_csv("grant_keywords_only.csv", index=False)

print("Done! Grant titles and keywords saved to 'grant_keywords_only.csv'")
