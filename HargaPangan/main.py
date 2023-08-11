import requests
from tqdm import tqdm
from datetime import datetime, timedelta
import json
import sys
sys.path.append("..")
from connections import Session
from models import PriceData

commodity_url = "https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetRefCommodityAndCategory"

commodity_response = requests.get(commodity_url)

if commodity_response.status_code == 200:
    commodity_data = commodity_response.json()["data"]
    commodity_info = {item["id"]: item["name"] for item in commodity_data}
else:
    print("Failed to fetch commodity data. Status code:", commodity_response.status_code)
    exit()

start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 1, 10)

current_date = start_date
delta = timedelta(days=7)

while current_date <= end_date:
    formatted_start_date = current_date.strftime("%Y-%m-%d")
    formatted_end_date = (current_date + timedelta(days=6)).strftime("%Y-%m-%d")

    for commodity_id in tqdm(commodity_info.keys(), desc="Fetching data"):
        commodity_name = commodity_info[commodity_id]
        data_url = (
            f"https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetGridDataKomoditas?"
            f"price_type_id=1&comcat_id={commodity_id}&province_id=&regency_id=&"
            f"showKota=false&showPasar=false&tipe_laporan=1&start_date={formatted_start_date}&end_date={formatted_end_date}"
        )

        response = requests.get(data_url)

        if response.status_code == 200:
            json_data = response.json()
            json_data_str = json.dumps(json_data)

            session = Session()
            price_data = PriceData(
                commodity_id=commodity_id,
                commodity_name=commodity_name,
                json_data=json_data_str
            )
            session.add(price_data)
            session.commit()
            session.close()

            tqdm.write(
                f"Data for commodity '{commodity_name}' from {formatted_start_date} to {formatted_end_date} saved using SQLAlchemy ORM")
        else:
            tqdm.write(f"Failed to fetch data for commodity '{commodity_name}'. Status code: {response.status_code}")

    current_date += delta

tqdm.write("All data saved using SQLAlchemy ORM.")
