# Data loader for Quant Data Manager

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Repository Structure](#repository-structure)
- [Features](#features)
- [Author](#author)

## Introduction

This repository implements a data processing pipeline for trading strategies using MetaTrader and StrategyQuant. The main goal is to automate the extraction and import of trading data, facilitating the optimization of trading strategies. The script utilizes configuration files to manage parameters and logging, ensuring a smooth workflow.

Key functionalities include:
- Loading configuration from YAML files
- Executing MetaTrader and StrategyQuant processes
- Logging the process for better traceability
- Handling CSV file management

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/jhontd03/DataLoadQDM.git
cd DataLoadQDM
pip install -r requirements.txt
```

### Requirements

The project requires Python 3.11.9 and the following key dependencies:

- python-dotenv
- PyYAML
- tqdm

## Usage

Here's a basic example of how to use the main script:

```python
import os
from dotenv import load_dotenv
from config_files import load_yaml, load_init_file
from run_process import start_mt_process, start_sqcli_process
from logger import Logger

# Load environment variables
load_dotenv()

# Load configuration
kwargs = load_yaml('config.yaml')

# Set up logger
logger = Logger(name="ProcessLogger", log_file="logs/process.log")

# Process each trading symbol
for symbol in kwargs['list_symbols']:
    load_init_file(symbol, **kwargs)
    process_mt = start_mt_process(kwargs['path_metatrader_exe'], kwargs['path_config_ini'])
    exit_code = process_mt.wait()
    
    if not exit_code:
        logger.info('Data written to CSV from MetaTrader')
    else:
        logger.error('Failed to write data from MetaTrader')

    # Start StrategyQuant CLI process
    process_sqcli = start_sqcli_process(
        path_sqcli_exe=kwargs['path_sqcli_exe'],
        symbol=symbol,
        instrument=f"{symbol}{kwargs['postfix_instrument_sqx']}",
        timezone=kwargs['timezone'],
        filepath=os.path.join(kwargs['path_export_data_csv'], f'{symbol}_Data.csv'),
    )
    exit_code = process_sqcli.wait()
    
    if not exit_code:
        logger.info('Data imported to Quant Data Manager')
    else:
        logger.error('Failed to import data to Quant Data Manager')
```

## Repository Structure

```
.
│   README.md
│   main.py
│   requirements.txt
│   config.yaml
│   config_files.py
│   run_process.py
│   logger.py
│   template_ea_ini.txt
```

## Features

- **Configuration Management**: Load parameters from YAML and environment files.
- **Process Automation**: Automatically start MetaTrader and StrategyQuant processes.
- **Logging**: Comprehensive logging of the data processing steps.
- **CSV Management**: Handle CSV file creation and deletion efficiently.

## Author

Jhon Jairo Realpe

jhon.td.03@gmail.com
