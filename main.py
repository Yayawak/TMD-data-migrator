# import sys
# sys.path.insert(0, "./scrapper")

from scrapper.scrapper import Scrapper
from nakornnayok_latlong_loader.latlong_loader import getLatLongOfNakornnayok
import pandas as pd

if __name__ == "__main__":
    print("Start program.")
    

    latlongs_nk_data = getLatLongOfNakornnayok()

    scp = Scrapper()
    df = scp.getDateTimeCSVDataFrame()
    scp.release()

    # for sheet_name, latlong2d in latlongs_nk_data:
    #     # latlong2d[0][0]
    #     print(sheet_name)
        # print(latlong2d[0])
        # print(latlong2d)
        # print()

        # df['']

    csv_urls = df['csv url']
    pd.read_csv(csv_urls[0]).to_csv("out.csv")

    # csv_urls[0]
    for url in csv_urls:
        print(url)
    #     csv_df = pd.read_csv(url)
        # csv_df.
        # print(csv_df)
