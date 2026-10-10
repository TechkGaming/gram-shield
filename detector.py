import re
from urllib.parse import urlparse


SUSPICIOUS_WORDS = [
    # English
    "urgent",
    "immediately",
    "otp",
    "verify",
    "click",
    "blocked",
    "suspended",
    "prize",
    "winner",
    "subsidy",
    "refund",
    "electricity",
    "account",
    "kyc",
    "password",

    # Tamil
    "அவசரம்",
    "உடனடியாக",
    "சரிபார்க்க",
    "முடக்கப்படும்",
    "துண்டிக்கப்படும்",
    "பரிசு",
    "மானியம்",
    "மின்சாரம்",
    "வங்கி",
    "ஆதார்",
    "கடவுச்சொல்",
    "கணக்கு",
]


SUSPICIOUS_TLDS = [
    ".xyz",
    ".top",
    ".click",
    ".online",
    ".site",
]


def analyze_message(message):

    message_lower = message.lower()

    reasons = []
    score = 0

    # -------------------------
    # Suspicious keywords
    # -------------------------

    found_words = []

    for word in SUSPICIOUS_WORDS:
        if word in message_lower:
            found_words.append(word)

    if found_words:
        score += min(len(found_words) * 10, 40)

        reasons.append(
            "Suspicious keywords detected: "
            + ", ".join(found_words)
        )

    # -------------------------
    # URL detection
    # -------------------------

    urls = re.findall(
        r"https?://[^\s]+|www\.[^\s]+",
        message
    )

    for url in urls:

        check_url = (
            url
            if url.startswith("http")
            else "http://" + url
        )

        try:

            domain = urlparse(
                check_url
            ).netloc.lower()

            if any(
                domain.endswith(tld)
                for tld in SUSPICIOUS_TLDS
            ):
                score += 25

                reasons.append(
                    f"Suspicious website domain detected: {domain}"
                )

            if (
                "gov.in" not in domain
                and any(
                    word in domain
                    for word in [
                        "government",
                        "subsidy",
                        "india",
                        "sbi",
                        "uidai"
                    ]
                )
            ):
                score += 25

                reasons.append(
                    f"Possible fake official domain: {domain}"
                )

        except Exception:

            score += 10

            reasons.append(
                "Invalid or suspicious URL detected"
            )

    # -------------------------
    # Urgency detection
    # -------------------------

    urgency_words = [

        # English
        "within 24 hours",
        "today",
        "immediately",
        "last chance",
        "account will be blocked",
        "will be disconnected",

        # Tamil
        "இன்று",
        "உடனடியாக",
        "துண்டிக்கப்படும்",
        "முடக்கப்படும்",
        "கடைசி வாய்ப்பு",
    ]

    if any(
        word in message_lower
        for word in urgency_words
    ):

        score += 20

        reasons.append(
            "Pressure or urgency language detected"
        )

    # -------------------------
    # Sensitive information
    # -------------------------

    sensitive_words = [

        # English
        "share otp",
        "send otp",
        "enter otp",
        "bank details",
        "password",
        "pin",
        "aadhaar number",

        # Tamil
        "otp",
        "ஆதார்",
        "கடவுச்சொல்",
        "வங்கி தகவல்",
    ]

    if any(
        word in message_lower
        for word in sensitive_words
    ):

        score += 25

        reasons.append(
            "Message requests sensitive personal information"
        )

    # -------------------------
    # Limit score
    # -------------------------

    score = min(score, 100)

    # -------------------------
    # Risk classification
    # -------------------------

    if score >= 60:
        risk = "HIGH"

    elif score >= 30:
        risk = "MEDIUM"

    else:
        risk = "LOW"

    # -------------------------
    # Scam classification
    # -------------------------

    if "மானியம்" in message_lower or "subsidy" in message_lower:

        scam_type = "Government Subsidy Scam"

    elif (
        "otp" in message_lower
        or "kyc" in message_lower
        or "ஆதார்" in message_lower
    ):

        scam_type = "OTP / KYC Scam"

    elif urls:

        scam_type = "Phishing Scam"

    elif (
        "மின்சாரம்" in message_lower
        or "electricity" in message_lower
    ):

        scam_type = "Electricity Scam"

    else:

        scam_type = "Suspicious Message"

    return {
        "risk": risk,
        "score": score,
        "scam_type": scam_type,
        "reasons": reasons,
        "urls": urls,
    }