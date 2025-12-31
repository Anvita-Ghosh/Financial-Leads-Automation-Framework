import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
grants_df = pd.read_csv("grant_keywords_only.csv")
project_df = pd.read_csv("extracted_projects.csv")

# Final structured output list
output_rows = []

for _, project in project_df.iterrows():
    project_title = project["Project Text"]
    project_keywords = project["Extracted Keywords"]

    # Combine project and grant keywords
    all_text = [project_keywords] + list(grants_df["keywords"])
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_text)

    # Compute cosine similarity
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

    # Rank top 3 most similar grants
    ranked = sorted(
        [
            (grants_df.loc[i, "grant_title"], round(score, 4))  # updated to match 'grant_title'
            for i, score in enumerate(similarity_scores)
        ],
        key=lambda x: x[1],
        reverse=True
    )[:3]

    # Add to output
    for i, (grant_title, score) in enumerate(ranked):
        output_rows.append({
            "Project Title": project_title if i == 0 else "",
            "Grant Name": grant_title,
            "Priority Score": score
        })

# Save final output
output_df = pd.DataFrame(output_rows)
output_df.to_csv("output.csv", index=False)

print("Final structured output saved to 'output.csv'")
