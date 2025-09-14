import re
import urllib.parse
import pandas as pd
from confusable_homoglyphs import confusables
from download_trusted import get_all_trusted_domains  # ✅ FIXED FUNCTION NAME

# ===== Step 0: Load trusted domains from hardcoded + online sources =====
TRUSTED_DOMAINS = set(get_all_trusted_domains())

# ===== Step 1: Automatically include all safe domains (Label=0) from CSVs =====
def add_safe_domains_from_csv(*csv_files):
    for file in csv_files:
        try:
            df = pd.read_csv(file, on_bad_lines='skip')
            
            # Standardize column names if needed
            if 'url' in df.columns:
                df.rename(columns={'url':'URL'}, inplace=True)
            if 'result' in df.columns:
                df.rename(columns={'result':'Label'}, inplace=True)
            if 'label' in df.columns:
                df.rename(columns={'label':'Label'}, inplace=True)

            # Add only safe domains (Label=0)
            safe_urls = df[df['Label'] == 0]['URL'].dropna().unique()
            for url in safe_urls:
                # Normalize URL (remove scheme, www)
                if not isinstance(url, str):
                    continue
                if not url.startswith(("http://", "https://")):
                    url = "http://" + url
                domain = urllib.parse.urlparse(url).netloc.replace("www.", "").lower()
                TRUSTED_DOMAINS.add(domain)
        except Exception as e:
            print(f"⚠️ Failed to load safe domains from {file}: {e}")

# Call this once with all your CSVs containing safe URLs
add_safe_domains_from_csv("urldata.csv", "urldata1.csv", "urls_data.txt")


def extract_features(url):
    features = {}

    try:
        # ✅ Normalize URL (add scheme if missing)
        if not url.startswith(("http://", "https://")):
            url = "http://" + url  

        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc.replace("www.", "").lower()
        path = parsed_url.path

        features["url_length"] = len(url)
        features["dot_count"] = url.count(".")
        features["has_at_symbol"] = int("@" in url)
        features["hyphen_count"] = url.count("-")
        features["digit_count"] = sum(c.isdigit() for c in url)

        # Check if domain is an IP address
        try:
            import ipaddress
            ipaddress.ip_address(domain)
            features["has_ip_address"] = 1
        except ValueError:
            features["has_ip_address"] = 0

        # Check if domain is in trusted domains
        is_legit = domain in TRUSTED_DOMAINS
        features["is_exact_legit"] = int(is_legit)

        # Homoglyph detection
        features["has_homoglyph"] = 0
        if not is_legit:
            for legit in TRUSTED_DOMAINS:
                if confusables.is_confusable(domain, legit):
                    features["has_homoglyph"] = 1
                    break

    except Exception as e:
        # If URL parsing fails, return default features
        print(f"Warning: failed to parse URL '{url}'. Error: {e}")
        features = {
            "url_length": 0,
            "dot_count": 0,
            "has_at_symbol": 0,
            "hyphen_count": 0,
            "digit_count": 0,
            "has_ip_address": 0,
            "is_exact_legit": 0,
            "has_homoglyph": 0
        }

    return features

# Optional helper for safe extraction when applying to DataFrame
def safe_extract_features(url):
    return extract_features(url)
