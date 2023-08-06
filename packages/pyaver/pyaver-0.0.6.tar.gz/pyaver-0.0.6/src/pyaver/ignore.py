import asyncio
import base58
from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair
from .enums import SolanaNetwork
from .aver_client import AverClient
from .constants import get_solana_endpoint, AVER_PROGRAM_ID, get_aver_api_endpoint
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Confirmed
import base58 
from .enums import Side, SizeFormat
from .refresh import refresh_multiple_user_markets, refresh_user_market
from solana.publickey import PublicKey
from .market import AverMarket
from .user_market import UserMarket
from requests import get, post

#DEVNET EXAMPLE

async def main():
    #Decoding the secret key from base58 to bytes
    secret_key = base58.b58decode('3QEHiFimG7U37u4tgmYi4rRFUgLQfPFGssAtqxAXwKxbuqehqVqeYxtFuufmcSfDaj5THFfgH2LsnAT3kzne6mM9')
    owner = Keypair.from_secret_key(secret_key)

    print(owner.public_key)

    #Default Transaction Options
    opts = TxOpts(preflight_commitment=Confirmed)
    connection = AsyncClient(
            get_solana_endpoint(SolanaNetwork.DEVNET),
            'confirmed',
            timeout=30
    )
    client = await AverClient.load(
        connection=connection, 
        owner=owner, 
        opts=opts, 
        network=SolanaNetwork.DEVNET, 
        program_id=AVER_PROGRAM_ID
        )

    all_markets = get(get_aver_api_endpoint(SolanaNetwork.DEVNET) + '/v2/markets')
    #Just pick the first active market
    chosen_market = ''
    for m in all_markets.json():
        print(m)
        if m['internal_status'] != 'test':
            chosen_market = m
            break
    print(chosen_market)
    market_pubkey = PublicKey(chosen_market['pubkey'])
    ###
    #Example warning
    #Sometimes, the markets loaded above may have already been resolved
    #Therefore, I've copied and pasted a market public key from https://dev.app.aver.exchange/
    ###
    market_pubkey = PublicKey('Bq8wyvvWbSLcodH3DjamHZCnRZ4XzGCg4UTCGi8tZhvL')

    #Load market
    market = await AverMarket.load(client, market_pubkey)

    #Print market data
    print(market.market_state)

    #Obtain orderbook
    outcome_1_orderbook = market.orderbooks[0]
    #Print orderbook data
    print('Best Ask Price', outcome_1_orderbook.get_best_ask_price(True))
    print('Best Bid Price', outcome_1_orderbook.get_best_bid_price(True))

    #Gets Solana Airdrop and USDC Token Airdrop
    #Only available on devnet
    # await client.request_lamport_airdrop(1_000_000, owner.public_key)
    # print('New Balance: ', await client.request_lamport_balance(owner.public_key))
    # #Creates Associated Token Account where tokens will be stored
    # ata = await client.get_or_create_associated_token_account(
    #     owner.public_key,
    #     owner,
    # )
    # signature = request_token_airdrop(client.aver_api_endpoint, client.quote_token,owner.public_key, 1_000_000_000)['signature']
    # #Wait to ensure transaction has been confirmed before moving on
    # await client.provider.connection.confirm_transaction(signature, Confirmed) 
    # token_balance = await client.request_token_balance(client.quote_token, owner.public_key)
    # print('New token balance: ', token_balance)

    #Create User Market Account
    #This function also automatically gets_or_creates a UserHostLifetime account
    uma = await UserMarket.get_or_create_user_market_account(
        client,
        market,
        owner,
        host=PublicKey('2eGTu9d4hdGvwvFDGG34a3JRLFiQ2Ar92LjJpb4vyQFw')
    )


    #Place order
    #This order a BUY side on outcome 1 at a price of 0.5 and size 10
    #This means it will cost 5 tokens and we will win 10 (once the bet is matched and if we win)
    # signature = await uma.place_order(
    #     owner,
    #     0, #Outcome 1
    #     Side.BUY,
    #     limit_price=0.5,
    #     size=3,
    #     size_format=SizeFormat.PAYOUT
    # )
    # #Wait to ensure transaction has been confirmed before moving on
    # await client.provider.connection.confirm_transaction(signature['result'], Confirmed)

    #Refresh market information efficiently
    #Refreshing a User Market also automatically refreshes the market
    uma = (await refresh_multiple_user_markets(client, [uma, uma]))[0]
    market = uma.market
    print('UHL')
    print(uma.user_host_lifetime.user_host_lifetime_state)
    
    #Cancel order
    #We should only have 1 order, so we'll cancel the first in the array
    # my_order_id = uma.user_market_state.orders[0].order_id
    # signature = await uma.cancel_order(
    #     owner,
    #     my_order_id,
    #     0, #We placed an order on outcome 1
    #     active_pre_flight_check=True
    # )
    signature = await uma.cancel_all_orders([0], owner)
    #Wait to ensure transaction has been confirmed before moving on
    await client.provider.connection.confirm_transaction(signature[0]['result'], Confirmed) 

    #Finally close the client
    await client.close()
def request_token_airdrop(
    aver_api_endpoint: str,
    quote_token: PublicKey,
    owner: PublicKey, 
    amount: int = 1_000_000_000,
    ):

    url = aver_api_endpoint + '/airdrop'

    body = {
        'wallet': owner.to_base58(),
        'mint': quote_token.__str__(),
        'amount': amount
    }

    response = post(url, body)
    return response.json()
    

asyncio.run(main())