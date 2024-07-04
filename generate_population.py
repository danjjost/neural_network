from config import Config
from src.pipeline.population_modifiers.population_generator import PopulationGenerator
from src.pipeline.population_modifiers.save_population import SavePopulation

if __name__ == "__main__":
    config = Config()    
    population = PopulationGenerator().generate(config.population_size, config.schema);
    SavePopulation(config.input_file_path).run(population)