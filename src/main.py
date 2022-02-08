from PIL import Image
from torch.utils.data import DataLoader

from .configs import paths
from .configs.constants import BATCH_SIZE, NUM_WORKERS, TRAIN_EPOCHS
from .context import Context
from .dataset import HCRDataset, MemoryDataset
from .scripts import predict, train, validate
from .util import debug_print, init_model_for_training, load_model, load_processor


class TrocrPredictor:
    def __init__(self, use_local_model: bool = True):
        self.processor = load_processor()
        self.model = load_model(use_local_model)

    def predict_for_image_paths(self, image_paths: list[str]) -> list[str]:
        images = [Image.open(path) for path in image_paths]
        return self.predict_images(images)

    def predict_images(self, images: list[Image.Image]) -> list[str]:
        dataset = MemoryDataset(images, self.processor)
        dataloader = DataLoader(dataset, BATCH_SIZE)
        predictions = predict(self.processor, self.model, dataloader)
        return [p[1] for p in sorted(predictions)]


def main_train(use_local_model: bool = False):
    processor = load_processor()
    train_dataset = HCRDataset(paths.train_dir, processor)
    train_dataloader = DataLoader(train_dataset, BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS)

    val_dataset = HCRDataset(paths.val_dir, processor)
    val_dataloader = DataLoader(val_dataset, BATCH_SIZE, num_workers=NUM_WORKERS)

    model = load_model(use_local_model)
    init_model_for_training(model, processor)

    context = Context(model, processor, train_dataset, train_dataloader, val_dataset, val_dataloader)
    train(context, TRAIN_EPOCHS)
    debug_print(f"Saving model to {paths.model_path}...")
    model.save_pretrained(paths.model_path)


def main_validate(use_local_model: bool = True):
    processor = load_processor()
    val_dataset = HCRDataset(paths.val_dir, processor)
    val_dataloader = DataLoader(val_dataset, BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS)

    model = load_model(use_local_model)

    context = Context(model, processor, None, None, val_dataset, val_dataloader)
    validate(context, True)