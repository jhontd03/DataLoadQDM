import os
from dotenv import load_dotenv
from config_files import load_yaml, load_init_file, drop_csv_files, load_symbol_log, update_symbol_log
from run_process import start_mt_process, start_sqcli_process
from logger import Logger
from tqdm import tqdm
from datetime import datetime

if __name__ == "__main__":
    
    load_dotenv()   

    kwargs = load_yaml('config.yaml')   

    kwargs['Login'] = os.getenv("Login")
    kwargs['Password'] = os.getenv("Password")   

    list_symbols = kwargs['list_symbols']
    
    logger = Logger(name="ProcessLogger", log_file="logs/process.log")  # Specify a valid log file path
    
    # Load the symbol processing status log
    symbol_log = load_symbol_log()
    logger.info(f"Loaded symbol status log with {len(symbol_log)} entries")
    
    # Get current date for comparison
    current_date = datetime.now().strftime('%Y-%m-%d')
    logger.info(f"Current date is {current_date}")
    
    for symbol_dict in tqdm(list_symbols, desc="Processing Symbols"):  # Wrap the loop with tqdm
        
        symbol_qdm = list(symbol_dict.keys())[0]
        symbol_mt5 = symbol_dict[symbol_qdm]['symbol_mt5']
        
        # Check if we have a previous processing record for this symbol
        # Set end_date to current date if not provided
        if kwargs['end_date'] == '':
            kwargs['end_date'] = datetime.now().strftime('%Y-%m-%d')        
        original_end_date = kwargs['end_date']

        if symbol_qdm in symbol_log:
            last_processed_date = symbol_log[symbol_qdm]
            logger.info(f"Symbol {symbol_qdm} was last processed until {last_processed_date}")
            
            # Check if symbol was already processed today
            if last_processed_date == current_date:
                logger.info(f"Symbol {symbol_qdm} was already processed today. Skipping.")
                continue
            
            # Update the end_date to current date and init_date to last processed date
            kwargs['init_date'] = last_processed_date
            kwargs['end_date'] = current_date
            
            logger.info(f"Setting date range for {symbol_qdm} from {kwargs['init_date']} to {kwargs['end_date']}")
        else:
            logger.info(f"No previous processing record for {symbol_qdm}, using default date range")
                       
        kwargs['mode_load_data'] = symbol_dict[symbol_qdm]['timeframe']               
        kwargs['name_expert'] = kwargs['selector_load_data'][kwargs['mode_load_data']]['file']
        
        load_init_file(symbol_mt5, **kwargs)
        process_mt = start_mt_process(kwargs['path_metatrader_exe'], kwargs['path_config_ini'])
        exit_code = process_mt.wait() 

        csv_file_path = os.path.join(kwargs['path_export_data_csv'], f'{symbol_mt5}_Data.csv')

        if not exit_code:
            logger.info(f'Write data to csv file from metatrader complete for {symbol_qdm}')  # Log success message
            
            # Check if CSV file exists before proceeding
            if not os.path.exists(csv_file_path):
                logger.error(f'CSV file for {symbol_qdm} not found at {csv_file_path}')
                # Continue to the next symbol without running SQCLI process
                # Reset the original end date for the next symbol
                kwargs['end_date'] = original_end_date
                continue                
        else:
            logger.error(f'Failed to write data to csv file from metatrader for {symbol_qdm}')  # Log error message
            # Skip to the next symbol if MetaTrader process failed
            # Reset the original end date for the next symbol
            kwargs['end_date'] = original_end_date
            continue

        process_sqcli = start_sqcli_process(
            path_sqcli_exe=kwargs['path_sqcli_exe'],
            symbol=f"{symbol_qdm}{kwargs['postfix_symbol_sqx']}",
            instrument=f"{symbol_mt5}{kwargs['postfix_instrument_sqx']}",
            timezone=kwargs['timezone'],
            filepath=csv_file_path,
        )
        exit_code = process_sqcli.wait() 

        if not exit_code:
            # Update the symbol log with the current end date
            current_end_date = kwargs['end_date']
            update_symbol_log(symbol_qdm, current_end_date)
            logger.info(f'Updated symbol log for {symbol_qdm} with end date {current_end_date}')
            logger.info(f'Import data to Quant Data Manager complete for {symbol_qdm}')  # Log success message
        else:
            logger.error(f'Failed import data to Quant Data Manager for {symbol_qdm}')  # Log error message
            
        logger.info(f'Cleaning up temporary CSV files for {symbol_qdm}')
        deleted_count, deleted_files = drop_csv_files(kwargs)
        if deleted_count > 0:
            logger.info(f'CSV cleanup complete: Deleted {deleted_count} files for {symbol_qdm}')
            if deleted_count <= 5:  # Only log individual files if there aren't too many
                logger.debug(f'Deleted files: {", ".join(deleted_files)}')
        else:
            logger.warning(f'No CSV files found to delete for {symbol_qdm}')
        
        # Reset the original end date for the next symbol
        kwargs['end_date'] = original_end_date
    
    logger.info("Data loading process completed for all symbols")
