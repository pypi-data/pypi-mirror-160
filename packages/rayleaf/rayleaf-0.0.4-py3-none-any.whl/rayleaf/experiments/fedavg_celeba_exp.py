from datetime import datetime


import rayleaf
import rayleaf.entities as entities
from rayleaf.entities import Server, Client


rayleaf.run_experiment(
    dataset = "celeba",
    dataset_dir = "../data/celeba/",
    output_dir= f"output/fedavg_celeba-{datetime.now()}/",
    model = "cnn",
    num_rounds = 200,
    eval_every = 10,
    ServerType=Server,
    client_types=[(Client, 200)],
    clients_per_round = 40,
    client_lr = 0.0001,
    batch_size = 64,
    seed = 0,
    use_val_set = False,
    num_epochs = 10,
    gpus_per_client_cluster = 1,
    num_client_clusters = 8,
    save_model = False,
    notes = None
)
