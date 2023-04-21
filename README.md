# Run Guide
## 1. Data Collection
We first want to collect and store data from our respective APIs and pages. We want to run the `collector.py` script 7 times (best number according ot testing to ensure we have enough data for all tables) To do this, we run the following command:

`./run_collector.sh 7`

<sub>(If you run into a permission error on Mac, run `chmod +x run_collector.sh`). You may also need to change the version of python in the run_collector.sh file to match your version of python</sub>

The script will run the collector.py file 7 times to ensure we collect over >100 rows for each table.

## 2. Data Visualization
We then want to visualize the data we collected. To do this, run the `visualizer.py` file.