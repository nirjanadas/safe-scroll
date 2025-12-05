import os
from pathlib import Path

import streamlit as st
import pandas as pd

from agents import (
    underage_risk_agent,
    content_risk_agent,
    interaction_risk_agent,
    policy_violation_agent,
    report_generator_agent,
)

POLICY_PATH = Path("policies") / "safety_policies.txt"


def load_data():
    data_dir = Path("data")
    users = pd.read_csv(data_dir / "users.csv")
    posts = pd.read_csv(data_dir / "posts.csv")
    interactions = pd.read_csv(data_dir / "interactions.csv")
    return users, posts, interactions


def load_policies() -> str:
    if POLICY_PATH.exists():
        return POLICY_PATH.read_text(encoding="utf-8")
    return "No policies found."


def main():
    st.set_page_config(
        page_title="AI Safety & Risk Auditor",
        page_icon="🛡️",
        layout="wide",
    )

    st.title("🛡️ AI Safety & Risk Auditor for Social Platforms")
    st.write(
        """
This tool simulates an **internal Trust & Safety system** for a social platform.

It uses multi-agent GenAI to:
- Analyze user posts and DMs
- Detect underage risk, bullying, self-harm, grooming patterns, and substance abuse
- Map findings to company safety policies
- Generate a human-readable **Safety Report** with a final recommended action

All data here is synthetic and for research/demo purposes only.
"""
    )

    users, posts, interactions = load_data()
    policies_text = load_policies()

    st.sidebar.header("User Selection")
    selected_user_id = st.sidebar.selectbox(
        "Choose a user to audit", options=users["user_id"].tolist()
    )

    st.sidebar.markdown("---")
    st.sidebar.write("Users table preview:")
    st.sidebar.dataframe(users.head(), height=200)

    user_row = users[users["user_id"] == selected_user_id].iloc[0].to_dict()
    user_posts_df = posts[posts["user_id"] == selected_user_id]
    user_interactions_df = interactions[
        (interactions["from_user"] == selected_user_id)
        | (interactions["to_user"] == selected_user_id)
    ]

    st.markdown("## 👤 User Profile")
    col_profile, col_posts = st.columns([1, 2])

    with col_profile:
        st.write("**User ID:**", user_row["user_id"])
        st.write("**Declared age:**", int(user_row["age"]))
        st.write("**Account type:**", user_row["account_type"])
        st.write("**Created at:**", str(user_row["created_at"]))

    with col_posts:
        st.write("**Recent Posts (sample):**")
        st.dataframe(
            user_posts_df[["post_id", "text", "timestamp"]].head(10),
            height=250,
        )

    st.markdown("## 📩 Interactions (DMs)")
    if not user_interactions_df.empty:
        st.dataframe(user_interactions_df, height=200)
    else:
        st.write("_No interactions found for this user in the sample data._")

    st.markdown("---")
    st.markdown("## 🚨 Run Safety Audit")

    if st.button("Run Multi-Agent Safety Audit"):
        # basic key check
        if not os.getenv("OPENAI_API_KEY") or "YOUR_OPENAI_API_KEY_HERE" in os.getenv(
            "OPENAI_API_KEY", ""
        ):
            st.error(
                "OPENAI_API_KEY environment variable is not set. Please configure it before running the audit."
            )
            return

        with st.spinner("Agents are analyzing this user..."):
            posts_payload = user_posts_df[["post_id", "text"]].to_dict(orient="records")

            users_age_map = dict(zip(users["user_id"], users["age"]))
            inter_payload = []
            for _, row in user_interactions_df.iterrows():
                r = row.to_dict()
                r["from_age"] = int(users_age_map.get(r["from_user"], -1))
                r["to_age"] = int(users_age_map.get(r["to_user"], -1))
                inter_payload.append(r)

            underage_res = underage_risk_agent(user_row, posts_payload)
            content_res = content_risk_agent(posts_payload)
            interaction_res = interaction_risk_agent(user_row, inter_payload)

            aggregated_findings = {
                "underage": underage_res,
                "content": content_res,
                "interactions": interaction_res,
            }

            policy_res = policy_violation_agent(policies_text, aggregated_findings)
            report_res = report_generator_agent(
                user_row, underage_res, content_res, interaction_res, policy_res
            )

        st.success("Safety audit completed.")

        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown("### 🧠 Underage Risk")
            st.json(underage_res)

            st.markdown("### 🎭 Content Risk (aggregated)")
            if "overall" in content_res:
                st.json(content_res["overall"])
            else:
                st.json(content_res)

            st.markdown("### 🤝 Interaction / Grooming Risk")
            st.json(interaction_res)

        with col_right:
            # Risk chart
            st.markdown("### 📊 Risk Overview (Content)")
            risk_map = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
            if "overall" in content_res:
                overall = content_res["overall"]
                bullying = risk_map.get(overall.get("bullying_risk", "none"), 0)
                selfharm = risk_map.get(overall.get("self_harm_risk", "none"), 0)
                sexual = risk_map.get(overall.get("sexual_exploitation_risk", "none"), 0)
                substance = risk_map.get(
                    overall.get("substance_abuse_risk", "none"), 0
                )

                risk_df = pd.DataFrame(
                    {
                        "Risk type": [
                            "Bullying",
                            "Self-harm",
                            "Sexual exploitation",
                            "Substance abuse",
                        ],
                        "Severity (0–4)": [bullying, selfharm, sexual, substance],
                    }
                ).set_index("Risk type")

                st.bar_chart(risk_df)
            else:
                st.write("No aggregated content risk data available.")

            st.markdown("### 📜 Policy Evaluation")
            st.json(policy_res)

            st.markdown("### 🔝 Final Safety Report")
            if report_res:
                st.write(
                    "**Title:**",
                    report_res.get("risk_title", "Safety Report"),
                )
                st.write(
                    "**Overall Risk Score:**",
                    report_res.get("overall_risk_score", "N/A"),
                )
                st.write("**Summary:**", report_res.get("risk_summary", ""))
                st.markdown("---")
                st.markdown(report_res.get("markdown_report", ""))
            else:
                st.write("No report generated.")

            # Simple text download for the report
            if report_res:
                report_text = (
                    f"# {report_res.get('risk_title', 'Safety Report')}\n\n"
                )
                report_text += report_res.get("markdown_report", "")
                st.download_button(
                    "⬇ Download Report as .txt",
                    data=report_text,
                    file_name=f"safety_report_{selected_user_id}.txt",
                    mime="text/plain",
                )

    st.markdown("---")
    st.markdown("### 📘 Safety Policies Used")
    with st.expander("View policies"):
        st.text(load_policies())


if __name__ == "__main__":
    main()
