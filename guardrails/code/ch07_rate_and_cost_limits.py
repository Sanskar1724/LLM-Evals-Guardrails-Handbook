"""
Chapter 7 - Rate limits and cost limits.

Run:  python ch07_rate_and_cost_limits.py

Every model call costs money and time. Without limits, one user
(or one bug in a loop) can use up your whole budget.

Four small limits:
  1. input size limit      - refuse very long messages
  2. rate limit            - max requests per minute for each user (token bucket)
  3. daily budget          - stop when today's spend reaches a cap
  4. step limit for agents - stop a loop that never ends

The clock is simulated, so the script finishes at once.

No key needed. Standard library only.
"""


class FakeClock:
    """A clock we move by hand, so the demo does not have to wait."""

    def __init__(self):
        self.now = 0.0

    def time(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class TokenBucket:
    """
    Classic rate limiter.
    The bucket holds up to `capacity` tokens. Each request takes one.
    Tokens come back at `refill_per_second`. Empty bucket = request refused.
    (Here "token" means a permission slip, not a word piece.)
    """

    def __init__(self, capacity, refill_per_second, clock):
        self.capacity = capacity
        self.refill_per_second = refill_per_second
        self.clock = clock
        self.tokens = float(capacity)
        self.last_time = clock.time()

    def allow(self):
        now = self.clock.time()
        self.tokens = min(self.capacity, self.tokens + (now - self.last_time) * self.refill_per_second)
        self.last_time = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


def estimate_tokens(text):
    """Rough rule for English: about 4 characters per token."""
    return max(1, len(text) // 4)


class Budget:
    """Tracks spend for one day and refuses calls that would pass the cap."""

    def __init__(self, daily_cap, price_per_1000_tokens):
        self.daily_cap = daily_cap
        self.price = price_per_1000_tokens
        self.spent = 0.0

    def cost_of(self, input_text, max_output_tokens):
        tokens = estimate_tokens(input_text) + max_output_tokens     # worst case
        return tokens / 1000 * self.price

    def try_spend(self, input_text, max_output_tokens):
        cost = self.cost_of(input_text, max_output_tokens)
        if self.spent + cost > self.daily_cap:
            return False, cost
        self.spent += cost
        return True, cost


MAX_INPUT_CHARS = 2000
MAX_OUTPUT_TOKENS = 300


def handle_request(user, text, buckets, budget, clock):
    """Run all limits in order. Cheap checks first."""
    if len(text) > MAX_INPUT_CHARS:
        return "REFUSED: message too long"
    bucket = buckets.setdefault(user, TokenBucket(capacity=3, refill_per_second=3 / 60, clock=clock))
    if not bucket.allow():
        return "REFUSED: too many requests, please wait"
    ok, cost = budget.try_spend(text, MAX_OUTPUT_TOKENS)
    if not ok:
        return "REFUSED: daily budget reached"
    return f"OK (cost about {cost:.4f}, spent today {budget.spent:.4f})"


def run_agent_with_step_limit(max_steps=5):
    """An agent that is stuck in a loop. The step limit stops it."""
    steps = 0
    while True:
        if steps >= max_steps:
            return f"STOPPED after {steps} steps: step limit reached"
        steps += 1
        _action = "search again"      # the stuck agent always picks the same action


def main():
    clock = FakeClock()
    buckets = {}
    budget = Budget(daily_cap=0.05, price_per_1000_tokens=0.01)

    print("PART 1 - rate limit: 3 requests per minute for each user")
    for i in range(1, 6):
        print(f"  t={clock.time():>4.0f}s asha request {i}: {handle_request('asha', 'hello', buckets, budget, clock)}")
    print(f"  t={clock.time():>4.0f}s ravi request 1: {handle_request('ravi', 'hello', buckets, budget, clock)}   <- other users are not affected")
    clock.advance(20)
    print(f"  t={clock.time():>4.0f}s asha request 6: {handle_request('asha', 'hello', buckets, budget, clock)}   <- one token came back after 20s")

    print()
    print("PART 2 - input size limit")
    print("  huge message:", handle_request("asha", "x" * 5000, buckets, budget, clock))

    print()
    print("PART 3 - daily budget of 0.05")
    clock.advance(3600)
    for i in range(1, 20):
        clock.advance(60)
        result = handle_request("user" + str(i), "please summarise this text " * 20, buckets, budget, clock)
        if result.startswith("REFUSED"):
            print(f"  request {i}: {result}")
            break
        print(f"  request {i}: {result}")

    print()
    print("PART 4 - step limit for an agent loop")
    print(" ", run_agent_with_step_limit(max_steps=5))


if __name__ == "__main__":
    main()
