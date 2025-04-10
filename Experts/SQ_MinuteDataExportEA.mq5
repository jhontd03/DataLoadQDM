//+-----------------------------------------------------------------------------------+
//|                                                         SQ_MinuteDataExportEA.mq5 |
//|                                                                                   |
//|                                          EA to export minute data from MetaTrader |
//|                                             Minute data are exported to directory |
//| {MetaQuotes folder}/Tester/{Data folder}/AgentXY/MQL5/Files/{Symbol}_Data.csv |
//+-----------------------------------------------------------------------------------+

#property copyright "Copyright © 2016 StrategyQuant"
#property link      "http://www.StrategyQuant.com"

int previousVolume = 0;
int handle;

int OnInit() {
   string fileName;
   StringConcatenate(fileName, Symbol(), "_Data.csv");
   
   handle = FileOpen(fileName, FILE_ANSI | FILE_WRITE, "\t", CP_UTF8);
   if(handle>0) {
      FileWrite(handle,"Date", "Time","Open","High","Low","Close","TickVol","Vol","Spread");
   }
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+

void OnTick() {
  
    double	open = iOpen(_Symbol,PERIOD_M1,1);
    double	high = iHigh(_Symbol,PERIOD_M1,1);
    double	low = iLow(_Symbol,PERIOD_M1,1);
    double	close = iClose(_Symbol,PERIOD_M1,1);
    long	tickvolume = iTickVolume(_Symbol,PERIOD_M1,1);
    long	volume = iVolume(_Symbol,PERIOD_M1,1);    
    int     spread = (int)SymbolInfoInteger(_Symbol,SYMBOL_SPREAD);  

    if(handle>0) {
      FileWrite(handle,
      TimeToString(TimeCurrent(), TIME_DATE),
      TimeToString(TimeCurrent(), TIME_SECONDS),
      open,
      high,
      low,
      close,      
      tickvolume,
      volume,
      spread);
    }

}

void OnDeinit(const int reason) {
    FileClose(handle);
}