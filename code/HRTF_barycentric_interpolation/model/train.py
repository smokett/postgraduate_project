from model.util import *
from model.model import *

import torch.backends.cudnn as cudnn
import torch.optim as optim
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import time
import sofar as sf
import scipy.fftpack

from plot import plot_panel, plot_losses


def train(config, train_prefetcher, overwrite=True):
    """ Train the generator and discriminator models

    :param config: Config object containing model hyperparameters
    :param train_prefetcher: prefetcher for training data
    :param overwrite: whether to overwrite existing model outputs
    """
    # Calculate how many batches of data are in each Epoch
    batches = len(train_prefetcher)

    # Assign torch device
    ngpu = config.ngpu
    path = config.path
    device = torch.device(config.device_name if (
            torch.cuda.is_available() and ngpu > 0) else "cpu")
    print(f'Using {ngpu} GPUs')
    print(device, " will be used.\n")
    cudnn.benchmark = True

    # Get train params
    batch_size, beta1, beta2, num_epochs, lr_gen, lr_dis, critic_iters = config.get_train_params()

    # Define Generator network and transfer to CUDA
    netG = Generator().to(device)
    netD = Discriminator().to(device)
    if ('cuda' in str(device)) and (ngpu > 1):
        netD = (nn.DataParallel(netD, list(range(ngpu)))).to(device)
        netG = nn.DataParallel(netG, list(range(ngpu))).to(device)

    # Define optimizers
    optD = optim.SGD(netD.parameters(), lr=lr_dis)
    optG = optim.SGD(netG.parameters(), lr=lr_gen)

    # Define loss functions
    adversarial_criterion = nn.BCEWithLogitsLoss()
    content_criterion = nn.MSELoss()

    if not overwrite:
        netG.load_state_dict(torch.load(f"{path}/Gen.pt"))
        netD.load_state_dict(torch.load(f"{path}/Disc.pt"))

    train_losses_G = []
    train_losses_D = []

    for epoch in range(num_epochs):
        times = []
        train_loss_D = 0.
        train_loss_G = 0.

        # Initialize the number of data batches to print logs on the terminal
        batch_index = 0

        # Initialize the data loader and load the first batch of data
        train_prefetcher.reset()
        batch_data = train_prefetcher.next()

        while batch_data is not None:
            if ('cuda' in str(device)) and (ngpu > 1):
                start_overall = torch.cuda.Event(enable_timing=True)
                end_overall = torch.cuda.Event(enable_timing=True)
                start_overall.record()
            else:
                start_overall = time.time()

            # Transfer in-memory data to CUDA devices to speed up training
            lr = batch_data["lr"].to(device=device, memory_format=torch.contiguous_format, non_blocking=True)
            hr = batch_data["hr"].to(device=device, memory_format=torch.contiguous_format, non_blocking=True)

            # Discriminator Training
            # Initialize the discriminator model gradients
            netD.zero_grad()

            # Use the generator model to generate fake samples
            sr = netG(lr)

            # Calculate the classification score of the discriminator model for real samples
            label = torch.full((batch_size, ), 1., dtype=hr.dtype, device=device)
            output = netD(hr).view(-1)
            loss_D_hr = adversarial_criterion(output, label)
            loss_D_hr.backward()

            # train on SR hrtfs
            label.fill_(0.)
            output = netD(sr.detach()).view(-1)
            loss_D_sr = adversarial_criterion(output, label)
            loss_D_sr.backward()

            # Compute the discriminator loss
            loss_D = loss_D_hr + loss_D_sr
            train_loss_D += loss_D

            # Update D
            optD.step()

            # Generator training
            if batch_index % int(critic_iters) == 0:
                # Initialize generator model gradients
                netG.zero_grad()
                label.fill_(1.)
                # Calculate adversarial loss
                output = netD(sr).view(-1)

                content_loss_G = config.content_weight * content_criterion(sr, hr)
                adversarial_loss_G = config.adversarial_weight * adversarial_criterion(output, label)
                # Calculate the generator total loss value and backprop
                loss_G = content_loss_G + adversarial_loss_G
                loss_G.backward()
                train_loss_G += loss_G

                optG.step()

            if ('cuda' in str(device)) and (ngpu > 1):
                end_overall.record()
                torch.cuda.synchronize()
                times.append(start_overall.elapsed_time(end_overall))
            else:
                end_overall = time.time()
                times.append(end_overall - start_overall)

            # Every 0th batch log useful metrics
            if batch_index == 0:
                with torch.no_grad():
                    torch.save(netG.state_dict(), f'{path}/Gen.pt')
                    torch.save(netD.state_dict(), f'{path}/Disc.pt')

                    plot_panel(lr, sr, hr, batch_index, epoch, path, ncol=4, freq_index=10)
                    progress(batch_index, batches, epoch, num_epochs,
                             timed=np.mean(times))
                    times = []

            # Preload the next batch of data
            batch_data = train_prefetcher.next()

            # After training a batch of data, add 1 to the number of data batches to ensure that the
            # terminal print data normally
            batch_index += 1

        train_losses_D.append(train_loss_D / len(train_prefetcher))
        train_losses_G.append(train_loss_G / len(train_prefetcher))
        print(f"Average epoch loss, discriminator: {train_losses_D[-1]}, generator: {train_losses_G[-1]}")

    plot_losses(train_losses_D, train_losses_G, path)

    print("TRAINING FINISHED")

