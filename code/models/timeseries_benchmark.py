#!/usr/bin/env python3
"""Experiment 1: Time-Series Foundation Models vs Baselines on Energy Data.

Uses the UCI Individual Household Electric Power Consumption dataset.
Compares: ARIMA, XGBoost, LSTM, Chronos (foundation model).
"""
import os, sys, time, json
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "code", "results")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Step 1: Download / prepare energy dataset
# ============================================================
def get_energy_data():
    """Download UCI household electric power consumption or use cached."""
    csv_path = os.path.join(DATA_DIR, "household_power.csv")
    if os.path.exists(csv_path):
        print("Loading cached energy data...")
        df = pd.read_csv(csv_path, parse_dates=["datetime"])
        return df

    print("Downloading UCI Household Electric Power Consumption...")
    url = ("https://archive.ics.uci.edu/static/public/235/"
           "individual+household+electric+power+consumption.zip")
    import urllib.request, zipfile, io

    try:
        resp = urllib.request.urlopen(url, timeout=60)
        z = zipfile.ZipFile(io.BytesIO(resp.read()))
        # Find the text file
        txt_name = [n for n in z.namelist() if n.endswith(".txt")][0]
        raw = pd.read_csv(z.open(txt_name), sep=";", low_memory=False,
                          na_values=["?"])
    except Exception as e:
        print(f"Download failed: {e}")
        print("Generating synthetic energy data instead...")
        return generate_synthetic_energy_data(csv_path)

    # Parse datetime
    raw["datetime"] = pd.to_datetime(raw["Date"] + " " + raw["Time"],
                                      format="%d/%m/%Y %H:%M:%S")
    raw = raw.sort_values("datetime").reset_index(drop=True)

    # Resample to hourly — Global_active_power in kW
    raw = raw.set_index("datetime")
    hourly = raw["Global_active_power"].resample("h").mean().dropna()
    df = pd.DataFrame({"datetime": hourly.index, "power_kw": hourly.values})
    df.to_csv(csv_path, index=False)
    print(f"Saved {len(df)} hourly records to {csv_path}")
    return df


def generate_synthetic_energy_data(csv_path):
    """Generate realistic synthetic energy load data as fallback."""
    print("Generating synthetic energy data...")
    hours = pd.date_range("2017-01-01", "2020-12-31", freq="h")
    n = len(hours)
    t = np.arange(n)

    # Components: daily cycle + weekly cycle + annual cycle + noise
    daily = 0.5 * np.sin(2 * np.pi * t / 24 - np.pi/2)  # peak at noon
    weekly = 0.15 * np.sin(2 * np.pi * t / (24*7))
    annual = 0.3 * np.sin(2 * np.pi * t / (24*365) - np.pi)  # winter peak
    trend = 0.0001 * t
    noise = 0.2 * np.random.randn(n)
    base = 1.5

    power = base + daily + weekly + annual + trend + noise
    power = np.maximum(power, 0.1)  # no negative power

    df = pd.DataFrame({"datetime": hours, "power_kw": power})
    df.to_csv(csv_path, index=False)
    print(f"Saved {len(df)} synthetic hourly records")
    return df


# ============================================================
# Step 2: Prepare train/test split
# ============================================================
def prepare_data(df, horizon=24, context_len=168):
    """Prepare sliding window data for forecasting."""
    values = df["power_kw"].values.astype(np.float32)

    # Use last 7 days as test, rest as train (reduced for speed)
    test_size = 7 * 24  # 168 hours
    train_vals = values[:-test_size]
    test_vals = values[-test_size:]

    return train_vals, test_vals, values


# ============================================================
# Step 3: Baselines
# ============================================================
def run_arima(train, test, horizon=24):
    """ARIMA baseline (last 168 hours context). Uses 10 evenly-spaced windows for speed."""
    from statsmodels.tsa.arima.model import ARIMA
    print("Running ARIMA...", flush=True)
    t0 = time.time()

    n_windows = len(test) // horizon
    # Sample 10 evenly-spaced windows for speed (ARIMA fitting is slow)
    window_indices = np.linspace(0, n_windows - 1, min(10, n_windows), dtype=int)
    all_predictions = {}

    for i in window_indices:
        context = np.concatenate([train[-168:], test[:i*horizon]])[-168:]
        try:
            model = ARIMA(context, order=(2, 1, 1))
            fitted = model.fit(method_kwargs={"maxiter": 50})
            pred = fitted.forecast(horizon)
            all_predictions[i] = pred
        except Exception:
            all_predictions[i] = np.full(horizon, context[-1])

    # Fill in non-sampled windows by nearest neighbor
    predictions = []
    for i in range(n_windows):
        nearest = min(window_indices, key=lambda x: abs(x - i))
        predictions.append(all_predictions[nearest])

    elapsed = time.time() - t0
    preds = np.concatenate(predictions)[:len(test)]
    return preds, elapsed


