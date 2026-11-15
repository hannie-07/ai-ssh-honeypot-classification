
import csv
from pathlib import Path

DATA_DIR = Path("data")

LABELS = [
    "reconnaissance",
    "brute_force",
    "malicious_command_attempt",
    "insufficient_evidence"
]

# Load human-reviewed labels
with open(DATA_DIR / "human_review.csv", newline="") as file:
    human_rows = list(csv.DictReader(file))

# Load Gemini predictions
with open(DATA_DIR / "gemini_predictions.csv", newline="") as file:
    prediction_rows = list(csv.DictReader(file))

# Match records using session IDs
human = {row["session_id"]: row["human_label"] for row in human_rows}
predictions = {row["session_id"]: row for row in prediction_rows}

matched_ids = sorted(set(human) & set(predictions))

comparison = []

for session_id in matched_ids:
    comparison.append({
        "session_id": session_id,
        "human_label": human[session_id],
        "predicted_label": predictions[session_id]["predicted_label"],
        "confidence": predictions[session_id]["confidence"]
    })

# Validate labels
for row in comparison:
    assert row["human_label"] in LABELS
    assert row["predicted_label"] in LABELS

# Build confusion matrix
matrix = {
    actual: {predicted: 0 for predicted in LABELS}
    for actual in LABELS
}

for row in comparison:
    matrix[row["human_label"]][row["predicted_label"]] += 1

total = len(comparison)
correct = sum(matrix[label][label] for label in LABELS)

print("Matched sessions:", total)
print("Accuracy:", correct / total if total else 0)

print("\nCLASSIFICATION REPORT")
print(f"{'Class':35} Precision  Recall  F1  Support")

all_metrics = []

for label in LABELS:
    tp = matrix[label][label]
    actual_count = sum(matrix[label].values())
    predicted_count = sum(matrix[actual][label] for actual in LABELS)

    precision = tp / predicted_count if predicted_count else 0
    recall = tp / actual_count if actual_count else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )

    all_metrics.append((precision, recall, f1, actual_count))

    print(
        f"{label:35} {precision:.2f}      "
        f"{recall:.2f}    {f1:.2f}  {actual_count}"
    )

macro = [
    sum(metric[i] for metric in all_metrics) / len(LABELS)
    for i in range(3)
]

weighted = [
    sum(metric[i] * metric[3] for metric in all_metrics) / total
    if total else 0
    for i in range(3)
]

print("\nMacro average:", [round(x, 2) for x in macro])
print("Weighted average:", [round(x, 2) for x in weighted])

# Save evaluation results
with open(DATA_DIR / "evaluation_results.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "session_id",
            "human_label",
            "predicted_label",
            "confidence"
        ]
    )
    writer.writeheader()
    writer.writerows(comparison)

# Save confusion matrix
with open(DATA_DIR / "confusion_matrix.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["human_label"] + LABELS)

    for label in LABELS:
        writer.writerow(
            [label] + [matrix[label][predicted] for predicted in LABELS]
        )

print("\nEvaluation files saved successfully.")
