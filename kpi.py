import pandas as pd
import matplotlib.pyplot as plt

# Mock data for Regional Managers
data = {
    "Regional_Manager": ["RM1", "RM2", "RM3", "RM4", "RM5", "RM6"],
    "Monthly_Profit": [46000, 50000, 43000, 47000, 45000, 44000],  # Individual profits
    "Target_Profit_Per_RM": [46000, 46000, 46000, 46000, 46000, 46000],  # Individual targets
    "Group_Profit": [285000] * 6,  # Group profit for all regions
    "Target_Group_Profit": [275000] * 6,  # Target group profit
    "Customer_Interactions": [30, 28, 25, 20, 27, 26],  # Weekly customer interactions
}

# Create a DataFrame
df = pd.DataFrame(data)

# Calculate Individual Performance Incentives
df["Individual_Performance"] = (df["Monthly_Profit"] / df["Target_Profit_Per_RM"]) * 0.75 * 0.05  # 75% of 5%

# Calculate Group Performance Incentives
df["Group_Performance"] = (df["Group_Profit"] / df["Target_Group_Profit"]) * 0.25 * 0.05  # 25% of 5%

# Calculate Bonus or Penalty Adjustment
group_performance_ratio = df["Group_Profit"].iloc[0] / df["Target_Group_Profit"].iloc[0]
if group_performance_ratio > 1.1:
    df["Bonus_Adjustment"] = 0.05 * 0.10  # 10% bonus
elif group_performance_ratio < 0.9:
    df["Bonus_Adjustment"] = -0.05 * 0.10  # 10% penalty
else:
    df["Bonus_Adjustment"] = 0  # No adjustment

# Calculate Total Payout
df["Total_Payout"] = df["Individual_Performance"] + df["Group_Performance"] + df["Bonus_Adjustment"]

# Add a compliance column for customer interactions
df["Customer_Interactions_Compliance"] = df["Customer_Interactions"].apply(
    lambda x: "Compliant" if x >= 25 else "Non-Compliant"
)

# Display the DataFrame
print("Regional Manager Incentive Data:")
print(df)

# Save to a CSV for Power BI
df.to_csv("Regional_Manager_Incentive_Data.csv", index=False)

# Visualizations
rms = df["Regional_Manager"]
individual_perf = df["Individual_Performance"]
group_perf = df["Group_Performance"]
total_payout = df["Total_Payout"]
compliance = df["Customer_Interactions_Compliance"]

# Bar Chart: Individual vs Group Performance
plt.figure(figsize=(10, 6))
bar_width = 0.35
x = range(len(rms))

plt.bar(x, individual_perf, bar_width, label="Individual Performance", alpha=0.7)
plt.bar([p + bar_width for p in x], group_perf, bar_width, label="Group Performance", alpha=0.7)

plt.xlabel("Regional Managers")
plt.ylabel("Performance Incentives (as % of profit)")
plt.title("Regional Manager KPI: Individual vs Group Performance")
plt.xticks([p + bar_width / 2 for p in x], rms)
plt.legend()
plt.tight_layout()
plt.show()

# Pie Chart: Total Payout Distribution
plt.figure(figsize=(8, 8))
plt.pie(
    total_payout,
    labels=rms,
    autopct="%1.1f%%",
    startangle=140,
    colors=plt.cm.Paired.colors,
)
plt.title("Total Payout Distribution Among Regional Managers")
plt.show()

# Horizontal Bar Chart: Customer Interaction Compliance
plt.figure(figsize=(10, 6))
colors = ["green" if c == "Compliant" else "red" for c in compliance]
plt.barh(rms, df["Customer_Interactions"], color=colors, alpha=0.7)
plt.axvline(25, color="blue", linestyle="--", label="Compliance Threshold (25)")
plt.xlabel("Customer Interactions")
plt.title("Customer Interaction Compliance")
plt.legend()
plt.tight_layout()
plt.show()
