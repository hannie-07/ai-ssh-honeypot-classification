# Research Report

## AI-Assisted Classification of SSH Honeypot Sessions Using Google Gemini

**Research type:** Exploratory cybersecurity experiment  
**Honeypot:** Cowrie 3.1.1  
**AI model:** Gemini 3.5 Flash-Lite  
**Programming language:** Python  
**Dataset size:** 51 unique SSH sessions

---

## 1. Abstract

This project explores the use of a large language model to classify behavioural activity recorded by an SSH honeypot.

A controlled experiment was conducted using Cowrie, an SSH and Telnet honeypot, deployed in a local Docker environment. A dataset of 51 unique sessions was collected, reviewed and assigned behavioural labels. Session information was subsequently submitted to Google's Gemini API for classification.

The model's predictions were compared against researcher-reviewed labels. All 51 predictions agreed with the reviewed labels, resulting in an observed agreement rate of 100%.

However, the experiment had important limitations, including a small dataset, class imbalance, repeated command patterns and the absence of brute-force examples. The result therefore demonstrates agreement within this controlled dataset rather than proven real-world detection accuracy.

## 2. Introduction

SSH services are frequently targeted by automated connection attempts, authentication attacks and suspicious command activity.

Honeypots provide a controlled environment for observing such behaviour without exposing production systems. However, analysing large volumes of honeypot logs can require considerable manual effort.

This project investigates whether an AI language model can assist with interpreting SSH session activity and assigning behavioural classifications.

The experiment focuses on the interpretation of session metadata, login events and commands recorded by Cowrie.

## 3. Research Objectives

The objectives were to:

1. Deploy and operate a local SSH honeypot.
2. Generate controlled SSH session activity.
3. extract useful information from Cowrie JSON logs.
4. Assign behavioural labels through researcher review.
5. Use Gemini to classify the same session information.
6. Compare AI predictions with researcher-reviewed labels.
7. Evaluate the results and identify methodological limitations.

## 4. Experimental Environment

The experiment used the following technologies:

| Technology | Purpose |
|---|---|
| Cowrie 3.1.1 | SSH honeypot |
| Docker | Container management |
| Kali Linux | Research environment |
| Python | Data processing and evaluation |
| Google Colab | API experimentation |
| Gemini API | AI classification |
| CSV and JSON | Dataset storage |

Cowrie was deployed in a local Docker environment and accessed through the loopback interface on port 2222.

All main experimental activity was researcher-generated in the controlled laboratory environment.

The 51 sessions represent individual recorded sessions, not 51 independent attackers.

## 5. Data Collection and Preparation

The experiment generated 51 unique sessions containing connection events, authentication information and command activity.

The recorded information was grouped by session ID and transformed into a structured CSV dataset.

The extracted features included:

- Session ID
- Event count
- Successful login indicator
- Failed login indicator
- Command count
- Recorded commands
- Event types

A separate AI input dataset was prepared without the human-reviewed labels so that the model could classify the sessions independently of the reference labels.

## 6. Behavioural Classification

Four classification categories were defined.

| Category | Interpretation |
|---|---|
| reconnaissance | Basic system or environment discovery |
| brute_force | Repeated unsuccessful authentication attempts |
| malicious_command_attempt | Suspicious commands suggesting an attempted malicious action |
| insufficient_evidence | Insufficient information to justify a stronger classification |

The researcher reviewed the collected session information and assigned reference labels.

The resulting distribution was:

| Category | Sessions |
|---|---:|
| reconnaissance | 2 |
| brute_force | 0 |
| malicious_command_attempt | 18 |
| insufficient_evidence | 31 |
| **Total** | **51** |

### Important observation

The experiment did not record any `cowrie.login.failed` events in the main dataset.

Although failed login activity had been intended as part of the experiment, the expected authentication failure events were not captured. Therefore, no sessions could be reliably labelled as brute-force examples.

Additionally, 18 sessions contained suspicious commands involving a payload retrieval and execution sequence. Cowrie recorded the `./payload.sh` command as `Command not found`.

These sessions were classified as malicious command attempts. Successful payload execution was not established.

## 7. AI Classification

The structured session information was submitted to Google's Gemini API.

Gemini 3.5 Flash-Lite was used to analyse the session information and return:

- Predicted behavioural label
- Explanation for the classification
- Confidence level

The predictions were saved in `gemini_predictions.csv`.