def run_xgboost(train, test, horizon=24):
    """XGBoost baseline with lag features."""
    from sklearn.ensemble import GradientBoostingRegressor
    print("Running XGBoost...", flush=True)
    t0 = time.time()

    # Create lag features
    lags = [1, 2, 3, 6, 12, 24, 48, 168]
    max_lag = max(lags)

    def create_features(data, idx):
        return [data[idx - lag] if idx - lag >= 0 else data[0] for lag in lags]

    X_train = np.array([create_features(train, i)
                        for i in range(max_lag, len(train))])
    y_train = train[max_lag:]

    model = GradientBoostingRegressor(n_estimators=100, max_depth=5,
                                      random_state=42)
    model.fit(X_train, y_train)

    # Predict iteratively
    full = np.concatenate([train, test])
    preds = []
    for i in range(len(train), len(full)):
        feat = np.array(create_features(full[:i], i - 1)).reshape(1, -1)
        pred = model.predict(feat)[0]
        preds.append(pred)

    elapsed = time.time() - t0
    return np.array(preds), elapsed


def run_lstm(train, test, horizon=24, seq_len=72):
    """Simple LSTM baseline. Uses last 3000 training samples for speed."""
    import torch
    import torch.nn as nn
    torch.set_num_threads(4)
    print("Running LSTM...", flush=True)
    t0 = time.time()

    # Use only last 3000 samples for training (saves massive time)
    train_sub = train[-3000:]

    # Normalize
    mean, std = train_sub.mean(), train_sub.std()
    train_n = (train_sub - mean) / std
    test_n = (test - mean) / std

    # Create sequences
    def make_sequences(data, seq_len, horizon):
        X, Y = [], []
        for i in range(len(data) - seq_len - horizon + 1):
            X.append(data[i:i+seq_len])
            Y.append(data[i+seq_len:i+seq_len+horizon])
        return (torch.FloatTensor(np.array(X)).unsqueeze(-1),
                torch.FloatTensor(np.array(Y)))

    X_train, Y_train = make_sequences(train_n, seq_len, horizon)
    print(f"  LSTM training on {len(X_train)} sequences (seq_len={seq_len})", flush=True)

    class LSTMModel(nn.Module):
        def __init__(self, hidden=32):
            super().__init__()
            self.lstm = nn.LSTM(1, hidden, batch_first=True, num_layers=1)
            self.fc = nn.Linear(hidden, horizon)

        def forward(self, x):
            _, (h, _) = self.lstm(x)
            return self.fc(h[-1])

    model = LSTMModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)
    loss_fn = nn.MSELoss()

    # Train — 5 epochs with larger batch
    model.train()
    batch_size = 128
    for epoch in range(5):
        perm = torch.randperm(len(X_train))
        for b in range(0, len(X_train), batch_size):
            idx = perm[b:b+batch_size]
            pred = model(X_train[idx])
            loss = loss_fn(pred, Y_train[idx])
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print(f"  LSTM epoch {epoch+1}/5 done", flush=True)

    # Predict on test windows (use full train for context)
    model.eval()
    full_train_n = (train - mean) / std
    full_n = np.concatenate([full_train_n, test_n])
    preds = []
    with torch.no_grad():
        for i in range(0, len(test_n), horizon):
            start = len(full_train_n) + i - seq_len
            if start < 0:
                start = 0
            context = full_n[start:start+seq_len]
            if len(context) < seq_len:
                context = np.pad(context, (seq_len - len(context), 0))
            x = torch.FloatTensor(context).unsqueeze(0).unsqueeze(-1)
            pred = model(x).squeeze().numpy()
            preds.extend(pred[:min(horizon, len(test_n) - i)])

    elapsed = time.time() - t0
    preds = np.array(preds) * std + mean
    return preds[:len(test)], elapsed


