import random
import pandas as pd
random.seed(42)
# 1. Legitmate / Safe Domains & Paths
legit_domains = [
    "google.com", "youtube.com", "github.com", "wikipedia.org", "amazon.in",
    "irctc.co.in", "sbi.co.in", "microsoft.com", "linkedin.com", "stackoverflow.com",
    "python.org", "kaggle.com", "flipkart.com", "icicibank.com", "hdfcbank.com",
    "indiapost.gov.in", "ncert.nic.in", "geeksforgeeks.org", "coursera.org", "udemy.com",
    "apple.com", "adobe.com", "netflix.com", "spotify.com", "canva.com",
    "zomato.com", "swiggy.com", "paytm.com", "phonepe.com", "makemytrip.com"
]

legit_paths = [
    "", "/about", "/contact", "/services", "/home", "/products", "/help",
    "/news", "/blog", "/docs/getting-started", "/courses/python", "/pricing",
    "/support/faq", "/careers", "/terms", "/privacy-policy", "/search?q=tutorial"
]

safe_urls = []
for _ in range(5000):
    domain = random.choice(legit_domains)
    prefix = random.choice(["https://www.", "https://"])
    path = random.choice(legit_paths)
    # Kabhi-kabhi valid query param add karein
    if random.random() < 0.2 and "?" not in path:
        path += f"?id={random.randint(10, 999)}"
    safe_urls.append(f"{prefix}{domain}{path}")

# 2. Realistic Phishing URL Patterns
brands = ["sbi", "hdfc", "icici", "paytm", "amazon", "google", "paypal", "netflix", "irctc", "epfo", "uidai"]
keywords = ["login", "verify", "secure", "update", "kyc", "account", "confirm", "banking", "bonus", "reward", "free", "wallet"]
tlds = [".xyz", ".top", ".info", ".online", ".site", ".club", ".tk", ".ml", ".com", ".net"]
shorteners = ["bit.ly", "tinyurl.com", "goo.gl", "ow.ly", "t.co", "is.gd", "buff.ly"]

phish_urls = []
for _ in range(5000):
    pattern_type = random.randint(1, 5)
    brand = random.choice(brands)
    kw1 = random.choice(keywords)
    kw2 = random.choice(keywords)
    tld = random.choice(tlds)

    if pattern_type == 1:
        # Subdomain spoofing + multiple hyphens
        url = f"http://{brand}-{kw1}-{kw2}.security-alert{tld}/auth/{kw1}?session={random.randint(10000,99999)}"
    elif pattern_type == 2:
        # Raw IP address URL
        ip = f"{random.randint(11,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        url = f"http://{ip}/{brand}/{kw1}-{kw2}.php?user=1"
    elif pattern_type == 3:
        # '@' symbol redirection trick
        url = f"https://www.{brand}.com@{kw1}-{brand}-portal{tld}/{kw2}"
    elif pattern_type == 4:
        # URL Shortener with suspicious slug
        short = random.choice(shorteners)
        url = f"http://{short}/{brand}-{kw1}{random.randint(10,99)}"
    else:
        # Long obfuscated URL with deep subdirectories
        url = f"http://www.{kw1}-{brand}-support-desk{tld}/web/portal/v2/{kw2}/index.html?token={random.randint(100000,999999)}&ref={brand}"

    phish_urls.append(url)

# 3. Combine & Shuffle
df_safe = pd.DataFrame({"url": safe_urls, "label": 0})
df_phish = pd.DataFrame({"url": phish_urls, "label": 1})

df = pd.concat([df_safe, df_phish]).sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("data/urldata.csv", index=False)
print(f"Success! Generated {len(df)} offline URLs (5000 Safe, 5000 Phishing) in data/urldata.csv")
