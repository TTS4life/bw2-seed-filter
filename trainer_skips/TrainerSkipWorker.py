from ui.FieldData import DataWorker
from rng.util import Gen5RNG
from trainer_skips.w2_thewholeskip import main as skip_main

class TrainerSkipWorkerHandler(DataWorker):
    
    
    
    def process(self, parameters):
        print("HIT WORKER!!!!!!")
        print(parameters)
        # If worker is BW2, create BW2 worker and run it
        # If worker is BW1, create BW1 worker instead

        skip_main(parameters)

    def get_name(self):
        return "Trainer Skip Generator"