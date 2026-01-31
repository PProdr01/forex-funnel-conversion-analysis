import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import os


# -----------------------------
# MAKE SURE OUTPUT FOLDERS EXIST
# -----------------------------
os.makedirs("data/raw", exist_ok=True)

# -----------------------------
# CONFIG
# -----------------------------
N_USERS = 10000
START_DATE = datetime(2024, 1, 1)

COUNTRIES = ["CY", "GR", "UK", "DE", "FR"]
CHANNELS = ["organic", "paid", "referral", "affiliate"]
DEVICES = ["mobile", "desktop"]
CAMPAIGNS = {
    "paid": ["google_search", "tiktok_ads", "meta_ads"],
    "affiliate": ["finblog_fx", "signals_group"],
    "organic": [None],
    "referral": [None],
}

np.random.seed(42)
random.seed(42)

# -----------------------------
# HELPERS
# -----------------------------
def random_date(start, days_range=90):
    return start + timedelta(days=np.random.randint(0, days_range),
                             hours=np.random.randint(0, 24),
                             minutes=np.random.randint(0, 60))


def event(user_id, name, time, channel, country, device, campaign=None,
          deposit_amount=None, trade_volume=None):
    return {
        "user_id": user_id,
        "event_time": time,
        "event_name": name,
        "channel": channel,
        "country": country,
        "device": device,
        "campaign": campaign,
        "deposit_amount": deposit_amount,
        "trade_volume": trade_volume,
    }

# -----------------------------
# GENERATE USERS
# -----------------------------
events = []

for user_id in range(1, N_USERS + 1):

    channel = np.random.choice(CHANNELS, p=[0.4, 0.35, 0.15, 0.10])
    country = np.random.choice(COUNTRIES)
    device = np.random.choice(DEVICES, p=[0.6, 0.4])
    campaign = random.choice(CAMPAIGNS[channel])

    t = random_date(START_DATE)

    # VISIT (everyone)
    events.append(event(user_id, "visit", t, channel, country, device, campaign))

    # SIGN UP
    if np.random.rand() < 0.45:
        t += timedelta(minutes=np.random.randint(5, 60))
        events.append(event(user_id, "sign_up", t, channel, country, device, campaign))
    else:
        continue

    # KYC START
    if np.random.rand() < (0.85 if device == "desktop" else 0.7):
        t += timedelta(minutes=np.random.randint(5, 120))
        events.append(event(user_id, "kyc_start", t, channel, country, device, campaign))
    else:
        continue

    # KYC APPROVED
    if np.random.rand() < 0.75:
        t += timedelta(hours=np.random.randint(1, 48))
        events.append(event(user_id, "kyc_approved", t, channel, country, device, campaign))
    else:
        continue

    # FIRST DEPOSIT
    if np.random.rand() < (0.6 if channel in ["paid", "affiliate"] else 0.45):
        deposit = round(np.random.lognormal(mean=5, sigma=0.6), 2)
        t += timedelta(hours=np.random.randint(1, 72))
        events.append(event(user_id, "first_deposit", t, channel, country, device,
                            campaign, deposit_amount=deposit))
    else:
        continue

    # FIRST TRADE
    if np.random.rand() < 0.8:
        volume = round(deposit * np.random.uniform(0.5, 3), 2)
        t += timedelta(minutes=np.random.randint(10, 180))
        events.append(event(user_id, "first_trade", t, channel, country, device,
                            campaign, trade_volume=volume))
    else:
        continue

    # RETENTION (7D)
    if np.random.rand() < 0.4:
        t += timedelta(days=np.random.randint(1, 7))
        volume = round(volume * np.random.uniform(0.5, 2), 2)
        events.append(event(user_id, "retained_7d", t, channel, country, device,
                            campaign, trade_volume=volume))

# -----------------------------
# SAVE DATA
# -----------------------------
df = pd.DataFrame(events).sort_values(["user_id", "event_time"])
df.to_csv("data/raw/events.csv", index=False)

print(f"Generated {len(df)} events for {N_USERS} users")
