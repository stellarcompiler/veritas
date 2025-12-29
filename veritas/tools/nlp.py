from crewai_tools import tool
import spacy
import json

# Load SpaCy large model once
nlp = spacy.load("en_core_web_lg")

INTENSIFIERS = {
    "very", "extremely", "highly", "deeply", "incredibly",
    "absolutely", "totally", "completely", "utterly",
    "unbelievably", "insanely"
}

@tool("spacy_claim_analyzer_tool")
def spacy_claim_analyzer_tool(claim: str) -> str:
    """
    Analyze a claim using SpaCy linguistic structure to extract entities
    and compute a sensationalism score based on grammar and syntax.
    """

    if not claim.strip():
        return '{"error": "No text provided."}'

    doc = nlp(claim)

    # -----------------------------
    # 1. Named Entity Extraction
    # -----------------------------
    entities = [ent.text for ent in doc.ents]

    # -----------------------------
    # 2. Structural Metrics
    # -----------------------------
    token_count = len(doc)
    if token_count == 0:
        token_count = 1  # safety

    # POS counts
    adj_count = sum(1 for t in doc if t.pos_ == "ADJ")
    adv_count = sum(1 for t in doc if t.pos_ == "ADV")

    # Intensifiers
    intensifier_count = sum(
        1 for t in doc if t.lemma_.lower() in INTENSIFIERS
    )

    # Exclamation emphasis
    exclamation_score = min(claim.count("!") * 10, 30)

    # Imperative detection (headline / command style)
    imperative_score = 0
    for sent in doc.sents:
        root = sent.root
        if root.pos_ == "VERB" and root.tag_ == "VB":
            imperative_score += 10

    # Short sentence punchiness (headline bias)
    short_sentence_bonus = 0
    for sent in doc.sents:
        if len(sent) <= 6:
            short_sentence_bonus += 5

    # Entity stacking (name-dropping for impact)
    entity_density = len(doc.ents) / token_count
    entity_score = min(entity_density * 40, 20)

    # -----------------------------
    # 3. Density-Based Emotion Score
    # -----------------------------
    modifier_density = (adj_count + adv_count) / token_count
    modifier_score = min(modifier_density * 60, 30)

    intensifier_score = min(intensifier_count * 8, 20)

    # -----------------------------
    # 4. Final Sensationalism Score
    # -----------------------------
    sensationalism_score = min(
        int(
            modifier_score
            + intensifier_score
            + exclamation_score
            + imperative_score
            + short_sentence_bonus
            + entity_score
        ),
        100
    )

    # -----------------------------
    # 5. Qualitative Interpretation
    # -----------------------------
    if sensationalism_score < 30:
        analysis = "The claim is linguistically neutral and informational."
    elif sensationalism_score < 70:
        analysis = "The claim uses emotionally suggestive or headline-style language."
    else:
        analysis = "The claim is structurally sensationalized and emotionally amplified."

    result = {
        "entities": entities,
        "sensationalism_score": sensationalism_score,
        "analysis": analysis
    }

    return json.dumps(result, indent=2)
