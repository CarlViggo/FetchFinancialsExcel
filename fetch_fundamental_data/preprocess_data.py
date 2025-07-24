from concurrent.futures import ThreadPoolExecutor
import data_analysis as analyse 
import company_data_extraction_EODH as eodh
import pandas as pd
import os 
from datetime import datetime

# =============== Globals ===============
now = datetime.today()
CURRENT_DATE = now.strftime("%Y-%m-%d")
# =======================================

# wrapper for the data fetching functions
def wrapper(company_ticker):
	
	# tillkalla fetch-funktionen 
	data = eodh.fetch_fundamentals(company_ticker)
	price_data = eodh.fetch_price_data(company_ticker)

	price = general = roce = pe = revenue = buybacks = ma = eps = total_yield = gross_p = accrual = asset_g = insiders = fcf = cop_at = {}
	
	# hämta dictionaries
	try: 
		# behöver två argument 
		price = eodh.real_time_price(company_ticker, data)
		print(f"Bakgrund hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av general: {e}")

	try: 
		general = eodh.get_selected_highlights(data)
		print(f"highlights hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av general: {e}")

	try: 
		roce = eodh.calculate_roce(data)
		print(f"highlights hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av roce: {e}")

	try: 
		pe = eodh.calculate_five_year_average_pe(company_ticker, data, price_data)
		print(f"pe hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av pe: {e}")

	try: 
		revenue = eodh.get_revenue_growth_data(data)
		print(f"revenue hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av revenue: {e}")
	
	try: 
		eps = eodh.get_eps_growth_full(data)
		print(f"eps hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av eps: {e}")
	
	try: 
		fcf = eodh.fcf_yield_growth_latest(data)
		print(f"fcf hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av fcf: {e}")
	
	try: 
		buybacks = eodh.buyback_change_latest(data)
		print(f"Moving Averages hämtade för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av ma: {e}")
	
	try: 
		insiders = eodh.get_percent_insiders(data)
		print(f"insiders hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av insiders: {e}")

	try: 
		ma = eodh.get_moving_averages(data)
		print(f"ma hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av ma: {e}")

	try: 
		gross_p = eodh.gross_profitability(data)
		print(f"Bruttolönsamhet hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av Bruttolönsamhet: {e}")
	
	try: 
		accrual = eodh.accruals(data)
		print(f"accruals hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av accruals: {e}")

	try: 
		asset_g = eodh.asset_growth(data)
		print(f"Asset Growth hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av Asset Growth: {e}")

	try: 
		total_yield = eodh.total_yield(data)
		print(f"Total Yield hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av Total Yield: {e}")

	try: 
		cop_at = eodh.compute_cop_at(data)
		print(f"cop_at hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av cop_at: {e}")

	# hämta komponenter för senare beräkning
	try: 
		conservative_comps = analyse.conservative(data, price_data)
		#print(f"Conservative hämtad för {company_ticker}.")
	except Exception as e:
		print(f"Ett fel uppstod vid hämtning av Conservative: {e}")

	combined = {**price, **general, **roce, **pe, **revenue, **eps, **fcf, **buybacks, **insiders, **ma, **gross_p, **accrual, **asset_g, **total_yield, **cop_at}
	other = {**conservative_comps}
	return combined, other

# calls wrapper and inserts a row with companydata into dataframe
def add_company_data(data_df, company_name, company_ticker):
    company_data = {
        'Bolag': company_name,
        'Ticker': company_ticker
    }

    company_data_separate = {
        'Ticker': company_ticker
    }

    indicators, other = wrapper(company_ticker)

    if indicators is not None:
        company_data.update(indicators)
        company_data_separate.update(other)
    else:
        print(f"Ingen data hittades för {company_ticker}, lägger till tom rad.")

    try:
        data_df = pd.concat([data_df, pd.DataFrame([company_data])], ignore_index=True)
    except Exception as e:
        print("Fel vid inläggning i DataFrame, lägger in tom rad istället.")
        data_df = pd.concat([data_df, pd.DataFrame([{'Ticker': company_ticker, 'Bolag': company_name}])], ignore_index=True)

    return data_df, company_data_separate

# concurrently calls add company data for each ticker in the list
def combine_datapoints(company_list, ticker_list, max_workers=10):
    data_df = pd.DataFrame()
    separate_data_list = []

    # Kombinera företagsnamn och ticker i en lista av tupler
    combined = list(zip(company_list, ticker_list))

    def process_company(args):
        company, ticker = args
        return add_company_data(pd.DataFrame(), company, ticker)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_company, combined))

    for df, separate_data in results:
        data_df = pd.concat([data_df, df], ignore_index=True)
        separate_data_list.append(separate_data)

    return data_df, separate_data_list

# extracts ticker list from excelfile (tracked portfolios) 
def extract_tickers_from_excel(file_path):
    df = pd.read_excel(file_path, header=None)
    tickers = []
    company_list = []
    for index, row in df.iterrows():
        if index < 1 or pd.isna(row[1]):
            continue
        company = str(row[0]).strip().upper()
        ticker = str(row[1]).strip().upper()
        ticker = ''.join(c for c in ticker if c.isalpha() or c.isdigit() or c == '.' or c == '-')
        # Ta bort eventuella punkter och bindestreck i början eller slutet
        ticker = ticker.strip('.-')
        
        if ticker:
            tickers.append(ticker)
		
        if company:
            company_list.append(company)
    return company_list, tickers