def valid(config, valid_prefetcher):
    torch.cuda.empty_cache()
    ngpu = config.ngpu
    path = config.path
    device = torch.device(config.device_name if (torch.cuda.is_available() and ngpu > 0) else "cpu")
    cudnn.benchmark = True
    netG = Generator().to(device)
    if ('cuda' in str(device)) and (ngpu > 1):
        netG = nn.DataParallel(netG, list(range(ngpu))).to(device)
    netG.load_state_dict(torch.load(f"{path}/Gen.pt"))
    netG.eval()
    valid_prefetcher.reset()
    batch_data = valid_prefetcher.next()
    output_list = []
    while batch_data is not None:
        lr = batch_data["lr"].to(device=device, memory_format=torch.contiguous_format, non_blocking=True)
        hr = batch_data["hr"].to(device=device, memory_format=torch.contiguous_format, non_blocking=True)
        sr = netG(lr)
        output_list.append(sr)
        batch_data = valid_prefetcher.next()
    
    for i in range(len(output_list)):
        output_list[i] = torch.permute(torch.squeeze(output_list[i]),(1,2,0))
        output_list[i] = torch.reshape(output_list[i],(output_list[i].shape[0], output_list[i].shape[1], 128, 5))
        output_list[i] = torch.permute(output_list[i],(3,0,1,2))
    
    print(output_list[0].shape)
    
    sofa = sf.read_sofa("HRIR_gan_1280.sofa")
    
    for d in range(0,len(output_list),2):
        output_list[d] = output_list[d].cpu().detach()
        output_list[d+1] = output_list[d+1].cpu().detach()
        left = output_list[d]
        right = output_list[d+1]
        left = left[:,2:-2,2:-2,:]
        right = right[:,2:-2,2:-2,:]

        if d == 0:
            print(left)

        left_hrir = np.zeros((left.shape[0],left.shape[1],left.shape[2],left.shape[3]*2))
        right_hrir = left_hrir.copy()

        for i in range(left.shape[0]):
            for j in range(left.shape[1]):
                for k in range(left.shape[2]):
                    left_hrir[i,j,k] = scipy.fft.irfft(np.concatenate((np.array([1.0]),left[i,j,k])))
                    right_hrir[i,j,k] = scipy.fft.irfft(np.concatenate((np.array([1.0]),right[i,j,k])))

        total_hrir = np.zeros((left_hrir.shape[0]*left_hrir.shape[1]*left_hrir.shape[2],2,left_hrir.shape[3]))
        count = 0
        for i in range(left_hrir.shape[0]):
            for j in range(left_hrir.shape[1]):
                for k in range(left_hrir.shape[2]):
                    total_hrir[count,0] = left_hrir[i,j,k]
                    total_hrir[count,1] = right_hrir[i,j,k]
                    count += 1

        sofa.Data_IR = total_hrir
        total_SourcePosition = np.zeros((total_hrir.shape[0],3))
        coordinates_file = open("generated_coordinates_degree.txt","r")
        count = 0
        for line in coordinates_file:
            line = line.strip()
            total_SourcePosition[count,0] = float(line.split(" ")[1])
            total_SourcePosition[count,1] = float(line.split(" ")[0])
            total_SourcePosition[count,2] = 1.0
            count += 1
        sofa.SourcePosition = total_SourcePosition
        sf.write_sofa("valid_sofa//"+str(d//2)+"_test.sofa", sofa)


