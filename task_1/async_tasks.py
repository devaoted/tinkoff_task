import asyncio
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from random import *

class Response(Enum):
    Success = 1
    RetryAfter = 2
    Failure = 3

class ApplicationStatusResponse(Enum):
    Success = 1
    Failure = 2

@dataclass
class ApplicationResponse:
    application_id: str
    status: ApplicationStatusResponse
    description: str
    last_request_time: datetime
    retriesCount: int

async def get_application_status1(identifier: str) -> Response:
    status = choice([Response.Success, Response.RetryAfter, Response.Failure])
    delay = uniform(0, 1)
    await asyncio.sleep(delay)
    print("1", status, delay)
    return status

async def get_application_status2(identifier: str) -> Response:
    status = choice([Response.Success, Response.RetryAfter, Response.Failure])
    delay = uniform(0, 1)
    await asyncio.sleep(delay)
    print("2", status, delay)
    return status

async def perform_operation(identifier: str) -> ApplicationResponse:
    start_time = datetime.now()
    retries_count = 0

    while (datetime.now() - start_time).total_seconds() < 15:
        future1 = asyncio.ensure_future(get_application_status1(identifier))
        future2 = asyncio.ensure_future(get_application_status2(identifier))

        done, pending = await asyncio.wait([future1, future2], return_when=asyncio.FIRST_COMPLETED)
 
        for task in pending:
            task.cancel()

        for task in done:
            response = task.result()
            if response == Response.RetryAfter:
                await asyncio.sleep(1)  
                retries_count += 1
            elif response == Response.Success:
                return ApplicationResponse(
                    application_id=identifier,
                    status=ApplicationStatusResponse.Success,
                    description="Success",
                    last_request_time=datetime.now(),
                    retriesCount=retries_count)
            else:
                return ApplicationResponse(
                    application_id=identifier,
                    status=ApplicationStatusResponse.Failure,
                    description="Failed",
                    last_request_time=datetime.now(),
                    retriesCount=retries_count)

    return ApplicationResponse(
        application_id=identifier,
        status=ApplicationStatusResponse.Failure,
        description="Timeout reached",
        last_request_time=datetime.now(),
        retriesCount=retries_count
    )

    
async def main():
    identifier = "identifier"
    result = await perform_operation(identifier)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())