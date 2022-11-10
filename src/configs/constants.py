import torch

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

num_workers = 8
should_log = True

batch_size = 2
train_epochs = 4
word_len_padding = 24  # will be overriden if the dataset contains labels longer than the constant
learning_rate = 5e-6