import textstat

def analyze_readability(text):
    """
    Returns a readability report with human-friendly meter-style feedback.
    """
    # Compute metrics
    flesch = textstat.flesch_reading_ease(text)
    grade = textstat.flesch_kincaid_grade(text)
    fog = textstat.gunning_fog(text)
    smog = textstat.smog_index(text)
    ari = textstat.automated_readability_index(text)
    asl = textstat.avg_sentence_length(text)
    dale = textstat.dale_chall_readability_score(text)

    # Interpret Flesch score (0–100)
    if flesch >= 90:
        level = "Very Easy"
        desc = "Extremely easy to read. Suitable for all audiences."
    elif flesch >= 70:
        level = "Easy"
        desc = "Good readability for general content and blogs."
    elif flesch >= 60:
        level = "Fairly Easy"
        desc = "Slightly formal. Suitable for educated readers."
    elif flesch >= 50:
        level = "Moderate"
        desc = "Fairly difficult. Use shorter sentences for clarity."
    elif flesch >= 30:
        level = "Difficult"
        desc = "Likely complex or technical content."
    else:
        level = "Very Difficult"
        desc = "Hard to read. Consider rewriting for simplicity."

    # Create a simple "meter" (visual bar)
    total_blocks = 20
    filled_blocks = int((min(max(flesch, 0), 100) / 100) * total_blocks)
    meter = "█" * filled_blocks + "░" * (total_blocks - filled_blocks)

    report = (
        f"🧾 Readability Overview\n"
        f"------------------------------\n"
        f"Flesch Reading Ease: {flesch:.2f}\n"
        f"Readability Meter: {meter}  ({level})\n"
        f"Interpretation: {desc}\n\n"
        f"Flesch-Kincaid Grade Level: {grade:.2f}\n"
        f"Gunning Fog Index: {fog:.2f}\n"
        f"SMOG Index: {smog:.2f}\n"
        f"Automated Readability Index: {ari:.2f}\n"
        f"Average Sentence Length: {asl:.2f} words\n"
        f"Dale–Chall Score: {dale:.2f}\n"
    )

    return report
