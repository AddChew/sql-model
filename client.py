import time
import asyncio

from httpx import AsyncClient
from tenacity import AsyncRetrying, stop_after_attempt, wait_random_exponential


class BaseAsyncClient:

    def __init__(self,
                 max_retries: int = 3,
                 timeout: float = 30.0,
                 ):
        self.retry = AsyncRetrying(
            stop = stop_after_attempt(max_attempt_number = max_retries),
            wait = wait_random_exponential(multiplier = 0.1, max = 30),
            reraise = True,
        )
        self.client = AsyncClient(timeout = timeout)
        self.client.headers.update({"x-acc-op": "sadsafas"})

    async def send_request(self, prompt: str):
        response = await self.client.get("https://jsonplaceholder.typicode.com/todos/1")
        return response.json()
    
    async def send_requests(self, prompts: list):
        retry_send_request = self.retry.wraps(self.send_request)
        results = await asyncio.gather(*[
            retry_send_request(prompt) for prompt in prompts
        ])
        return results

    def stream(self, prompts: list):
        return asyncio.run(self.send_requests(prompts))
    

client = BaseAsyncClient(timeout=30)
start = time.time()
print(client.stream(prompts = [i for i in range(10)]))
end = time.time()
print(end - start)