from google.cloud import bigquery
import logging

logger = logging.getLogger(__name__)


class BigQueryTableRetriever:
    def __init__(self, project: str):
        self.bq_client = bigquery.Client(project=project)

    def retrieve(self, table_uri: str):
        logger.info("Downloading features...")
        query = f"select * from {table_uri}"
        logger.info(f"bq_client.project: {self.bq_client.project}")

        import os
        import json

        def get_project_id():
            # In python 3.7, this works
            project_id = os.getenv("GCP_PROJECT")

            if not project_id:  # > python37
                # Only works on runtime.
                import urllib.request

                url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
                req = urllib.request.Request(url)
                req.add_header("Metadata-Flavor", "Google")
                project_id = urllib.request.urlopen(req).read().decode()

            if not project_id:  # Running locally
                with open(os.environ["GOOGLE_APPLICATION_CREDENTIALS"], "r") as fp:
                    credentials = json.load(fp)
                project_id = credentials["project_id"]

            if not project_id:
                raise ValueError("Could not get a value for PROJECT_ID")

            return project_id

        logger.info(f"get_project_id: {get_project_id()}")
        df = self.bq_client.query(query).to_dataframe()
        return df
