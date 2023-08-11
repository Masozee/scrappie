import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime

def scrape_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def main():
    date_taken = datetime.now().strftime("%Y%m%d_%H%M%S")  # Get the current date and time
    stocks_url = "https://www.pasardana.id/api/Stock/GetAllSimpleStocks?username=anonymous"
    profile_output_filename = f"Profile_{date_taken}.csv"
    directors_output_filename = f"Directors_{date_taken}.csv"
    secretaries_output_filename = f"Secretaries_{date_taken}.csv"
    stockholders_output_filename = f"StockHolders_{date_taken}.csv"
    commisioner_output_filename = f"Commisioners_{date_taken}.csv"
    companychild_output_filename = f"CompanyChild_{date_taken}.csv"
    finstatement_output_filename = f"Financial_Statement_{date_taken}.csv"

    # Fetch data to get the list of stocks
    data = scrape_data(stocks_url)
    if data:
        # Use tqdm to show progress
        with tqdm(total=len(data), desc="Fetching and processing data", unit="stock") as pbar:
            with open(profile_output_filename, 'w', encoding='utf-8') as profile_output_file, \
                 open(directors_output_filename, 'w', encoding='utf-8') as directors_output_file, \
                 open(secretaries_output_filename, 'w', encoding='utf-8') as secretaries_output_file, \
                 open(stockholders_output_filename, 'w', encoding='utf-8') as stockholders_output_file, \
                 open(commisioner_output_filename, 'w', encoding='utf-8') as commisioner_output_file, \
                 open(companychild_output_filename, 'w', encoding='utf-8') as companychild_output_file, \
                 open(finstatement_output_filename, 'w', encoding='utf-8') as finstatement_output_file :


                for stock in data:
                    if "Code" in stock:
                        code = stock["Code"]

                        url_with_code = f"https://www.pasardana.id/api/Stock/GetByCode?code={code}&username=anonymous"
                        profile_url = f"https://www.pasardana.id/api/StockProfile/GetProfileByCode?code={code}"

                        data = scrape_data(url_with_code)
                        if data:
                            extracted_data = {
                                "Id": data.get("Id"),
                                "Code": data.get("Code"),
                                "Name": data.get("Name"),
                                "NewSectorName": data.get("NewSectorName"),
                                "NewSubSectorName": data.get("NewSubSectorName"),
                                "NewIndustryName": data.get("NewIndustryName"),
                                "NewSubIndustryName": data.get("NewSubIndustryName"),
                                "SectorName": data.get("SectorName"),
                                "SubSectorName": data.get("SubSectorName"),
                                "BoardRecording": data.get("BoardRecording"),
                                "HeadOffice": data.get("HeadOffice"),
                                "Phone": data.get("Phone"),
                                "RepresentativeName": data.get("RepresentativeName"),
                                "WebsiteUrl": data.get("WebsiteUrl"),
                                "Address": data.get("Address"),
                                "TotalEmployees": data.get("TotalEmployees"),
                                "ExchangeAdministration": data.get("ExchangeAdministration"),
                                "Npwp": data.get("Npwp"),
                                "Npkp": data.get("Npkp"),
                                "IsActive": data.get("IsActive"),
                                "ListingDate": data.get("ListingDate"),
                                "AnnualDividend": data.get("AnnualDividend"),
                                "GeneralInformation": data.get("GeneralInformation"),
                                "Fax": data.get("Fax"),
                                "FoundingDate": data.get("FoundingDate"),
                                "CompanyEmail": data.get("CompanyEmail")
                            }

                            df = pd.DataFrame([extracted_data])
                            if not profile_output_file.tell():  # Write header only once
                                df.to_csv(profile_output_file, index=False)
                            else:
                                df.to_csv(profile_output_file, index=False, header=False)

                        profile_data = scrape_data(profile_url)
                        if profile_data:
                            if "Directors" in profile_data:
                                directors_df = pd.DataFrame(profile_data["Directors"])
                                directors_df["IdField"] = data["Id"]  # Adding IdField based on Id from url_with_code
                                if not directors_output_file.tell():  # Write header only once
                                    directors_df.to_csv(directors_output_file, index=False)
                                else:
                                    directors_df.to_csv(directors_output_file, index=False, header=False)

                            if "Secretaries" in profile_data:
                                secretaries_df = pd.DataFrame(profile_data["Secretaries"])
                                secretaries_df["IdField"] = data["Id"]  # Adding IdField based on Id from url_with_code
                                if not secretaries_output_file.tell():  # Write header only once
                                    secretaries_df.to_csv(secretaries_output_file, index=False)
                                else:
                                    secretaries_df.to_csv(secretaries_output_file, index=False, header=False)

                            if "StockHolders" in profile_data:
                                stockholders_df = pd.DataFrame(profile_data["StockHolders"])
                                stockholders_df["IdField"] = data["Id"]  # Adding IdField based on Id from url_with_code
                                if not stockholders_output_file.tell():  # Write header only once
                                    stockholders_df.to_csv(stockholders_output_file, index=False)
                                else:
                                    stockholders_df.to_csv(stockholders_output_file, index=False, header=False)

                            if "Commisioners" in profile_data:
                                commisioner_df = pd.DataFrame(profile_data["Commisioners"])
                                commisioner_df["IdField"] = data["Id"]  # Adding IdField based on Id from url_with_code
                                if not commisioner_output_file.tell():  # Write header only once
                                    commisioner_df.to_csv(commisioner_output_file, index=False)
                                else:
                                    commisioner_df.to_csv(commisioner_output_file, index=False, header=False)

                            if "CompanyChilds" in profile_data:
                                companychild_df = pd.DataFrame(profile_data["CompanyChilds"])
                                companychild_df["IdField"] = data["Id"]  # Adding IdField based on Id from url_with_code
                                if not companychild_output_file.tell():  # Write header only once
                                    companychild_df.to_csv(companychild_output_file, index=False)
                                else:
                                    companychild_df.to_csv(companychild_output_file, index=False, header=False)

                            if "Financialstatement" in profile_data:
                                financial_statement_data = profile_data["Financialstatement"]
                                if isinstance(financial_statement_data, dict):
                                    financial_statement_data = [financial_statement_data]

                                finstatement_df = pd.DataFrame(financial_statement_data)
                                finstatement_df["IdField"] = data["Id"]  # Adding IdField based on Id from url_with_code
                                if not finstatement_output_file.tell():  # Write header only once
                                    finstatement_df.to_csv(finstatement_output_file, index=False)
                                else:
                                    finstatement_df.to_csv(finstatement_output_file, index=False, header=False)

                    pbar.update(1)  # Increment the progress bar

        print(f"All data saved to {profile_output_filename}")
        print(f"Directors data saved to {directors_output_filename}")
        print(f"Secretaries data saved to {secretaries_output_filename}")
        print(f"StockHolders data saved to {stockholders_output_filename}")
        print(f"Commisioner data saved to {commisioner_output_filename}")
        print(f"Company Childs data saved to {companychild_output_filename}")
        print(f"Financial Statement data saved to {finstatement_output_filename}")

if __name__ == "__main__":
    main()
