from datetime import datetime

import torch


import rayleaf
from rayleaf.entities import Server, Client


def dpsgd_cnn(
    stdev: float,
    C: float,
    num_rounds: int = 100,
    eval_every: int = 10,
    num_clients: int = 200,
    clients_per_round: int = 40,
    client_lr: float = 0.05,
    batch_size: int = 64,
    seed: int = 0,
    num_epochs: int = 10,
    gpus_per_client_cluster: float = 1,
    num_client_clusters: int = 8,
    save_model: bool = False,
    notes: str = None
):
    curr_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    class DPSGDClient(Client):
        def train(self):
            self.train_model(compute_grads=True)

            for param_tensor, layer in self.grads.items():
                self.grads[param_tensor] /= max(1, torch.linalg.norm(layer) / C)
                self.grads[param_tensor] += stdev * C * torch.randn(layer.shape)

            return self.num_train_samples, self.grads
    

    class DPSGDServer(Server):
        def update_model(self):
            self.reset_grads()

            total_weight = 0
            for (client_samples, client_grad) in self.updates:
                total_weight += client_samples

                for param_tensor, grad in client_grad.items():
                    self.grads[param_tensor] += client_samples * grad

            for param_tensor in self.grads.keys():
                self.grads[param_tensor] /= total_weight
            
            for param_tensor, grad in self.grads.items():
                self.model_params[param_tensor] += grad


    rayleaf.run_experiment(
        dataset = "femnist",
        dataset_dir = "data/femnist/",
        output_dir= f"output/dpsgd_cnn-{curr_time}/",
        model = "cnn",
        num_rounds = num_rounds,
        eval_every = eval_every,
        ServerType=DPSGDServer,
        client_types=[(DPSGDClient, num_clients)],
        clients_per_round = clients_per_round,
        client_lr = client_lr,
        batch_size = batch_size,
        seed = seed,
        use_val_set = False,
        num_epochs = num_epochs,
        gpus_per_client_cluster = gpus_per_client_cluster,
        num_client_clusters = num_client_clusters,
        save_model = save_model,
        notes = notes
    )
