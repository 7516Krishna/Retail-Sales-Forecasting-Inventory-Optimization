def detect_spikes(df):
    df = df.copy()

    mean = df['sales'].mean()
    std = df['sales'].std()

    df['anomaly'] = df['sales'] > (mean + 2 * std)

    return df