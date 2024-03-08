# gen-time-series-analysis

Time series analysis using Gen. This code is based entirely on the [Gen Experiment Repo](https://github.com/probcomp/pldi2019-gen-experiments).

## Getting Started

### Dependencies

- Python 3.x
- Julia

### Installing

- Clone the repository using `git clone <repo_url>`
- Move to the repository directory: `cd gen-time-series-analysis`
- Install Python dependencies: `pip install -r requirements.txt`
- Set up the Julia environment:
  - Start Julia and activate the project environment: `julia --project=.` 
  - Install the required packages: `] instantiate`

### Data

Data should be placed in the `src/data` directory. The data should be in CSV format with the first column as the time index and the second column as the value, without headers.

As an example, a python script `get_stock_data.py` is provided to fetch time series stock prices. The script can be run using `python get_stock_data.py <ticker>`.

### Running the model

The model can be run using the following command:

```
./run.sh <filename>
```

For example if your data is in `resources/data/nvda.csv`, you can run the model using:

```
./run.sh nvda.csv
```

### Visualizing the results
Once the pipeline has ran, the results can be visualized using the following command:

```
python process_results.py
```

This script will create figures in the `results` directory for each json file.

### References

For more information please refer to the following resources:

- [Gen: a general-purpose probabilistic programming system with programmable inference](https://dl.acm.org/doi/10.1145/3314221.3314642)
- [Scalable Structure Learning, Inference, and Analysis with Probabilistic Programs](https://dspace.mit.edu/handle/1721.1/147226)
- [Time Series Structure Discovery via Probabilistic Program Synthesis](https://arxiv.org/abs/1611.07051)