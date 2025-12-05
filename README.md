# 🛡️ AI Safety & Risk Auditor for Social Platforms

This project is a small simulation of an **internal Trust & Safety tool** for a social media platform.

It uses a **multi-agent LLM pipeline** on top of synthetic company data (users, posts, DMs) to:

- Analyse user posts and private messages
- Detect underage risk / misrepresentation
- Detect bullying and harassment
- Detect self-harm / mental health risk
- Detect grooming / sexual exploitation patterns
- Detect substance abuse promotion
- Map the findings to simplified **safety policies**
- Generate a **user-level safety report** with an overall risk score and recommended action

All data in this project is **synthetic** and for **research/demo purposes only**.

---

## ✨ Features

- Multi-agent GenAI workflow:
  - Underage Risk Agent
  - Content Safety Agent (bullying, self-harm, grooming, substance)
  - Interaction/Grooming Agent
  - Policy Violation Agent
  - Safety Report Generator
- Streamlit dashboard to:
  - Select a user
  - Inspect posts + DMs
  - Run a complete safety audit
  - View structured JSON outputs
  - Visualise risk levels with a bar chart
  - Download the final report as a `.txt` file

---

## 🗂 Folder structure

```text
ai-safety-auditor/
├─ app.py                     # Streamlit app (UI + pipeline)
├─ agents.py                  # All LLM-based safety agents
├─ generate_synthetic_data.py # Script to create synthetic data
├─ requirements.txt
├─ README.md
├─ data/
│  ├─ users.csv               # Generated users
│  ├─ posts.csv               # Generated posts
│  └─ interactions.csv        # Generated DMs
└─ policies/
   └─ safety_policies.txt     # Simplified company policies
