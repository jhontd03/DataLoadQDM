import subprocess
from typing import List, Optional


def start_mt_process(path_metatrader_exe: str, path_config_ini: str) -> subprocess.Popen:
    """
    Start a MetaTrader process with the specified configuration file.
    
    Parameters
    ----------
    path_metatrader_exe : str
        Full path to the MetaTrader executable file.
    path_config_ini : str
        Full path to the configuration .ini file.
    
    Returns
    -------
    subprocess.Popen
        The subprocess object representing the started MetaTrader process.
    
    Notes
    -----
    Command line arguments are based on MetaTrader documentation:
    https://www.metatrader5.com/en/terminal/help/start_advanced/start
    
    Examples
    --------
    >>> process = start_mt_process("C:/Program Files/MetaTrader5/terminal.exe", 
    ...                            "C:/Users/username/mt5_config.ini")
    """
    command: List[str] = [path_metatrader_exe, f"/config: {path_config_ini}"]
    process: subprocess.Popen = subprocess.Popen(command)
    return process


def start_sqcli_process(
        path_sqcli_exe: str,
        symbol: str,
        instrument: str,
        timezone: str,
        filepath: str,
        additional_args: Optional[List[str]] = None
    ) -> subprocess.Popen:
    """
    Start a StrategyQuant CLI process to import data.
    
    Parameters
    ----------
    path_sqcli_exe : str
        Full path to the StrategyQuant CLI executable.
    symbol : str
        Trading symbol to use for the imported data.
    instrument : str
        Instrument type for the imported data.
    timezone : str
        Timezone for the data timestamps.
    filepath : str
        Path to the data file to be imported.
    additional_args : List[str], optional
        Additional command line arguments to pass to the CLI, by default None.
    
    Returns
    -------
    subprocess.Popen
        The subprocess object representing the started StrategyQuant CLI process.
    
    Notes
    -----
    Command line arguments are based on StrategyQuant documentation:
    https://strategyquant.com/doc/cli-command-line/data-manage-data/
    https://strategyquant.com/doc/quantdatamanager/quant-data-manager-command-line-interface-help/
    
    Examples
    --------
    >>> process = start_sqcli_process(
    ...     "C:/Program Files/StrategyQuant/sqcli.exe",
    ...     "EURUSD",
    ...     "forex",
    ...     "GMT",
    ...     "C:/data/eurusd_data.csv"
    ... )
    """
    command: List[str] = [
        path_sqcli_exe,
        "-data",
        "action=import",
        f"symbol={symbol}",
        f"instrument={instrument}",
        f"filepath={filepath}",
        "errorhandling=ignore",
        f"timezone={timezone}"
    ]
    
    # Add any additional arguments if provided
    if additional_args:
        command.extend(additional_args)
        
    process: subprocess.Popen = subprocess.Popen(command)
    return process
