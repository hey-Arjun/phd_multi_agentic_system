# Keywords that indicate irrelevant sections (Footers, Contact, Ads)
IGNORE_KEYWORDS = [
    "Contact", "Unit 1", "Unit 2", "gmail.com", "Copyright", "All Rights Reserved", 
    "Privacy Policy", "Cookies", "Facebook", "Twitter", "Instagram",
    "NAV", "Menu", "Home", "Back", "Next", "Previous",
    "Search", "Apply Now", "Login", "Sign in", "Register",
    "Skip to content", "Toggle navigation", "Breadcrumb",
    "Read more", "View more", "Click here", "Learn more"
]

def clean_text(text: str) -> str:
    lines = text.split('\n')
    # Keep lines only if they don't contain the "noise" words
    cleaned = [l for l in lines if not any(word in l for word in IGNORE_KEYWORDS)]
    return "\n".join(cleaned)