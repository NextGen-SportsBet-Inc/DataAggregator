import time
from BaseBallWrapper.baseball_wrapper import BaseballWrapper
from BasketballWrapper.basketball_wrapper import BasketballWrapper
from FootballWrapper.football_wrapper import FootballWrapper
from HockeyWrapper.hockey_wrapper import HockeyWrapper
from BaseWrapper.base_wrapper import Wrapper

# TODO: Change to logging
print("Gathering information")

# Initiate Wrappers
baseball_wrapper = BaseballWrapper()
basketball_wrapper = BasketballWrapper()
football_wrapper = FootballWrapper()
hockey_wrapper = HockeyWrapper()

# Init data collection info: sports, associated wrappers, collecting data urls, queues, and routing keys
example_sport_wrapper = None
_DATA_COLLECTION: dict[str, tuple[Wrapper, dict[str, tuple[str, str]]]] = {

    "example_sport": (example_sport_wrapper, {
        "call_endpoint_url": ('rabbitmq_queue_name', 'routing_key_for_queue')
    }),

    "baseball": (baseball_wrapper, {
    }),
    "basketball": (basketball_wrapper, {
    }),
    "football": (football_wrapper, {
        "v3/odds/live": ('football_live_odds', 'odds.#')
    }),
    "hockey": (hockey_wrapper, {
    }),
}
del _DATA_COLLECTION["example_sport"]

for _, (wrapper, _dict) in _DATA_COLLECTION.items():
    for _, (queue_name, routing_key) in _dict.items():
        wrapper.declare_queue(queue_name, routing_key)


def main():
    while True:

        for sport, (wrapper, _dict) in _DATA_COLLECTION.items():

            for url, (_, routing_key) in _dict.items():

                # Collect data
                collected_data = wrapper.collect_data(url)

                if collected_data is None:
                    # TODO: Change to logging
                    print(f"No data collected for {sport} on {url}")
                    continue

                # Publish data
                # TODO: Change to logging
                print(f"Data collected for {sport} on {url}")
                wrapper.publish_data(collected_data, routing_key)

        time.sleep(5 * 60)  # Sleep 5 minutes


if __name__ == '__main__':
    main()
