import requests
from datetime import datetime
from tqdm import tqdm
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append("..")

from connections import Session
from models import Profile, Directors, StockHolders  # Import your defined models


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

def update_or_create(session, model, filters, new_data):
    entry = session.query(model).filter_by(**filters).first()

    if entry:
        is_data_changed = any(getattr(entry, key) != new_data[key] for key in new_data)
        if is_data_changed:
            for key, value in new_data.items():
                setattr(entry, key, value)
            session.commit()
    else:
        new_entry = model(**new_data)
        session.add(new_entry)
        session.commit()

def main():
    date_taken = datetime.now().strftime("%Y%m%d_%H%M%S")  # Get the current date and time
    stocks_url = "https://www.pasardana.id/api/Stock/GetAllSimpleStocks?username=anonymous"

    session = Session()

    # Fetch data to get the list of stocks
    data = scrape_data(stocks_url)
    if data:
        # Use tqdm to show progress
        with tqdm(total=len(data), desc="Fetching and processing data", unit="stock") as pbar:

            for stock in data:
                if "Code" in stock:
                    code = stock["Code"]

                    url_with_code = f"https://www.pasardana.id/api/Stock/GetByCode?code={code}&username=anonymous"
                    profile_url = f"https://www.pasardana.id/api/StockProfile/GetProfileByCode?code={code}"

                    data = scrape_data(url_with_code)
                    if data:
                        extracted_data = {
                            "code": data.get("Code"),
                            "name": data.get("Name"),
                            "new_sector_name": data.get("NewSectorName"),
                            "new_sub_sector_name": data.get("NewSubSectorName"),
                            "new_industry_name": data.get("NewIndustryName"),
                            "new_sub_industry_name": data.get("NewSubIndustryName"),
                            "sector_name": data.get("SectorName"),
                            "sub_sector_name": data.get("SubSectorName"),
                            "board_recording": data.get("BoardRecording"),
                            "head_office": data.get("HeadOffice"),
                            "phone": data.get("Phone"),
                            "representative_name": data.get("RepresentativeName"),
                            "website_url": data.get("WebsiteUrl"),
                            "address": data.get("Address"),
                            "total_employees": data.get("TotalEmployees"),
                            "exchange_administration": data.get("ExchangeAdministration"),
                            "npwp": data.get("Npwp"),
                            "npkp": data.get("Npkp"),
                            "is_active": data.get("IsActive"),
                            "listing_date": data.get("ListingDate"),
                            "annual_dividend": data.get("AnnualDividend"),
                            "general_information": data.get("GeneralInformation"),
                            "fax": data.get("Fax"),
                            "founding_date": data.get("FoundingDate"),
                            "company_email": data.get("CompanyEmail")
                        }

                        update_or_create(session, Profile, {"code": extracted_data["code"]}, extracted_data)

                        profile_data = scrape_data(profile_url)
                        if profile_data:
                            directors_data = profile_data.get("Directors")
                            if directors_data:
                                for director in directors_data:
                                    director_data = {
                                        "fk_profile_id": director.get("Id"),  # Use "Id" instead of ["Id"]
                                        "name": director.get("Name"),
                                        "role": director.get("Role"),
                                        "affiliated": True if director.get("Affiliated") == "Ya" else False,
                                        "id_field": extracted_data["code"],
                                        # ... (other fields)
                                    }
                                    update_or_create(session, Directors, {"name": director_data["name"]}, director_data)

                            stockholders_data = profile_data.get("StockHolders")
                            if stockholders_data:
                                for stockholder in stockholders_data:
                                    amount_str = stockholder.get("Amount")
                                    if amount_str and '.' in amount_str:  # Check if Amount is not empty and contains dots
                                        amount_float = float(amount_str.replace('.', ''))
                                    else:
                                        amount_float = None  # Handle empty or non-convertible cases

                                    percentage_str = stockholder.get("Percentage")
                                    if percentage_str and '.' in percentage_str:  # Check if Percentage is not empty and contains dots
                                        percentage_float = float(percentage_str.replace('.', ''))
                                    else:
                                        percentage_float = None  # Handle empty or non-convertible cases

                                    stockholder_data = {
                                        "fk_profile_id": stockholder.get("Id"),  # Use "Code" instead of "id"
                                        "name": stockholder.get("Name"),
                                        "holding_type": stockholder.get("HoldingType"),
                                        "amount": amount_float,
                                        "percentage": percentage_float,
                                        "id_field": extracted_data["code"],
                                        # ... (other fields)
                                    }
                                    update_or_create(session, StockHolders, {"name": stockholder_data["name"]},
                                                     stockholder_data)

                        pbar.update(1)
    session.close()  # Close the session
    print("All data saved to the database.")

if __name__ == "__main__":
    main()
