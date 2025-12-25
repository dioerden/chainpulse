import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# 1. Ingest Raw Data (Simulating Dune Analytics Export)
try:
    # In a real scenario, this would be 'dune_export.csv'
    df = pd.read_csv('data/dune_raw_exports.csv')
    df['block_time'] = pd.to_datetime(df['block_time'])
    print(f"✅ Loaded {len(df)} raw transactions.")
except FileNotFoundError:
    print("❌ Error: 'data/dune_raw_exports.csv' not found. Run 'generate_raw_data.py' first.")
    exit()

# 2. Sybil Filtering Logic (The "Special Sauce")
print("🕵️  Applying Sybil Filters...")

# Calculate Wallet Metadata
wallet_stats = df.groupby('from_address').agg({
    'tx_hash': 'count',
    'value_usd': 'sum',
    'block_time': ['min', 'max']
})
wallet_stats.columns = ['lifetime_tx_count', 'total_volume_usd', 'first_seen', 'last_seen']

# Calculate Wallet Age (Days)
wallet_stats['wallet_age_days'] = (wallet_stats['last_seen'] - wallet_stats['first_seen']).dt.days

# Identify "Gameable" Wallets
# Logic: Must have >5 Txs, >$10 Volume, and active for >1 week
organic_wallets = wallet_stats[
    (wallet_stats['lifetime_tx_count'] > 5) & 
    (wallet_stats['total_volume_usd'] >= 10.0) &
    (wallet_stats['wallet_age_days'] > 7)
].index

print(f"   - Total Unique Wallets: {len(wallet_stats)}")
print(f"   - Organic Wallets: {len(organic_wallets)}")
print(f"   - Bot/Sybil Ratio: {(1 - len(organic_wallets)/len(wallet_stats)):.1%}")

# 3. Time-Series Aggregation (DAU)
df['date'] = df['block_time'].dt.date

# Raw DAU (Reported)
daily_raw = df.groupby('date')['from_address'].nunique()

# Organic DAU (Filtered)
df_organic = df[df['from_address'].isin(organic_wallets)]
daily_organic = df_organic.groupby('date')['from_address'].nunique()

# Merge for plotting
dau_data = pd.DataFrame({'Reported DAU': daily_raw, 'Organic DAU': daily_organic}).fillna(0)

# 4. Visualization: usage Divergence
fig = go.Figure()

# Reported DAU (Grey Area)
fig.add_trace(go.Scatter(
    x=dau_data.index, y=dau_data['Reported DAU'],
    name="Reported Users (Raw)",
    fill='tozeroy',
    line=dict(color='gray', width=1),
    fillcolor='rgba(128, 128, 128, 0.2)'
))

# Organic DAU (Green Line)
fig.add_trace(go.Scatter(
    x=dau_data.index, y=dau_data['Organic DAU'],
    name="Organic Users (Validated)",
    line=dict(color='#00C853', width=3)
))

# Cosmetic Formatting
fig.update_layout(
    title_text="<b>Real Traction Analysis:</b> Organic vs Reported DAU",
    template="plotly_white",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig.update_yaxes(title_text="Daily Active Wallets")

# Save Output
output_path = "assets/traction_chart.png"
# Write as Image for README (requires kaleido)
fig.write_image(output_path, scale=2)
# Also save HTML for interactive view
fig.write_html("scripts/traction_chart.html")

print(f"✅ Chart saved to {output_path}")

