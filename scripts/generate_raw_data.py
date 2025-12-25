import pandas as pd
import numpy as np
import datetime
import random
import uuid

# Configuration
TOTAL_TXS = 15000
START_DATE = datetime.date.today() - datetime.timedelta(days=180)

# 1. Generate Timestamps (Non-uniform distribution to simulate trends)
dates = []
current_date = START_DATE
for i in range(180):
    # Logarithmic growth in daily transactions
    daily_count = int(50 * np.log(i + 5) * (1 + np.random.normal(0, 0.2)))
    daily_count = max(10, daily_count)
    
    # Add timestamps for this day
    for _ in range(daily_count):
        # random time in day
        second = random.randint(0, 86399)
        dt = current_date + datetime.timedelta(seconds=second)
        dates.append(dt)
    
    current_date += datetime.timedelta(days=1)

# Truncate or expand to match target loose size
df = pd.DataFrame({'block_time': dates})

# 2. Generate Wallet Addresses (Simulate Pareto Principle: Whales vs One-time users)
num_unique_wallets = int(len(df) * 0.4) # 40% unique addresses
wallet_pool = [f'0x{uuid.uuid4().hex[:40]}' for _ in range(num_unique_wallets)]

# Assign wallets using zipfian distribution (some highly active, most once)
# Simple approach: 
# 10% of wallets do 60% of txs (Power users/Bots)
# 90% of wallets do 40% of txs
users_high_activity = wallet_pool[:int(num_unique_wallets*0.1)]
users_low_activity = wallet_pool[int(num_unique_wallets*0.1):]

wallets = []
for _ in range(len(df)):
    if random.random() < 0.6:
        wallets.append(random.choice(users_high_activity))
    else:
        wallets.append(random.choice(users_low_activity))

df['from_address'] = wallets[:len(df)]

# 3. Generate Values (Entry Volume simulation)
# Some are dust (<$1), some are real entry (>$10)
df['value_usd'] = np.random.exponential(scale=25, size=len(df))

# 4. Generate metadata
df['tx_hash'] = [f'0x{uuid.uuid4().hex}' for _ in range(len(df))]
df['method_id'] = np.random.choice(['0x60806040', '0xa9059cbb', '0x23b872dd'], size=len(df))

# Save to CSV
output_path = "data/dune_raw_exports.csv"
df.to_csv(output_path, index=False)
print(f"Generated {len(df)} raw transactions to {output_path}")
