import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import json
import os
import re
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def rescale_linear(xs, yl, yh):
    """Rescale values linearly between [yl, yh]."""
    xl = min(xs)
    xh = max(xs)
    slope = float(yh - yl) / (xh - xl)
    intercept = yh - xh * slope
    return slope* xs + intercept

def unscale_linear(xs, yl, yh, xl, xh):
    """Rescale values linearly between [xl, xh]."""
    slope = float(yh - yl) / (xh - xl)
    intercept = yh - xh * slope
    return (xs - intercept) / slope

def convert_timestamps_to_dates(timestamps):
    # Convert timestamps from seconds to datetime objects
    return [datetime.datetime.fromtimestamp(ts) for ts in timestamps]

def get_model_name_from_filename(filename: str):

    pattern = re.compile("lightweight-(.*?)_ntest")
    match = pattern.search(filename)
    extracted_part = match.group(1) if match else "No match found"

    return extracted_part

def get_max_min(ticker: str):

    datafile = f"src/data/{ticker}.csv"
    df = pd.read_csv(datafile, header=None, names=['datetime', 'price'])

    x_max = df['datetime'].max()
    x_min = df['datetime'].min()

    y_max = df['price'].max()
    y_min = df['price'].min()

    return (x_min, y_min), (x_max, y_max)

if __name__ == "__main__":

    # get all json in /results
    results = os.listdir('results')
    results = [r for r in results if r.endswith('.json')]

    for file in results:
        with open(f"results/{file}", 'r') as f:
            results = json.load(f)

            predictions = results['statistics'][-1]['predictions_held_out']
            title = get_model_name_from_filename(file)
            (x_min, y_min), (x_max, y_max) = get_max_min(title)

            xs_train = unscale_linear(np.array(results['xs_train']), 0, 1, x_min, x_max)
            ys_train = unscale_linear(np.array(results['ys_train']), -1, 1, y_min, y_max)
            xs_test = unscale_linear(np.array(results['xs_test']), 0, 1, x_min, x_max)
            ys_test = unscale_linear(np.array(results['ys_test']), -1, 1, y_min, y_max)
            predictions = unscale_linear(np.array(predictions), -1, 1, y_min, y_max)
            average_prediction = np.mean(predictions, axis=0)

            MaxNLocator(integer=True)

            # Convert your timestamp arrays/lists to readable dates
            xs_train_dates = convert_timestamps_to_dates(xs_train)
            xs_test_dates = convert_timestamps_to_dates(xs_test)

            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
            plt.xticks(rotation=45, ha='right')

            ax.plot(xs_train_dates, ys_train, marker='.', linestyle='--', color='k', label='Observed Data')
            ax.plot(xs_test_dates, average_prediction, linestyle='-', color='b', label='Average Prediction')

            for p in predictions:
                ax.plot(xs_test_dates, p, linestyle='-', color='g', alpha=.05)
            ax.plot([], [], color='g', label='Predictions')
            ax.scatter(xs_test_dates, ys_test, marker='+', color='r', s=30, label='Held-out Data')
            ax.legend(framealpha=0, loc='upper left')
            ax.set_xlabel('Date', fontsize=12) 
            ax.set_ylabel('Price (USD)', fontsize=12)
            ax.set_title(f'{title}', fontsize=13)

            # set a high dpi 
            fig.set_dpi(250)

            # set xlim to the last few dates
            ax.set_xlim(xs_train_dates[-100], xs_test_dates[-1])

            # tight_layout() adjusts the plot to fit into the figure
            plt.tight_layout()
            # Ensure the results directory exists
            results_dir = 'results'
            os.makedirs(results_dir, exist_ok=True)

            # Save the figure
            fig.savefig(f'{results_dir}/prediction_plot_{file}.png')
    pass
