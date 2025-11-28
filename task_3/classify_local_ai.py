import json
from transformers import pipeline
import warnings

# Suppress standard huggingface warnings
warnings.filterwarnings('ignore')

MESSAGES = [
    "The app is not tracking my time on Android anymore.",
    "I would like to upgrade my plan from Free to Pro.",
    "How can I export all my timesheets to Excel?",
    "Billing failed again, my credit card keeps getting declined.",
    "I forgot my password and cannot log in.",
    "The web dashboard is very slow when loading reports.",
    "Can you add an integration with Microsoft Teams?",
    "I want to change the owner of our workspace.",
    "The mobile app crashes every time I try to clock in.",
    "How do I invite new members to my organization?",
    "We were charged twice this month, please check our invoice.",
    "Is there a way to track time offline and sync later?",
    "Please add dark mode to the web app.",
    "I need help updating our company billing address.",
    "The GPS location is inaccurate when my team clocks in.",
    "Can I limit which devices employees are allowed to clock in from?",
    "Our data export is missing some projects.",
    "I'd like to request a feature to approve timesheets before payroll.",
    "My account was deactivated and I don't know why.",
    "We need an option to automatically round time entries to 15 minutes."
]

# ------------------------------------------------------------------
# INTENT-BASED LABEL ENGINEERING
# ------------------------------------------------------------------
# I used a lable map since the earlier versions of my code were not giving satisfactory results
# 

LABEL_MAP = {
    "a technical failure, crash, error, or incorrect data": "bug",
    
    "a billing, payment, invoice, or subscription issue": "billing",
    
    "a suggestion to implement a new feature or improvement": "feature_request",
    
    "a question asking for asisstance or instructions on how to use the software or settings": "account_help",
    
    "irrelevant text": "other"
}

# Extract keys for the model
CANDIDATE_LABELS = list(LABEL_MAP.keys())

def load_messages_from_file(filename="messages.txt"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File {filename} not found, using built-in messages.")
        return MESSAGES

def classify_tickets():
    print("Loading specialized zero-shot model...")
    print("Using: MoritzLaurer/deberta-v3-base-zeroshot-v2.0")
    
    try:
        classifier = pipeline(
            "zero-shot-classification",
            model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
            device=-1 
        )
    except Exception as e:
        print(f"Error: {e}")
        return

    print("Model loaded successfully!\n")
    
    messages = load_messages_from_file()
    results = []
    category_counts = {val: 0 for val in set(LABEL_MAP.values())}
    
    print("Classifying tickets...\n")
    
    for i, message in enumerate(messages, 1):
        
        
        result = classifier(
            message, 
            candidate_labels=CANDIDATE_LABELS,
            hypothesis_template="The user is asking about {}."
        )
        
        top_description = result['labels'][0]
        top_score = result['scores'][0]
        simple_category = LABEL_MAP[top_description]

        # If the model is not super confident (< 0.7) and discriminates 
        # between feature_request and account_help, we can apply logic:
        # "How to" / "Can I" usually implies Account Help (Usage question)
        # "Add" / "Request" usually implies Feature Request
        
        if simple_category == "feature_request" and top_score < 0.8:
            lower_msg = message.lower()
            if "how can i" in lower_msg or "how do i" in lower_msg or "can i" in lower_msg:
                # If it's a question about capability, bias towards account_help
                print(f"   -> Re-routing '{message[:20]}...' from Feature to Help based on heuristics")
                simple_category = "account_help"

        results.append({
            "text": message,
            "category": simple_category,
            "score": round(top_score, 4),
            "ai_logic": top_description
        })
        
        category_counts[simple_category] += 1
        print(f"[{i:02d}] {simple_category.upper():<15} | {message[:60]}...")

    # Save output
    output_file = "classified_local.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Summary
    print("\n" + "=" * 50)
    print("CLASSIFICATION SUMMARY")
    print("=" * 50)
    for label in sorted(category_counts.keys()):
        print(f"{label}: {category_counts[label]}")
    print("=" * 50)

if __name__ == "__main__":
    classify_tickets()



#discalimer: I tried various methods, but the model seems to confuse feature_requests and account_help tickets the most