#!/usr/bin/env python3
"""
Ollama Load Testing Script
Tests concurrent request limits and performance on Raspberry Pi 5

Usage:
    python test_ollama_load.py --concurrent 1   # Test single request
    python test_ollama_load.py --concurrent 5   # Test 5 parallel requests
    python test_ollama_load.py --concurrent 10  # Test 10 parallel requests
"""
import asyncio
import time
import statistics
import argparse
from typing import List
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

# Short test prompt to reduce wait time
TEST_PROMPT = """Generate a simple recipe with these ingredients: tomatoes, pasta, garlic.
Format: Recipe name, ingredients list, 3 steps. Keep it short."""


def test_single_request(request_id: int) -> dict:
    """Send a single synchronous request to Ollama"""
    print(f"[Request {request_id}] Starting...")
    start = time.time()

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": TEST_PROMPT,
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": 200}
            },
            timeout=120
        )
        response.raise_for_status()
        duration = time.time() - start

        result = response.json()
        tokens = len(result.get("response", "").split())

        print(f"[Request {request_id}] ✅ Success in {duration:.2f}s ({tokens} tokens)")
        return {
            "id": request_id,
            "success": True,
            "duration": duration,
            "tokens": tokens,
            "error": None
        }
    except Exception as e:
        duration = time.time() - start
        print(f"[Request {request_id}] ❌ Failed after {duration:.2f}s: {e}")
        return {
            "id": request_id,
            "success": False,
            "duration": duration,
            "tokens": 0,
            "error": str(e)
        }


async def test_concurrent_requests(num_concurrent: int) -> List[dict]:
    """Run multiple requests in parallel using threads"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing {num_concurrent} concurrent requests to Ollama")
    print(f"{'='*60}\n")

    start_time = time.time()

    # Use asyncio to simulate concurrent requests (blocking I/O in thread pool)
    loop = asyncio.get_event_loop()
    tasks = [
        loop.run_in_executor(None, test_single_request, i)
        for i in range(1, num_concurrent + 1)
    ]

    results = await asyncio.gather(*tasks)
    total_time = time.time() - start_time

    # Calculate statistics
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    if successful:
        durations = [r["duration"] for r in successful]
        avg_duration = statistics.mean(durations)
        min_duration = min(durations)
        max_duration = max(durations)
        median_duration = statistics.median(durations)
    else:
        avg_duration = min_duration = max_duration = median_duration = 0

    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Total requests:       {num_concurrent}")
    print(f"Successful:           {len(successful)} ✅")
    print(f"Failed:               {len(failed)} ❌")
    print(f"Total time:           {total_time:.2f}s")
    print(f"\nResponse Times (successful requests):")
    print(f"  Average:            {avg_duration:.2f}s")
    print(f"  Median:             {median_duration:.2f}s")
    print(f"  Min:                {min_duration:.2f}s")
    print(f"  Max:                {max_duration:.2f}s")

    if failed:
        print(f"\n❌ Failed requests:")
        for r in failed:
            print(f"  Request {r['id']}: {r['error']}")

    # Performance analysis
    print(f"\n{'='*60}")
    print(f"💡 ANALYSIS")
    print(f"{'='*60}")

    if len(successful) == num_concurrent:
        print(f"✅ All requests succeeded!")
        if max_duration > avg_duration * 2:
            print(f"⚠️  Some requests took 2x longer than average")
            print(f"   → Pi may be struggling with {num_concurrent} concurrent requests")
        else:
            print(f"✅ Response times fairly consistent")
            print(f"   → Pi handles {num_concurrent} concurrent requests well")
    elif len(successful) > 0:
        print(f"⚠️  {len(failed)} requests failed out of {num_concurrent}")
        print(f"   → Pi is at/above capacity with {num_concurrent} concurrent requests")
    else:
        print(f"❌ All requests failed!")
        print(f"   → Pi cannot handle {num_concurrent} concurrent requests")

    print(f"{'='*60}\n")

    return results


def main():
    parser = argparse.ArgumentParser(description="Test Ollama concurrent request limits")
    parser.add_argument(
        "--concurrent", "-c",
        type=int,
        default=1,
        help="Number of concurrent requests to send (default: 1)"
    )
    args = parser.parse_args()

    print(f"\n🚀 Ollama Load Test")
    print(f"Target: {OLLAMA_URL}")
    print(f"Model:  {MODEL}")

    # Run test
    asyncio.run(test_concurrent_requests(args.concurrent))


if __name__ == "__main__":
    main()
