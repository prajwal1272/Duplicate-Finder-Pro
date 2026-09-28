import pandas as pd

df = pd.read_excel("domain_duplicate.xlsx")

# Domain column se duplicate remove
unique_domain = df["Domain"].drop_duplicates()

# count
print("Total Domain:", len(df))
print("Unique Domain:", len(unique_domain))
print("Duplicate Domain:", len(df)-len(unique_domain))


# Save unique domains
unique_domain.to_excel(
    "unique_domain.xlsx",
    index=False
)