# function for updating existing dataframe with data
def update_existing_data(df, bolag_list, ticker_list, max_workers=10):
    existing_tickers = set(df['Ticker'].astype(str))
    ticker_list_set = set(ticker_list)
    tickers_to_remove = existing_tickers - ticker_list_set
    df = df[~df['Ticker'].isin(tickers_to_remove)]

    separate_data_list = []

    combined = list(zip(bolag_list, ticker_list))

    def fetch_and_merge(args):
        bolag, ticker = args
        print(f"Uppdaterar data för: {bolag} ({ticker})")
        try:
            updated_data, other = wrapper(ticker)
            company_data_separate = {'Ticker': ticker, 'Bolag': bolag}
            if updated_data:
                company_data_separate.update(other)
            return bolag, ticker, updated_data, company_data_separate
        except Exception as e:
            print(f"Misslyckades att uppdatera {bolag} ({ticker}): {e}")
            return bolag, ticker, None, {'Ticker': ticker, 'Bolag': bolag}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(fetch_and_merge, combined))

    for bolag, ticker, updated_data, separate_data in results:
        separate_data_list.append(separate_data)

        if updated_data is None:
            continue

        for key in updated_data:
            if key not in df.columns:
                df[key] = None

        if ticker in df['Ticker'].values:
            i = df.index[df['Ticker'] == ticker][0]
            # Uppdatera både Bolag och andra fält om det behövs
            df.at[i, 'Bolag'] = bolag
            for key, value in updated_data.items():
                df.at[i, key] = value
        else:
            new_row = {col: None for col in df.columns}
            new_row['Ticker'] = ticker
            new_row['Bolag'] = bolag
            for key, value in updated_data.items():
                if key not in new_row:
                    df[key] = None
                new_row[key] = value
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df, separate_data_list


def main():
    while True:
        try:
            filenames_input = input("Enter output filenames, e.g.: file1.xlsx, file2.xlsx : ")
            filenames = [f.strip() for f in filenames_input.split(',')]
            
            portfolio_names_input = input("Enter portfolio filenames e.g.: portfolio1.xlsx, portfolio2.xlsx : ")
            portfolio_names = [f.strip() for f in portfolio_names_input.split(',')]
            
            if len(filenames) != len(portfolio_names):
                print("Error: The number of filenames and portfolio names must be the same.")
                continue

            break
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")

    N = len(filenames)

    mode = input("[U]ppdatera befintlig fil eller [N]y fil för ALLA portföljer? ").strip().lower()

    for idx in range(N):
        filepath = f'{DRIVE_PATH}/updated_fundamentals/{filenames[idx]}'
        portfolio_path = f"{DRIVE_PATH}/tracked_portfolios/{portfolio_names[idx]}"
        
        company_list, ticker_list = extract_tickers_from_excel(portfolio_path)

        # uppdatera
        if mode == 'u':
            print(f"Uppdaterar fil: {filepath}")
            if not os.path.exists(filepath):
                print(f"Filen '{filepath}' hittades inte. Skapar ny fil istället.")
                # Option to create new if not found, or skip
                # You might want to handle this more robustly based on your needs
                new_df, separate_data_list = combine_datapoints(company_list, ticker_list)
                df_analysed = analyse.greenblatt_formula(new_df)
                df_analysed = analyse.conservative_formula(df_analysed, separate_data_list)
                df_analysed = analyse.quality_score(df_analysed)
                df_analysed["Senast uppdaterad"] = CURRENT_DATE
                df_analysed.to_excel(filepath, index=False, engine='openpyxl')
                print(f"Ny fil skapad (eftersom original inte hittades): {filepath}")
                continue # Skip to next portfolio

            df = pd.read_excel(filepath, engine="openpyxl")
            updated_df, separate_data_list = update_existing_data(df, company_list, ticker_list)

            # data Analysis part
            df_analysed = analyse.greenblatt_formula(updated_df)
            df_analysed = analyse.conservative_formula(df_analysed, separate_data_list)
            df_analysed = analyse.quality_score(df_analysed)
            df_analysed["Senast uppdaterad"] = CURRENT_DATE

            df_analysed.to_excel(filepath, index=False, engine='openpyxl')
            print(f"Filen uppdaterad: {filepath}")

        # skapa ny fil
        elif mode == 'n':
            print(f"Skapar ny fil: {filepath}")
            new_df, separate_data_list = combine_datapoints(company_list, ticker_list)
            
            # data Analysis part
            df_analysed = analyse.greenblatt_formula(new_df)
            df_analysed = analyse.conservative_formula(df_analysed, separate_data_list)
            df_analysed = analyse.quality_score(df_analysed)
            df_analysed["Senast uppdaterad"] = CURRENT_DATE

            df_analysed.to_excel(filepath, index=False, engine='openpyxl')
            print(f"Ny fil skapad: {filepath}")

        else:
            print("Ogiltigt val för alla portföljer. Avbryter.")
            break # Exit the loop if invalid choice for all
    print("Alla portföljer har bearbetats.")

if __name__ == "__main__":
    main()

#filename = "Buyback_ETF.xlsx"
#filenames = ["Handelsbanken_Index.xlsx", "NASDAQ_composite.xlsx", "NASDAQ_EUROPE_Index.xlsx"]
#filenames = ["DNB_Norden_ETF.xlsx"]
#portfolio_name = "BUYBACK_ETF.xlsx"

#portfolio_names = ["Index/HANDELSBANKEN_SVERIGE_INDEX.xlsx", "Index/NASDAQ_composite.xlsx","Index/NASDAQ_EUROPE.xlsx"]
#portfolio_names = ["ETF/DNB_NORDEN_ETF.xlsx"]

#filenames = Global_Stars_Portfölj.xlsx, UG_Portfölj.xlsx, Nordisk_Kvalitet_Portfölj.xlsx
#portfolio_names = GLOBAL_STARS.xlsx, UG.xlsx, NORDISK_KVALITET.xlsx
