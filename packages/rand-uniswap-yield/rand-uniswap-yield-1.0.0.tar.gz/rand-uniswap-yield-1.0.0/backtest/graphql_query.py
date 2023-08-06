from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import pandas as pd
from datetime import datetime


def graph(network: str, address: str, fromdate: int) -> pd.DataFrame:

    if network == 'ethereum':
        url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'
    elif network == 'polygon':
        # 'https://api.thegraph.com/subgraphs/name/steegecs/uniswap-v3-polygon'
        url = 'https://api.thegraph.com/subgraphs/name/zephyrys/uniswap-polygon-but-it-works'
    elif network == 'arbitrum':
        url = 'https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-arbitrum-one'
    elif network == 'optimism':
        url = 'https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-optimism-dev'

    sample_transport = RequestsHTTPTransport(
        url=url,
        verify=True,
        retries=5,
    )
    client = Client(
        transport=sample_transport
    )

    # Printing out query date
    fromatted_date = datetime.utcfromtimestamp(
        fromdate).strftime('%Y-%m-%d %H:%M:%S')

    # Making the query for gql
    query_text = '''
        query ($fromdate: Int!)
        {
        poolHourDatas(where:{pool:"'''+str(address)+'''",periodStartUnix_gt:$fromdate},orderBy:periodStartUnix,orderDirection:desc,first:1000)
        {
        periodStartUnix
        liquidity
        high
        low
        pool{
            
            totalValueLockedUSD
            totalValueLockedToken1
            totalValueLockedToken0
            token0
                {decimals
                }
            token1
                {decimals
                }
            }
        close
        feeGrowthGlobal0X128
        feeGrowthGlobal1X128
        }
    
        }
        '''
    query = gql(query_text)
    params = {
        "fromdate": fromdate
    }

    # Printing query infos
    print("-------------------------------- GraphQL Query --------------------------------")
    print("Query information:")
    print("Endpoint:", url)
    print("Network:", network)
    print("Pool contract:", address)
    print("Uniswap pool info:",
          f"https://info.uniswap.org/#/{network}/pools/{address}")
    print('Querying from unix timestamp:', fromdate, '/', fromatted_date)
    print('Querying GraphQL endpoint:', url)

    # Executing query and formatting returned value
    response = client.execute(query, variable_values=params)
    df = pd.json_normalize(response['poolHourDatas'])
    df = df.astype(float)
    print("Query succeeded.")
    print("-------------------------------- GraphQL Query --------------------------------")

    return df
