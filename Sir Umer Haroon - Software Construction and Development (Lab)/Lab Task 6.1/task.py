import re 

def password_validation(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[^a-zA-Z0-9\s]).{8,}$"
    return re.match(pattern, password)


password = input("Enter a password: ")
if password_validation(password):
    print("The chosen password is strong.")
else:    
    print("The chosen password is not strong.")

# posts = [
# "@Ali: Phone X12 is EXCELLENT! #TechReview https://example.com/review&quot",
# "@Sara99: Great camera, but average battery life. #Smartphone",
# "@TechWorld: Phone X12 costs $799 and Phone X13 costs $899. #PriceCheck",
# "@Bilal: I love the new PHONE X14! It has 5G support. #Innovation",
# "@Ayesha: EXCELLENT performance and GREAT design! #TechNews",
# "@MobileFan: Phone X15 is available for $999. #NewLaunch",
# "@Hamza: The camera is great, and the display is EXCELLENT! #Photography",
# "@ZaraTech: Phone X16 has 12GB RAM and costs $1099. https://example.com/phone&quot",
# "@Usman: I love Phone X17, but its battery lasts only 8 hours. #Review",
# "@TechGuru: GREAT features at just $699! Phone X18 is impressive. #Gadgets",
# "@Mina: Phone X19 has 256GB storage and excellent performance. #Technology",
# "@Farhan: I LOVE this smartphone! Phone X20 costs $1199. #PremiumPhone",
# "@DigitalWorld: Phone X21 supports 5G and has 16GB RAM. #MobileTech",
# "@Hira: Great price, excellent camera, and amazing design! #BestPhone",
# "@AhmedTech: Phone X22 is priced at $899, while Phone X23 costs $999. #Comparison"
# ]

# price_pattern = r"(?<=\$)\d+"
# hashtag_pattern = r"(?<=#)[A-Za-z0-9_]+"
# number_pattern = r"(?<!\$)\b\d+\b"

# model_pattern = r"\bPhone(?=\s+X\d+\b)\s+(X\d+)\b"
# positive_pattern = r"\b(?:excellent|great|love)\b"
# url_pattern = r"https?://\S+"
# username_pattern = r"@\w+:?"

# for post in posts:
# 	prices = re.findall(price_pattern, post)
# 	hashtags = re.findall(hashtag_pattern, post)
# 	numbers = re.findall(number_pattern, post)
# 	model_references = re.findall(model_pattern, post, re.IGNORECASE)
# 	positive_keywords = re.findall(positive_pattern, post, re.IGNORECASE)

# 	cleaned_post = re.sub(url_pattern, "", post)
# 	cleaned_post = re.sub(username_pattern, "", cleaned_post)
# 	cleaned_post = re.sub(r"\s+", " ", cleaned_post).strip().lower()

# 	print(f"Cleaned post: {cleaned_post}")
# 	print(f"  Keywords: {positive_keywords}")
# 	print(f"  Hashtags: {hashtags}")
# 	print(f"  Prices: {prices}")
# 	print(f"  Numbers not preceded by $: {numbers}")
# 	print(f"  Model references: {model_references}")
# 	print()
# l