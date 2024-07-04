from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

PROJECT_ID = "project-name-69696969"
DATASET_ID = "dataset-id"
PATH_TO_CREDS = "ebay-api\image_upload\project-name-696969-3e69ddba6a9e.json"

def get_listing_images_for_quality_scoring(category):
    client = bigquery.Client("project-name-696969")

    df = client.query("query").to_dataframe()
    num_rows = df.shape[0]
    
    print(f"Number of rows in the DataFrame: {num_rows}")
    return df

def get_creds():
    credentials = service_account.Credentials.from_service_account_file(PATH_TO_CREDS,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    return credentials


def read_bigquery(query, project_id: str = PROJECT_ID):
    client = bigquery.Client(credentials=get_creds(), project=project_id)
    df = client.query(query).to_dataframe()
    return df

dict_query = [read_bigquery("SELECT image_url FROM project-name-696969.listings.ebay_listing_images LIMIT 5").to_dict()]
for i in dict_query:
    print(i)
