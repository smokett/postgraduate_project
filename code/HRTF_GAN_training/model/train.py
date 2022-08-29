import scipy

from model.util import *
from model.model import *

import torch.backends.cudnn as cudnn
import torch.optim as optim
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import time

from model.custom_conv import CubeSpherePadding2D, CubeSphereConv2D

from plot import plot_panel, plot_losses, plot_magnitude_spectrums, plot_SD_node, plot_SD_frequency
import sofar as sf

def reset_fc(m) -> None:
    for name, layer in m.named_children():
        if name == 'classifier':
            for module in layer.modules():
                if isinstance(module, nn.Linear):
                    torch.nn.init.xavier_uniform_(module.weight.data)

def reset_output(m) -> None:
    for name, layer in m.named_children():
        if name == 'conv_block3':
            for module in layer.modules():
                if isinstance(module, CubeSphereConv2D):
                    nn.init.kaiming_normal_(module.equatorial_weight)
                    nn.init.kaiming_normal_(module.polar_weight)
                    if module.equatorial_bias is not None:
                        nn.init.constant_(module.equatorial_bias, 0)
                        nn.init.constant_(module.polar_bias, 0)


def train(config, train_prefetcher, overwrite=True):
    """ Train the generator and discriminator models

    :param config: Config object containing model hyperparameters
    :param train_prefetcher: prefetcher for training data
    :param overwrite: whether to overwrite existing model outputs
    """
    # Calculate how many batches of data are in each Epoch
    batches = len(train_prefetcher)

    # get list of positive frequencies of HRTF for plotting magnitude spectrum
    hrir_samplerate = 48000.0
    all_freqs = scipy.fft.fftfreq(256, 1 / hrir_samplerate)
    pos_freqs = all_freqs[all_freqs >= 0]

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
    optD = optim.Adam(netD.parameters(), lr=lr_dis, betas=(beta1, beta2))
    optG = optim.Adam(netG.parameters(), lr=lr_gen, betas=(beta1, beta2))

    # Define loss functions
    adversarial_criterion = nn.BCEWithLogitsLoss()
    #content_criterion = nn.MSELoss()
    content_criterion = spectral_distortion_metric
    content_criterion_1 = ILD_metric

    if not overwrite:
        netG.load_state_dict(torch.load(f"{path}/Gen_SD_350.pt"))
        netD.load_state_dict(torch.load(f"{path}/Disc_SD_350.pt"))
        netD.apply(reset_fc)
        netG.apply(reset_output)

    train_losses_G = []
    train_losses_G_adversarial = []
    train_losses_G_content = []
    train_losses_D = []
    train_losses_D_hr = []
    train_losses_D_sr = []

    for epoch in range(num_epochs):
        times = []
        train_loss_G = 0.
        train_loss_G_adversarial = 0.
        train_loss_G_content = 0.
        train_loss_D = 0.
        train_loss_D_hr = 0.
        train_loss_D_sr = 0.

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
            lr = batch_data["lr"].to(device=device, memory_format=torch.contiguous_format,
                                     non_blocking=True, dtype=torch.float)
            hr = batch_data["hr"].to(device=device, memory_format=torch.contiguous_format,
                                     non_blocking=True, dtype=torch.float)

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
            train_loss_D += loss_D.item()
            train_loss_D_hr += loss_D_hr.item()
            train_loss_D_sr += loss_D_sr.item()

            # Update D
            optD.step()

            # Generator training
            if batch_index % int(critic_iters) == 0:
                # Initialize generator model gradients
                netG.zero_grad()
                label.fill_(1.)
                # Calculate adversarial loss
                output = netD(sr).view(-1)

                #content_loss_G = config.content_weight * content_criterion(sr, hr)
                content_loss_G = config.content_weight * (content_criterion(sr, hr) + content_criterion_1(sr, hr))

                adversarial_loss_G = config.adversarial_weight * adversarial_criterion(output, label)
                # Calculate the generator total loss value and backprop
                loss_G = content_loss_G + adversarial_loss_G
                loss_G.backward()
                
                train_loss_G += loss_G.item()
                train_loss_G_adversarial += adversarial_loss_G.item()
                train_loss_G_content += content_loss_G.item()

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
                    torch.save(netG.state_dict(), f'{path}/Gen_SD_350_250.pt')
                    torch.save(netD.state_dict(), f'{path}/Disc_SD_350_250.pt')

                    plot_panel(lr, sr, hr, batch_index, epoch, path, ncol=4, freq_index=10)

                    magnitudes_real = torch.permute(hr.detach().cpu()[0], (1, 2, 3, 0))
                    magnitudes_interpolated = torch.permute(sr.detach().cpu()[0], (1, 2, 3, 0))
                    #plot_SD_node(sr, hr, epoch, path)
                    #plot_SD_frequency(sr, hr, epoch, path)
                    plot_magnitude_spectrums(pos_freqs, magnitudes_real[:,:,:,:128], magnitudes_interpolated[:,:,:,:128], epoch, path)
                    progress(batch_index, batches, epoch, num_epochs,
                             timed=np.mean(times))
                    times = []


            # Preload the next batch of data
            batch_data = train_prefetcher.next()

            # After training a batch of data, add 1 to the number of data batches to ensure that the
            # terminal print data normally
            batch_index += 1
        


        train_losses_D.append(train_loss_D / len(train_prefetcher))
        train_losses_D_hr.append(train_loss_D_hr / len(train_prefetcher))
        train_losses_D_sr.append(train_loss_D_sr / len(train_prefetcher))
        train_losses_G.append(train_loss_G / len(train_prefetcher))
        train_losses_G_adversarial.append(train_loss_G_adversarial / len(train_prefetcher))
        train_losses_G_content.append(train_loss_G_content / len(train_prefetcher))
        print(f"Average epoch loss, discriminator: {train_losses_D[-1]}, generator: {train_losses_G[-1]}")
        print(f"Average epoch loss, D_real: {train_losses_D_hr[-1]}, D_fake: {train_losses_D_sr[-1]}")
        print(f"Average epoch loss, G_adv: {train_losses_G_adversarial[-1]}, train_losses_G_content: {train_losses_G_content[-1]}")

    plot_losses(train_losses_D, train_losses_G,
                label_1='Discriminator loss', label_2='Generator loss',
                path=path, filename='loss_curves')
    plot_losses(train_losses_D_hr, train_losses_D_sr,
                label_1='Discriminator loss, real', label_2='Discriminator loss, fake',
                path=path, filename='loss_curves_D')
    plot_losses(train_losses_G_adversarial, train_losses_G_content,
                label_1='Generator loss, adversarial', label_2='Generator loss, content',
                path=path, filename='loss_curves_G')

    print("TRAINING FINISHED")


