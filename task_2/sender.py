import asyncio
import concurrent.futures
from enum import Enum
from typing import List
from datetime import timedelta
from dataclasses import dataclass
from random import *

timeout_seconds = timedelta(seconds=15).total_seconds()

@dataclass
class Payload:
    origin: str
    data: bytes

@dataclass
class Address:
    name: str
    city: str

@dataclass
class Event:
    recipients: List[Address]
    payload: Payload

class Result(Enum):
    Accepted = 1
    Rejected = 2

async def read_data() -> Event:
    return Event(
        [Address("Vlad", "Moscow"), Address("Danil", "Moscow"), Address("Angelina", "Moscow"), Address("Rolan", "Kazan")], 
        Payload("Family", [1, 2, 3]))
                 

async def send_data(dest: Address, payload: Payload) -> Result:
    return choice([Result.Accepted, Result.Rejected])

async def perform_operation() -> None:
    while True:
        try:
            event = await read_data()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                tasks = [send_data(addr, event.payload) for addr in event.recipients]
                results = await asyncio.gather(*tasks)

                for result in results:
                    if result == Result.Rejected:
                        print("Rejected")
                        await asyncio.sleep(1)
                    elif result == Result.Accepted:
                        print("Accepted")
                await asyncio.sleep(timeout_seconds)
             
        except Exception as e:
            print(f"An error occurred: {e}")



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(perform_operation())