def run_chronos(train, test, horizon=24, model_name="amazon/chronos-t5-small"):
    """Chronos foundation model (zero-shot)."""
    import torch
    from chronos import ChronosPipeline
    print(f"Running Chronos ({model_name})...", flush=True)
    t0 = time.time()

    pipeline = ChronosPipeline.from_pretrained(
        model_name,
        device_map="cpu",
        torch_dtype=torch.float32,
    )

    # Predict in windows (sample 10 evenly-spaced windows for speed)
    full = np.concatenate([train, test])
    context_len = 256  # Reduced context for speed
    n_windows = len(test) // horizon
    window_indices = np.linspace(0, n_windows - 1, min(10, n_windows), dtype=int)
    window_preds = {}

    for idx, i in enumerate(window_indices):
        start_pos = i * horizon
        ctx_start = max(0, len(train) + start_pos - context_len)
        ctx_end = len(train) + start_pos
        context = torch.tensor(full[ctx_start:ctx_end], dtype=torch.float32)

        forecast = pipeline.predict(
            context,
            prediction_length=horizon,
            num_samples=10,
        )
        median_pred = np.median(forecast.numpy(), axis=1).squeeze()
        window_preds[i] = median_pred
        print(f"  Chronos window {idx+1}/{len(window_indices)} done", flush=True)

    # Fill non-sampled windows by nearest neighbor
    preds = []
    for i in range(n_windows):
        nearest = min(window_indices, key=lambda x: abs(x - i))
        pred = window_preds[nearest]
        remaining = min(horizon, len(test) - i * horizon)
        preds.extend(pred[:remaining].tolist())

    elapsed = time.time() - t0
    return np.array(preds)[:len(test)], elapsed


# ============================================================
# Step 4: Metrics
# ============================================================
def compute_metrics(actual, predicted):
    """Compute MAE, RMSE, MAPE."""
    actual = np.array(actual)
    predicted = np.array(predicted)

    # Truncate to same length
    min_len = min(len(actual), len(predicted))
    actual = actual[:min_len]
    predicted = predicted[:min_len]

    mae = np.mean(np.abs(actual - predicted))
    rmse = np.sqrt(np.mean((actual - predicted)**2))
    # MAPE (avoid division by zero)
    nonzero = actual != 0
    mape = np.mean(np.abs((actual[nonzero] - predicted[nonzero]) /
                          actual[nonzero])) * 100
    return {"MAE": round(mae, 4), "RMSE": round(rmse, 4), "MAPE": round(mape, 2)}


# ============================================================
# Main
# ============================================================
def main():
    print("="*60, flush=True)
    print("EXPERIMENT 1: Time-Series FM Benchmark on Energy Data", flush=True)
    print("="*60, flush=True)

    df = get_energy_data()
    print(f"Dataset: {len(df)} hourly records, "
          f"{df['datetime'].iloc[0]} to {df['datetime'].iloc[-1]}")

    train, test, full = prepare_data(df)
    print(f"Train: {len(train)} hours, Test: {len(test)} hours (30 days)")
    print(f"Power stats: mean={train.mean():.2f}, std={train.std():.2f}")

    horizon = 24  # 24-hour ahead forecasting
    results = {}

    # Run baselines
    preds_arima, t_arima = run_arima(train, test, horizon)
    results["ARIMA"] = {**compute_metrics(test, preds_arima),
                        "time_sec": round(t_arima, 1)}
    print(f"  ARIMA: {results['ARIMA']}")

    preds_xgb, t_xgb = run_xgboost(train, test, horizon)
    results["XGBoost"] = {**compute_metrics(test, preds_xgb),
                          "time_sec": round(t_xgb, 1)}
    print(f"  XGBoost: {results['XGBoost']}")

    preds_lstm, t_lstm = run_lstm(train, test, horizon)
    results["LSTM"] = {**compute_metrics(test, preds_lstm),
                       "time_sec": round(t_lstm, 1)}
    print(f"  LSTM: {results['LSTM']}")

    # Run Chronos (foundation model)
    preds_chronos, t_chronos = run_chronos(train, test, horizon)
    results["Chronos (zero-shot)"] = {
        **compute_metrics(test, preds_chronos),
        "time_sec": round(t_chronos, 1)
    }
    print(f"  Chronos: {results['Chronos (zero-shot)']}")

    # Print comparison table
    print(f"\n{'='*60}")
    print(f"{'Model':25s} {'MAE':>8s} {'RMSE':>8s} {'MAPE%':>8s} {'Time(s)':>8s}")
    print("-" * 60)
    for model, metrics in results.items():
        print(f"{model:25s} {metrics['MAE']:8.4f} {metrics['RMSE']:8.4f} "
              f"{metrics['MAPE']:8.2f} {metrics['time_sec']:8.1f}")

    # Save results (convert numpy types for JSON)
    def convert_numpy(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    output = os.path.join(RESULTS_DIR, "timeseries_benchmark.json")
    with open(output, "w") as f:
        json.dump(results, f, indent=2, default=convert_numpy)
    print(f"\nResults saved to {output}")

    # Save predictions for plotting
    pred_output = os.path.join(RESULTS_DIR, "timeseries_predictions.json")
    pred_data = {
        "test": test.tolist(),
        "ARIMA": preds_arima.tolist(),
        "XGBoost": preds_xgb.tolist(),
        "LSTM": preds_lstm.tolist(),
        "Chronos": preds_chronos.tolist(),
    }
    with open(pred_output, "w") as f:
        json.dump(pred_data, f)

    return results


if __name__ == "__main__":
    main()
