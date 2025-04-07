import os
from dotenv import load_dotenv
from config_files import load_yaml, load_init_file, drop_csv_files
from run_process import start_mt_process, start_sqcli_process
from logger import Logger
from tqdm import tqdm

if __name__ == "__main__":
    
    load_dotenv()   

    kwargs = load_yaml('config.yaml')   

    kwargs['Login'] = os.getenv("Login")
    kwargs['Password'] = os.getenv("Password")   

    list_symbols = kwargs['list_symbols']
    kwargs['name_expert'] = kwargs['selector_load_data'][kwargs['mode_load_data']]['file']

    logger = Logger(name="ProcessLogger", log_file="logs/process.log")  # Specify a valid log file path
    
    for symbol in tqdm(list_symbols, desc="Processing Symbols"):  # Wrap the loop with tqdm
    
        symbol_mt5 = list(symbol.keys())[0]
        symbol_qdm = symbol[symbol_mt5]
        
        load_init_file(symbol_mt5, **kwargs)
        process_mt = start_mt_process(kwargs['path_metatrader_exe'], kwargs['path_config_ini'])
        exit_code = process_mt.wait() 
        
        if not exit_code:
            logger.info('Write data to csv from metatrader')  # Log success message
        else:
            logger.error('Failed to write data to csv from metatrader')  # Log error message

        csv_file_path = os.path.join(kwargs['path_export_data_csv'], f'{symbol_mt5}_Data.csv')

        process_sqcli = start_sqcli_process(
            path_sqcli_exe=kwargs['path_sqcli_exe'],
            symbol=f"{symbol_qdm}{kwargs['postfix_symbol_sqx']}",
            instrument=f"{symbol_qdm}{kwargs['postfix_instrument_sqx']}",
            timezone=kwargs['timezone'],
            filepath=csv_file_path,
        )
        exit_code = process_sqcli.wait() 

        if not exit_code:
            logger.info('Import data to Quant Data Manager')  # Log success message
        else:
            logger.error('Failed to import data to Quant Data Manager')  # Log error message
            
        drop_csv_files(kwargs)
