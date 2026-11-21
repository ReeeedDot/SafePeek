import re
from urllib.parse import urlparse
import tldextract

SUSPICIOUS_WORDS = [
    'login', 'signin', 'verify', 'update', 'secure', 'account',
    'banking', 'confirm', 'password', 'free', 'lucky', 'bonus', 'kyc', 'wallet', 'reward'
]
SHORTENERS = ['bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co', 'is.gd', 'buff.ly']

def extract_features(url: str) -> list:
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    parsed = urlparse(url)
    ext = tldextract.extract(url)
    hostname = parsed.netloc.lower()
    path = parsed.path.lower()

    subdomains = ext.subdomain.split('.') if ext.subdomain else []
    ip_pattern = r'^\d{1,3}(\.\d{1,3}){3}$'

    return [
        len(url),                                                        # 1. URL length
        len(hostname),                                                   # 2. Hostname length
        len(path),                                                       # 3. Path length
        url.count('.'),                                                  # 4. Dot count
        url.count('-'),                                                  # 5. Hyphen count
        url.count('@'),                                                  # 6. '@' symbol count
        url.count('?'),                                                  # 7. '?' count
        url.count('='),                                                  # 8. '=' count
        path.count('/'),                                                 # 9. Subdirectory depth
        1 if parsed.scheme == 'https' else 0,                            # 10. HTTPS flag
        1 if re.match(ip_pattern, hostname.split(':')[0]) else 0,        # 11. IP in domain
        len(subdomains),                                                 # 12. Subdomain count
        sum(word in url.lower() for word in SUSPICIOUS_WORDS),           # 13. Keyword hits
        1 if any(s in hostname for s in SHORTENERS) else 0,              # 14. Shortener flag
        sum(c.isdigit() for c in url)                                    # 15. Digit count
    ]