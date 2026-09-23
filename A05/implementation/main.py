import asyncio
import logging
from fixtures import FIXTURES
from ingestion import fetch_fixture, worker

# Configure logging to clearly see concurrent execution and interleaving
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s | %(message)s',
    datefmt='%H:%M:%S'
)

async def main():
    logging.info("Starting Concurrent Market Fixture Ingestion Pipeline")
    
    # Create a severely Bounded Queue (maxsize=2) to guarantee backpressure triggers
    queue = asyncio.Queue(maxsize=2)
    
    # 2. Concurrent Execution: Start Consumers (Workers)
    workers = []
    for i in range(2): # 2 Workers
        task = asyncio.create_task(worker(i+1, queue))
        workers.append(task)
        
    # 2. Concurrent Execution: Start Producers
    producers = []
    for i, fixture in enumerate(FIXTURES):
        task = asyncio.create_task(fetch_fixture(fixture, queue, i+1))
        producers.append(task)
        
    # Wait for all producers to finish generating data
    await asyncio.gather(*producers)
    logging.info("All producers finished pushing. Waiting for workers to drain the queue...")
    
    # Block until the queue is completely processed
    await queue.join()
    logging.info("Queue successfully drained.")
    
    # Cancel the infinite worker loops
    for w in workers:
        w.cancel()
        
    # Allow workers to process their own cancellation exceptions
    await asyncio.gather(*workers, return_exceptions=True)
    logging.info("Pipeline cleanly shut down.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Manual interruption.")