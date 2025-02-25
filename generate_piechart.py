import requests
import matplotlib.pyplot as plt
from github import Github
import os

# Get your GitHub username
GITHUB_USERNAME = "YOUR_GITHUB_USERNAME"  # Replace with your GitHub username
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub Action will use this token

# Initialize GitHub API
g = Github(GITHUB_TOKEN)
user = g.get_user()

# Fetch repository languages
language_data = {}
for repo in user.get_repos():
    if repo.fork:  # Ignore forked repos
        continue
    languages = repo.get_languages()
    for lang, bytes in languages.items():
        language_data[lang] = language_data.get(lang, 0) + bytes

# Sort and normalize data
total_bytes = sum(language_data.values())
language_data = {k: (v / total_bytes) * 100 for k, v in sorted(language_data.items(), key=lambda item: item[1], reverse=True)}

# Generate Pie Chart
plt.figure(figsize=(7, 7), facecolor='white')
colors = plt.cm.Paired.colors  # Eye-catching colors
plt.pie(language_data.values(), labels=language_data.keys(), autopct='%1.1f%%', colors=colors, startangle=140, wedgeprops={"edgecolor": "black"})
plt.title(f"{GITHUB_USERNAME}'s GitHub Language Usage", fontsize=14, fontweight='bold', color='black')

# Save Pie Chart
plt.savefig("language_piechart.png", bbox_inches='tight', dpi=200)
