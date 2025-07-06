# 🤖 Intelligent CRM Agent – AI Marketing Agent

This project showcases a smart Customer Relationship Management (CRM) system built using AI agents, LangGraph, and real transactional data. The agent is designed to analyze customer behavior, segment audiences using RFM analysis, and generate personalized marketing campaigns and emails. It also integrates human review into sensitive operations to ensure reliability and control.

---

## 🏗️ Project Architecture

```text
┌─────────────────┐    ┌────────────────────┐    ┌─────────────────┐
│   Frontend      │    │   AI Agent Engine  │    │   Database      │
│   (Chat UI)     │◄──►│   (LangGraph Flow) │◄──►│   (PostgreSQL)  │
└─────────────────┘    └────────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌────────────────────┐
                       │  MCP Marketing API │
                       │    (Tool Server)   │
                       └────────────────────┘
                       

# 🚀 Features

### 🧠 Smart Customer Behavior Analysis  
Automatically analyzes historical purchase data and behavioral patterns to extract actionable insights.

### 📧 Personalized Email Campaigns  
Generates marketing emails tailored to individual customers based on their behaviors, preferences, and segment.

### 🎯 RFM-Based Segmentation  
Categorizes customers into meaningful groups using Recency, Frequency, and Monetary metrics:
- 🏆 Champions
- ⚠️ At-Risk
- 💰 Big Spenders
- 🆕 Recent Buyers
- 🔁 Frequent Buyers
- 👥 Others

### ✋ Human-in-the-Loop Review  
Adds a human approval step before executing sensitive operations like launching mass campaigns or triggering automated emails.

### 📊 Live Retail Data Integration  
Connects directly to a PostgreSQL database containing real transaction data for up-to-date insights and decisions.

### 🔄 Campaign Types Supported  
- **Re-engagement**: Reconnect with inactive or slipping customers  
- **Referral**: Leverage loyal, high-value customers to generate referrals  
- **Loyalty**: Reward and retain your most valuable users
