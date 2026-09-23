import asyncio
import logging
from fixtures import Fixture

logger = logging.getLogger(__name__)

async def fetch_fixture(fixture: Fixture, queue: asyncio.Queue, producer_id: int):
    """Producer: Simulates fetching ticks and pushing them to a bounded queue."""
    for i in range(3): # Generate 3 ticks per fixture
        item = f"{fixture.symbol}_TICK_{i+1}"
        logger.info(f"[Producer {producer_id}] Fetching {item}...")
        
        try:
            # 1. Await suspension & 3. Timeout/Cancellation
            if fixture.should_timeout:
                # Force a timeout by setting a strict limit smaller than the delay
                await asyncio.wait_for(asyncio.sleep(fixture.delay), timeout=1.0)
            else:
                # Normal I/O await suspension
                await asyncio.sleep(fixture.delay)
                
        except asyncio.TimeoutError:
            logger.error(f"[Producer {producer_id}] TIMEOUT fetching {fixture.symbol}! Canceling feed.")
            break # Exit producer loop on timeout
            
        # 4. Bounded Queue Backpressure Check
        if queue.full():
            logger.warning(f"[Producer {producer_id}] QUEUE FULL! Backpressure applied. Waiting to push {item}...")
            
        # Producer will physically block here if the queue is full
        await queue.put(item)
        logger.info(f"[Producer {producer_id}] Placed {item} in queue. (Size: {queue.qsize()})")

async def worker(worker_id: int, queue: asyncio.Queue):
    """Consumer: Processes items from the queue."""
    try:
        while True:
            # Await suspension waiting for work
            item = await queue.get()
            logger.info(f"[Worker {worker_id}] Started processing {item}...")
            
            # Simulate heavy processing (slower than producers to force backpressure)
            await asyncio.sleep(1.0) 
            
            logger.info(f"[Worker {worker_id}] Finished {item}. (Queue size: {queue.qsize()})")
            queue.task_done()
            
    except asyncio.CancelledError:
        logger.info(f"[Worker {worker_id}] Shutdown signal received. Canceling worker.")