All 51 sessions received predictions, with no missing session IDs or duplicate predictions in the completed dataset.

## 8. Evaluation Methodology

The AI predictions were compared against the researcher's reviewed labels using session IDs.

A Python evaluation script was developed using the built-in `csv` and `pathlib` libraries.

The script calculated:

- Accuracy
- Precision
- Recall
- F1-score
- Macro average
- Weighted average
- Confusion matrix

The script also generated two output files:

- `evaluation_results.csv`
- `confusion_matrix.csv`

The evaluation script was reconstructed after the initial experiment to make the evaluation reproducible without third-party Python dependencies. It operates on the existing reviewed-label and prediction CSV files.

## 9. Results

### 9.1 Overall agreement

| Metric | Result |
|---|---:|
| Matched sessions | 51 |
| Correct predictions | 51 |
| Observed agreement | 100% |
| Macro average F1 | 0.75 |
| Weighted average F1 | 1.00 |

### 9.2 Classification report

| Category | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| reconnaissance | 1.00 | 1.00 | 1.00 | 2 |
| brute_force | 0.00 | 0.00 | 0.00 | 0 |
| malicious_command_attempt | 1.00 | 1.00 | 1.00 | 18 |
| insufficient_evidence | 1.00 | 1.00 | 1.00 | 31 |

The zero scores for brute-force classification reflect the absence of examples in that category. They should not be interpreted as evidence of failed detection.

### 9.3 Confusion matrix

| Actual / Predicted | Recon | Brute force | Malicious attempt | Insufficient evidence |
|---|---:|---:|---:|---:|
| Reconnaissance | 2 | 0 | 0 | 0 |
| Brute force | 0 | 0 | 0 | 0 |
| Malicious attempt | 0 | 0 | 18 | 0 |
| Insufficient evidence | 0 | 0 | 0 | 31 |

All evaluated predictions matched their corresponding researcher-reviewed labels.

## 10. Discussion

The experiment demonstrated that Gemini could reproduce the researcher's reviewed classifications across the 51 collected sessions.

The result suggests that language models may be useful as an additional analytical aid when interpreting structured honeypot activity.

However, the observed agreement should be interpreted cautiously.

The dataset was relatively small and contained repeated behavioural patterns. In particular, the 18 malicious command attempt sessions shared a similar command sequence.

The reference labels were also assigned by a single researcher. Consequently, the evaluation does not establish independent ground truth.

The model's reported confidence was high for all 51 predictions, but these confidence values were not independently calibrated.

The macro average was lower than the weighted average because the brute-force category had zero support. This illustrates why class distribution must be considered when interpreting classification metrics.

## 11. Limitations

The major limitations were:

1. **Small sample size:** Only 51 sessions were evaluated.
2. **Controlled environment:** The experiment used researcher-generated activity rather than live external attack traffic.
3. **Class imbalance:** No brute-force examples were available.
4. **Repeated patterns:** Several sessions contained similar command sequences.
5. **Single-reviewer labels:** The reference labels were not independently verified by multiple analysts.
6. **Uncalibrated confidence:** Gemini's confidence output was not independently validated.
7. **Limited generalisation:** The results cannot establish performance against unseen or real-world attacks.
8. **Reproducibility scope:** The evaluation script is available, but the original data preparation and API execution scripts were not preserved as a complete executable pipeline.

## 12. Future Work

Further research could improve the experiment through:

- Generating valid failed authentication events and collecting brute-force examples.
- Increasing the number and diversity of SSH sessions.
- Introducing more varied command sequences.
- Obtaining independent reviews from additional analysts.
- Comparing multiple AI models.
- Testing the model on sessions excluded from the initial experiment.
- Evaluating the effect of prompt design on classification consistency.
- Exploring how AI-assisted analysis could support SOC analyst workflows.

## 13. Conclusion

This project investigated the application of a large language model to SSH honeypot session classification.

Using Cowrie-generated activity, Python-based data preparation and Gemini API predictions, the experiment achieved 100% agreement with the researcher's reviewed labels across 51 sessions.

The result provides an initial demonstration of AI-assisted interpretation of honeypot activity. It does not establish production readiness or general real-world detection accuracy.

The experiment also highlighted the importance of reliable data collection, representative class distributions, independent reference labels and transparent reporting when evaluating AI systems in cybersecurity.

---

**Research note:** All main experimental activity was conducted in a controlled local laboratory environment. The findings should be interpreted within the stated experimental scope.

