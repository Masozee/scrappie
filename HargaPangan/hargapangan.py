import requests
import csv
from tqdm import tqdm

# Step 1: Fetch data from the first URL to get the commodity IDs
commodity_url = "https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetRefCommodityAndCategory"

commodity_response = requests.get(commodity_url)

if commodity_response.status_code == 200:
    commodity_data = commodity_response.json()["data"]
    commodity_info = {item["id"]: item["name"] for item in commodity_data}
else:
    print("Failed to fetch commodity data. Status code:", commodity_response.status_code)
    exit()

# Step 2: Fetch data for each commodity using the second URL
base_data_url = "https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetGridDataKomoditas"
price_type_id = 1
start_date = "2020-08-01"
end_date = "2020-08-09"
province_id = ""
regency_id = ""
show_kota = False
show_pasar = False
tipe_laporan = 1

for commodity_id in tqdm(commodity_info.keys(), desc="Fetching data"):
    commodity_name = commodity_info[commodity_id]
    data_url = (
        f"{base_data_url}?price_type_id={price_type_id}&comcat_id={commodity_id}&province_id={province_id}&"
        f"regency_id={regency_id}&showKota={show_kota}&showPasar={show_pasar}&tipe_laporan={tipe_laporan}&"
        f"start_date={start_date}&end_date={end_date}"
    )

    response = requests.get(data_url)

    if response.status_code == 200:
        data = response.json()
        extracted_data = data["data"]

        csv_filename = f"data_commodity_{commodity_name}.csv"  # Use commodity name

        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = extracted_data[0].keys() if extracted_data else []
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            csv_writer.writeheader()
            csv_writer.writerows(extracted_data)

        tqdm.write(f"Data for commodity '{commodity_name}' saved in '{csv_filename}'")
    else:
        tqdm.write(f"Failed to fetch data for commodity '{commodity_name}'. Status code: {response.status_code}")
