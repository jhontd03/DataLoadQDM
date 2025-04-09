import os
import yaml
import json
from typing import Dict, Any, List, Tuple
from datetime import datetime


def load_init_file(symbol: str, **kwargs: Any) -> None:
    """
    Load and modify an initialization file template by replacing placeholder values.
    
    Parameters
    ----------
    symbol : str
        Trading symbol to replace the placeholder in the template.
    **kwargs : dict
        Keyword arguments containing configuration parameters:
        
        - path_template_ea_ini : str
            Path to the template initialization file.
        - path_config_ini : str
            Path where the modified initialization file will be saved.
        - name_expert : str
            Name of the expert advisor.
        - Login : str
            Login credential.
        - Password : str
            Password credential.
        - timeframe : str
            Time frame for the data.
        - init_date : str
            Start date for the data in 'YYYY-MM-DD' format.
        - end_date : str
            End date for the data in 'YYYY-MM-DD' format. If empty, current date is used.
        - mode_load_data : str
            Key to select the data loading mode from selector_load_data.
        - selector_load_data : dict
            Dictionary containing configuration for different data loading modes.
    
    Returns
    -------
    None
        The function writes the modified file to the path specified in kwargs['path_config_ini'].
    
    Notes
    -----
    The function replaces placeholders in the template file with actual values.
    If end_date is not provided, the current date is used.
    
    Examples
    --------
    >>> load_init_file('EURUSD', 
    ...               path_template_ea_ini='templates/ea_template.ini',
    ...               path_config_ini='config/my_ea.ini',
    ...               name_expert='MyExpert',
    ...               Login='12345',
    ...               Password='secret',
    ...               timeframe='H1',
    ...               init_date='2023-01-01',
    ...               end_date='',
    ...               mode_load_data='default',
    ...               selector_load_data={'default': {'Model': 1}})
    """
    with open(kwargs['path_template_ea_ini'], "r") as archivo:
        lineas = archivo.readlines()
    
    # Replace placeholders with actual values
    replacements = {
        "# name_expert": kwargs['name_expert'],
        "# symbol": symbol,
        "# Login": kwargs['Login'],
        "# Password": kwargs['Password'],
        "# expert_path": kwargs['name_expert'],
        "# time_frame": kwargs['timeframe'],
        "# init_date": kwargs['init_date'],
        "# end_date": kwargs['end_date'],
        "# Model": str(kwargs['selector_load_data'][kwargs['mode_load_data']]['Model'])
    }
    
    for i, linea in enumerate(lineas):
        for placeholder, value in replacements.items():
            if placeholder in linea:
                lineas[i] = lineas[i].replace(placeholder, value)
    
    # Write the modified content to the output file
    with open(kwargs['path_config_ini'], "w") as file_export:
        file_export.writelines(lineas)


def load_yaml(file_path: str) -> Dict[str, Any]:
    """
    Load a YAML file and return its contents as a dictionary.
    
    Parameters
    ----------
    file_path : str
        Path to the YAML file to be loaded.
    
    Returns
    -------
    Dict[str, Any]
        Dictionary containing the parsed YAML data.
    
    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    yaml.YAMLError
        If the YAML file has invalid syntax.
    
    Examples
    --------
    >>> config = load_yaml('config/settings.yaml')
    >>> print(config['server']['host'])
    'localhost'
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def drop_csv_files(kwargs: Dict[str, str]) -> Tuple[int, List[str]]:
    """
    Delete all CSV files in a specified directory.
    
    Parameters
    ----------
    kwargs : Dict[str, str]
        Dictionary containing configuration parameters:
        
        - path_export_data_csv : str
            Path to the directory containing CSV files to be deleted.
    
    Returns
    -------
    Tuple[int, List[str]]
        A tuple containing the count of deleted files and a list of the deleted filenames
    
    Notes
    -----
    This function permanently deletes files and should be used with caution.
    
    Examples
    --------
    >>> deleted_count, deleted_files = drop_csv_files({'path_export_data_csv': 'data/exports'})
    >>> print(f"Deleted {deleted_count} files: {', '.join(deleted_files)}")
    """
    csv_file_list: List[str] = os.listdir(kwargs['path_export_data_csv'])
    deleted_files = []
    
    for csv_file in csv_file_list:
        if csv_file.endswith(".csv"):
            full_path = os.path.join(kwargs['path_export_data_csv'], csv_file)
            try:
                os.remove(full_path)
                deleted_files.append(csv_file)
            except Exception as e:
                # If deletion fails, don't add to deleted_files list
                pass
                
    return len(deleted_files), deleted_files


def load_symbol_log(log_file_path: str = 'logs/symbol_status.json') -> Dict[str, str]:
    """
    Load the symbol status log file containing the last processed date for each symbol.
    
    Parameters
    ----------
    log_file_path : str, optional
        Path to the symbol status log file, by default 'logs/symbol_status.json'
    
    Returns
    -------
    Dict[str, str]
        Dictionary with symbol names as keys and their last processed dates as values.
        Returns an empty dictionary if the file doesn't exist or has invalid content.
    
    Examples
    --------
    >>> symbol_log = load_symbol_log()
    >>> print(symbol_log['EURUSD'])
    '2023-05-01'
    """
    try:
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as file:
                return json.load(file)
        return {}
    except (json.JSONDecodeError, IOError):
        # Return empty dict if file doesn't exist or is corrupted
        return {}


def update_symbol_log(symbol: str, end_date: str, log_file_path: str = 'logs/symbol_status.json') -> None:
    """
    Update the symbol status log with the latest processed date for a symbol.
    
    Parameters
    ----------
    symbol : str
        The symbol name to update.
    end_date : str
        The date string representing when the symbol was last processed.
    log_file_path : str, optional
        Path to the symbol status log file, by default 'logs/symbol_status.json'
    
    Returns
    -------
    None
        Updates the log file with the new end date for the specified symbol.
    
    Examples
    --------
    >>> update_symbol_log('EURUSD', '2023-05-15')
    """
    # Load existing log data
    symbol_log = load_symbol_log(log_file_path)
    
    # Update with new information
    symbol_log[symbol] = end_date
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    
    # Save updated log
    with open(log_file_path, 'w') as file:
        json.dump(symbol_log, file, indent=4)
