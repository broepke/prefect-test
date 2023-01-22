import requests
from prefect import flow, task
from prefect import flow, get_run_logger
from prefect_snowflake.database import SnowflakeConnector
from prefect_snowflake.database import snowflake_query

snowflake_connector_block = SnowflakeConnector.load("fxdmz")

@task
def get_imdb_list(result):
    
    id_list = []
    
    for i in range(len(result)):
        id_list.append(result[i][2])
    
    return id_list

@task
def built_url(id_list):
    
    url = "https://t241zyf9j9.execute-api.us-east-1.amazonaws.com/default/lamba-tmdb?"
    
    for i in range(len(id_list)):
        url += "ids="
        url += id_list[i]
        if i == len(id_list)-1:
            return url
        else:
            url += "&"
    
    return url

@flow(retries = 3)
def get_tmdb_records():
    
    logger = get_run_logger()
    
    # The max should never exceed 70 records based on URL limits
    query = """
    SELECT ORG_ID, CREATIVEWORKID, IMDB_VALUE
    FROM EIDR.PUBLIC.ORGS_IMDB_FILTERED
    ORDER BY RANDOM()
    LIMIT 3;
    """
    
    result = snowflake_query(
        query,
        snowflake_connector_block,
        params={"id_param": 1}
    )
    
    id_list = get_imdb_list(result)
    logger.info(id_list)
    
    url = built_url(id_list)
    logger.info(url)
    
    # Call the Lambda function
    response = requests.get(url)
    
    if response.status_code == 200:
        return logger.info(response.status_code)
    else:
        raise Exception(response.status_code)
        #return logger.warning(response.status_code)
    


if __name__ == "__main__":
    get_tmdb_records()
