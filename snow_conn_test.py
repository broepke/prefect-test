import pprint

from prefect import flow
from prefect_snowflake.database import SnowflakeConnector
from prefect_snowflake.database import snowflake_query

snowflake_connector_block = SnowflakeConnector.load("fxdmz")

@flow
def snowflake_query_flow():
    
    query = """select * from orgs where org_id = '4911a544-e3be-4f16-b2f6-92e9ee166ab1';"""
    
    result = snowflake_query(
        query,
        snowflake_connector_block,
        params={"id_param": 1}
    )
    return result

pprint.pprint(snowflake_query_flow())
