import torch
import os

from torch.utils.data import DataLoader
from torchvision.transforms import transforms

from model.dataset import CUDAPrefetcher, TrainValidHRTFDataset, CPUPrefetcher


def initialise_folders(tag, overwrite):
    """Set up folders for given tag

    :param tag: label to use for run
    :param overwrite: whether to overwrite existing model outputs
    """
    if overwrite:
        try:
            os.mkdir(f'runs')
        except:
            pass
        try:
            os.mkdir(f'runs/{tag}')
        except:
            pass


def load_dataset(config, mean, std) -> [CUDAPrefetcher, CUDAPrefetcher, CUDAPrefetcher]:
    """Based on https://github.com/Lornatang/SRGAN-PyTorch/blob/main/train_srgan.py"""
    # define transforms
    transform = transforms.Normalize(mean=mean, std=std)
    # Load train, test and valid datasets
    train_datasets = TrainValidHRTFDataset(config.train_hrtf_dir, config.hrtf_size, config.upscale_factor, "Train",
                                           transform=None)
    valid_datasets = TrainValidHRTFDataset(config.valid_hrtf_dir, config.hrtf_size, config.upscale_factor, "Valid",
                                           transform=None)
    # TODO: set up test datasets
    # test_datasets = TestHRTFDataset(config.test_lr_hrtf_dir, config.test_hr_hrtf_dir)

    # Generator all dataloader
    train_dataloader = DataLoader(train_datasets,
                                  batch_size=config.batch_size,
                                  shuffle=True,
                                  num_workers=config.num_workers,
                                  pin_memory=True,
                                  drop_last=True,
                                  persistent_workers=True)
    valid_dataloader = DataLoader(valid_datasets,
                                  batch_size=1,
                                  shuffle=False,
                                  num_workers=1,
                                  pin_memory=True,
                                  drop_last=False,
                                  persistent_workers=True)
    # test_dataloader = DataLoader(test_datasets,
    #                              batch_size=1,
    #                              shuffle=False,
    #                              num_workers=1,
    #                              pin_memory=True,
    #                              drop_last=False,
    #                              persistent_workers=True)

    # Place all data on the preprocessing data loader
    if torch.cuda.is_available() and config.ngpu > 0:
        device = torch.device(config.device_name)
        train_prefetcher = CUDAPrefetcher(train_dataloader, device)
        valid_prefetcher = CUDAPrefetcher(valid_dataloader, device)
        # test_prefetcher = CUDAPrefetcher(test_dataloader, device)
    else:
        train_prefetcher = CPUPrefetcher(train_dataloader)
        valid_prefetcher = CPUPrefetcher(valid_dataloader)

    return train_prefetcher, valid_prefetcher  # , test_prefetcher


def progress(i, batches, n, num_epochs, timed):
    """Prints progress to console

    :param i: Batch index
    :param batches: total number of batches
    :param n: Epoch number
    :param num_epochs: Total number of epochs
    :param timed: Time per batch
    """
    message = 'batch {} of {}, epoch {} of {}'.format(i, batches, n, num_epochs)
    print(f"Progress: {message}, Time per iter: {timed}")

def spectral_distortion_inner(input_spectrum, target_spectrum):
    #print(input_spectrum.shape)
    numerator = target_spectrum
    denominator = input_spectrum
    return torch.mean((20 * torch.log10(numerator / denominator)) ** 2)


def spectral_distortion_metric(generated, target, reduction='mean'):
    """Computes the mean spectral distortion metric for a 5 dimensional tensor (N x C x P x W x H)
    Where N is the batch size, C is the number of frequency bins, P is the number of panels (usually 5),
    H is height, and W is width.
    Computes the mean over every HRTF in the batch"""
    batch_size = generated.size(0)
    num_panels = generated.size(2)
    height = generated.size(3)
    width = generated.size(4)
    total_positions = num_panels * height * width

    total_sd_metric = 0
    for b in range(batch_size):
        total_all_positions = 0
        for i in range(num_panels):
            for j in range(height):
                for k in range(width):
                    average_over_frequencies = spectral_distortion_inner(generated[b, :, i, j, k],target[b, :, i, j, k])
                    total_all_positions += torch.sqrt(average_over_frequencies)
        sd_metric = total_all_positions / total_positions
        total_sd_metric += sd_metric

    if reduction == 'mean':
        output_loss = total_sd_metric / batch_size
    elif reduction == 'sum':
        output_loss = total_sd_metric
    else:
        raise RuntimeError("Please specify a valid method for reduction (either 'mean' or 'sum').")

    return output_loss

def ILD_metric_inner(input_spectrum, target_spectrum):
    input_left = input_spectrum[:128]
    input_right = input_spectrum[128:]
    target_left = target_spectrum[:128]
    target_right = target_spectrum[128:]
    input_ILD = torch.mean((20 * torch.log10(input_left / input_right)))
    target_ILD = torch.mean((20 * torch.log10(target_left / target_right)))
    return torch.abs(input_ILD-target_ILD)




def ILD_metric(generated, target, reduction="mean"):
    batch_size = generated.size(0)
    num_panels = generated.size(2)
    height = generated.size(3)
    width = generated.size(4)
    total_positions = num_panels * height * width

    total_ILD_metric = 0

    for b in range(batch_size):
        total_all_positions = 0
        for i in range(num_panels):
            for j in range(height):
                for k in range(width):
                    average_over_frequencies = ILD_metric_inner(generated[b, :, i, j, k],target[b, :, i, j, k])
                    total_all_positions += average_over_frequencies
        ILD_metric = total_all_positions / total_positions
        total_ILD_metric += ILD_metric
    if reduction == 'mean':
        output_loss = total_ILD_metric / batch_size
    elif reduction == 'sum':
        output_loss = total_ILD_metric
    else:
        raise RuntimeError("Please specify a valid method for reduction (either 'mean' or 'sum').")
    
    return output_loss




