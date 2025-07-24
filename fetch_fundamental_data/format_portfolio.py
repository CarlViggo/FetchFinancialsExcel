import pandas as pd

# DRIVE_PATH removed - paths should be provided as arguments

def format_portfolio(template_name, infront_fil_name, formatted_name): 
    print(template_name)
    # Ange sökvägar till dina filer här:
    path_file1 = f"{DRIVE_PATH}/other/{template_name}"  # Fil med kolumner MIC, Börsnamn, Land, EODHD-suffix
    path_file2 = f"{DRIVE_PATH}/unformated_portfolios/{infront_fil_name}" # Fil med kolumner Beskrivning, Symbol, MIC
    path_file3 = f"{DRIVE_PATH}/tracked_portfolios/{formatted_name}" # Fil där färdigdormatterad portfoliop sparas 
    
    print(path_file1)
    print(path_file2)
    print(path_file3)

    # Läs in filerna
    df_suffix = pd.read_excel(path_file1)
    df_symbols = pd.read_excel(path_file2)

    #  ersätt mellanslag med '-' och ta bort '*'
    df_symbols['Symbol'] = df_symbols['Symbol'].astype(str).str.replace(' ', '-').str.replace('*', '')

    # s ihop med suffix baserat på MIC
    df_merged = df_symbols.merge(df_suffix[['MIC', 'EODHD-suffix']], on='MIC', how='left')

    #  ny kolumn med ticker + '.' + suffix
    df_merged['EODHD_Ticker'] = df_merged['Symbol'] + '.' + df_merged['EODHD-suffix']

    # Behåll bara 'Beskrivning' och 'EODHD_Ticker', byt namn på kolumner
    df_final = df_merged[['Beskrivning', 'EODHD_Ticker']].copy()
    df_final.rename(columns={'Beskrivning': 'Bolag', 'EODHD_Ticker': 'Ticker'}, inplace=True)

    # spara till ny Excel-fil
    df_final.to_excel(path_file3, index=False)

    print(f"Portfolio formatterad Resultatet sparat till: {path_file3}")

if __name__ == "__main__": 
    template_name = "mic_to_eodhd_suffix.xlsx"
    infront_fil_name = "NASDAQ_Global.xlsx"
    formatted_name = "NASDAQ_Global.xlsx"
    format_portfolio(template_name, infront_fil_name, formatted_name)
