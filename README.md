# BaSys4IPPS_IFW_Agent
Calculation of failure probabilities using uniform outlier scores of machine components determined from regular test cycle (Python).

# How to Install
To execute signed python (<3.11) scripts in powershell, it necessary to run the following command with administrator rights in a powershell terminal:
````pwsh
Set-ExecutionPolicy RemoteSigned
````
To create a virtual environment and install the setup, use:
```` 
# Use virtual environment (example for Windows OS)

py -3 -m venv venv3
./venv3/Scripts/activate

# Install the project
pip install -e .[dev]
````

# How to Use
Use the cli to predict outliers based on the training data in *./examples/train* (*.csv files), where each file
represents a sensor. The option *--test-index* denotes the index of the timeseries that is tested for being an outlier.
The index range used for training can also be adjusted. 
Use ``` basys-agent load-data fit-predict --help ```.

````console
basys-agent -p ./config.yaml load-data --csv-dir "./examples/train" --sensor 5 fit-predict --train-end 50 --test-index 115
````

Use configuration file *./config.yaml* to adjust the training and prediction process. When using tsfresh feature extraction,
adjust the corresponding json file (e.g. *"./examples/tsfresh_features.json"*) and enable or disable features to extract from the data.
