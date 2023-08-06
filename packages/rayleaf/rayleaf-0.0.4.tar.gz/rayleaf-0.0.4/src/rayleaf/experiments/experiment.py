from rayleaf.experiments.fedavg_cnn_exp import fedavg_cnn
# from dpsgd_cnn_exp import dpsgd_cnn
# from sign_cnn_exp import sign_femnist


NUM_ROUNDS = 10
EVAL_EVERY = 1
NUM_CLIENTS = 10
CLIENTS_PER_ROUND = 5
CLIENT_LR = 0.06
BATCH_SIZE = 64
SEED = 0
NUM_EPOCHS = 10
GPUS_PER_CLIENT_CLUSTER = 1
NUM_CLIENT_CLUSTERS = 2
SAVE_MODEL = False
USE_GRADS = True

fedavg_cnn(
    num_rounds = NUM_ROUNDS,
    eval_every = EVAL_EVERY,
    num_clients = NUM_CLIENTS,
    clients_per_round = CLIENTS_PER_ROUND,
    client_lr = CLIENT_LR,
    batch_size = BATCH_SIZE,
    seed = SEED,
    num_epochs = NUM_EPOCHS,
    gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
    num_client_clusters = NUM_CLIENT_CLUSTERS,
    save_model = SAVE_MODEL,
    use_grads = USE_GRADS
)

# for stdev in [10 ** n for n in range(-4, 2)]:
#     for C in [10 ** n for n in range(-2, 4)]:
#         dpsgd_cnn(
#             stdev = stdev,
#             C = C,
#             num_rounds = NUM_ROUNDS,
#             eval_every = EVAL_EVERY,
#             num_clients = NUM_CLIENTS,
#             clients_per_round = CLIENTS_PER_ROUND,
#             client_lr = CLIENT_LR,
#             batch_size = BATCH_SIZE,
#             seed = SEED,
#             num_epochs = NUM_EPOCHS,
#             gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#             num_client_clusters = NUM_CLIENT_CLUSTERS,
#             save_model = SAVE_MODEL,
#             notes = f"stdev = {stdev}, C = {C}"
#         )

# sign_femnist(
#     num_rounds = NUM_ROUNDS,
#     eval_every = EVAL_EVERY,
#     num_clients = NUM_CLIENTS,
#     clients_per_round = CLIENTS_PER_ROUND,
#     client_lr = CLIENT_LR,
#     batch_size = BATCH_SIZE,
#     seed = SEED,
#     num_epochs = NUM_EPOCHS,
#     gpus_per_client_cluster = GPUS_PER_CLIENT_CLUSTER,
#     num_client_clusters = NUM_CLIENT_CLUSTERS,
#     save_model = SAVE_MODEL
# )
