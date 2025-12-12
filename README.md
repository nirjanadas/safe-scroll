<!-- ===================== -->
<!-- SafeScroll App Banner -->
<!-- ===================== -->

<p align="center">
  <img src="assets/safescroll_overview.png" width="100%" />
</p>

<p align="center">
  <img src="assets/safescroll_moderation.png" width="100%" />
</p>

---

# 🛡️ SafeScroll — AI-Powered Social Media Safety Auditor  
**Making your social feed safer — one scroll at a time.**

SafeScroll is an **AI-powered Trust & Safety auditing system** that simulates how modern social media platforms internally detect and respond to harmful content and unsafe user behavior.

It demonstrates how **multi-agent GenAI systems** can be applied to:
- content moderation
- underage safety
- grooming detection
- policy enforcement
- human-readable safety reporting

This project is built for **research, demos, and resume-ready showcasing** of real-world AI safety engineering.

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
 safe-scroll/
├── .streamlit/
│   └── config.toml
├── assets/
│   ├── safescroll_overview.png
│   └── safescroll_moderation.png
├── data/
│   ├── interactions.csv
│   ├── posts.csv
│   └── users.csv
├── policies/
│   └── safety_policies.txt
├── README.md
├── agents.py
├── app.py
├── generate_synthetic_data.py
└── requirements.txt
```