def valid(config, valid_prefetcher):
    hrir_samplerate = 48000.0
    all_freqs = scipy.fft.fftfreq(256, 1 / hrir_samplerate)
    pos_freqs = all_freqs[all_freqs >= 0]
    torch.cuda.empty_cache()
    ngpu = config.ngpu
    path = config.path
    device = torch.device(config.device_name if (torch.cuda.is_available() and ngpu > 0) else "cpu")
    cudnn.benchmark = True
    netG = Generator().to(device)
    if ('cuda' in str(device)) and (ngpu > 1):
        netG = nn.DataParallel(netG, list(range(ngpu))).to(device)
    netG.load_state_dict(torch.load(f"{path}/Gen_1000_250_5.pt"))
    netG.eval()
    valid_prefetcher.reset()
    index = 1
    f = open("avg_score.txt","w")
    with torch.no_grad():
        batch_data = valid_prefetcher.next()
        output_list = []
        while batch_data is not None:
            lr = batch_data["lr"].to(device=device, memory_format=torch.contiguous_format, non_blocking=True, dtype=torch.float)
            hr = batch_data["hr"].to(device=device, memory_format=torch.contiguous_format, non_blocking=True, dtype=torch.float)
            sr = netG(lr)
            magnitudes_real = torch.permute(hr.detach().cpu()[0], (1, 2, 3, 0))
            magnitudes_interpolated = torch.permute(sr.detach().cpu()[0], (1, 2, 3, 0))
            #plot_magnitude_spectrums(pos_freqs,magnitudes_real[:,:,:,:128], magnitudes_interpolated[:,:,:,:128],"left",str(index),path,log_scale_magnitudes=True)
            plot_SD_node(sr,hr,index,path,f)
            output_list.append(sr)
            batch_data = valid_prefetcher.next()
            index += 1
        
        for i in range(len(output_list)):
            output_list[i] = torch.permute(torch.squeeze(output_list[i]),(1,2,3,0))

    f.close()
    sofa = sf.read_sofa("HRIR_gan_1280.sofa")
    
    for d in range(0,len(output_list)):
    #for d in range(0,len(output_list),2):
        output_list[d] = output_list[d].cpu().detach()
        #output_list[d+1] = output_list[d+1].cpu().detach()
        left = output_list[d][:,:,:,:128]
        right = output_list[d][:,:,:,128:]
        #left = output_list[d]
        #right = output_list[d+1]

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

        # when saving real data, exchange the first four panels and flip the last sky panel

        temp = total_hrir[0:1024]
        tmp1 = temp[0:512]
        tmp2 = temp[512:]
        temp = np.concatenate((tmp2,tmp1),0)

        temp_1 = total_hrir[1024:]
        temp_1 = np.flip(temp_1,0)

        total_hrir = np.concatenate((temp, temp_1), axis=0)

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
        sf.write_sofa("valid_sofa//"+str(d)+"_test.sofa", sofa)
