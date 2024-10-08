import time
from typing import Optional
from config import Config
from src.azure_helpers.blob_client import BlobClient
from src.pipeline.population import PopulationDTO
from src.utilities.logger import Logger


class BlobPoller():
    def __init__(self, output_blob_client: BlobClient, config: Optional[Config] = None) -> None:
        self.output_blob_client = output_blob_client
        self.config = config if config is not None else Config()

    def poll(self, population: PopulationDTO) -> None:
        Logger().debug("BlobPoller - Starting...")
        blobs_to_await = [n.id for n in population.population]
        
        time_started_ms = self.get_current_time_ms()
        
        while self.has_blobs_to_await(blobs_to_await) and (self.is_timed_out(time_started_ms) is False):
            output_ids = self.output_blob_client.get_all_ids()
            
            for blob_name in output_ids:
                if blob_name in blobs_to_await:
                    self.update_network_in_population(population, blob_name)
                    blobs_to_await.remove(blob_name)
            
            time.sleep(self.config.polling_rate_ms / 1000)
        
        Logger().debug(f'BlobPoller - Finished with "{len(blobs_to_await)}" blobs left to await.')
        self.log_statistics(population)

    def get_current_time_ms(self):
        return time.time() * 1000

    def is_timed_out(self, time_started: float) -> bool:
        current_time = self.get_current_time_ms()
        return current_time - time_started > self.config.poll_timeout_ms

    def has_blobs_to_await(self, blobs_to_await: list[str]):
        return len(blobs_to_await) != 0

    def update_network_in_population(self, population: PopulationDTO, blob_name: str) -> None:
        network = self.output_blob_client.download(blob_name)
                    
        for i in range(len(population.population)):
            if population.population[i].id == network.id:
                population.population[i] = network
                
    def log_statistics(self, population: PopulationDTO):
        try:
            scores = [n.score for n in population.population]
            
            population.average_score = sum(scores) / len(scores)
            population.min_score = min(scores)
            population.max_score = max(scores)
            
            Logger().debug(f'BlobPoller - Average Score: {population.average_score}')
            Logger().debug(f'BlobPoller - Min Score: {population.min_score}')
            Logger().debug(f'BlobPoller - Max Score: {population.max_score}')
            
        except Exception as e:
            Logger().log(f'BlobPoller - Error logging statistics, skipping: {e}')
