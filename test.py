import requests
print("starting")

gr_key = "lkPQBdBth7EI3WJjFYWawg"

res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": gr_key, "isbns": "9781632168146"})
print(res.json())