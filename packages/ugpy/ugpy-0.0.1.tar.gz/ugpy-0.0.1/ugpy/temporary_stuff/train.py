"""
Training functions
slightly modified from deeplearning.neuromatch :
https://deeplearning.neuromatch.io/tutorials/W2D2_ConvnetsAndDlThinking/student/W2D2_Tutorial1.html#
"""
import torch
from torch import nn
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import datetime
import time
import copy
import pandas as pd
import json

import torchmetrics as tm
import torchvision.transforms as transforms

from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score


# nn.BCEWithLogitsLoss combines nn.Sigmoid and nn.BCELoss
# criterion = nn.BCEWithLogitsLoss(pos_weight = n_syn/n_trash)
# optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

def train(model, criterion, optimizer, device, train_loader, validation_loader, epochs):
    """
  Training loop
  Args:
    model: nn.module
      Neural network instance
    criterion: nn.Loss
      Criteria to calculate loss
    optimizer: torch.optim
      Type of optimiser to use
    device: string
      GPU/CUDA if available, CPU otherwise
    epochs: int
      Number of epochs
    train_loader: torch.loader
      Training Set
    validation_loader: torch.loader
      Validation set
  Returns:
    Nothing
  """

    train_loss, validation_loss = [], []
    train_acc, validation_acc = [], []
    PREDICTION_THRESHOLD = 0.5
    with tqdm(range(epochs), unit='epoch') as tepochs:
        tepochs.set_description('Training')
        for epoch in tepochs:
            # TRAIN ____________________________________________________________________________
            # set to training mode
            model.train()
            # Keeps track of the running loss
            running_loss = 0.
            correct, total = 0, 0
            for img1, img2, target in train_loader:
                img1, img2, target = img1.to(device=device, dtype=torch.float), \
                                     img2.to(device=device, dtype=torch.float), \
                                     target.to(device=device, dtype=torch.float)
                # 1. Get the model output (call the model with the data from this batch)
                output = model(img1, img2)
                # 2. Zero the gradients out (i.e. reset the gradient that the optimizer
                #                       has collected so far with optimizer.zero_grad())
                optimizer.zero_grad()
                # 3. Get the Loss (call the loss criterion with the model's output
                #                  and the target values)
                loss = criterion(output, target)
                # 4. Calculate the gradients (do the pass backwards from the loss
                #                             with loss.backward())
                loss.backward()
                # 5. Update the weights (using the training step of the optimizer,
                #                        optimizer.step())
                optimizer.step()
                # 6. Keep notes:
                #       set loss = loss.item() in the set_postfix function
                tepochs.set_postfix(loss=loss.item())
                #       Add the loss for this batch
                running_loss += loss.item()
                #       Get how many data-points processed and how many were predicted correctly
                predicted = (output > PREDICTION_THRESHOLD).to(dtype=int)
                total += target.size(0)
                correct += (predicted == target.to(dtype=int)).sum().item()

            # append the loss for this epoch
            # (running loss divided by the number of batches e.g. len(train_loader))
            train_loss.append(running_loss / len(train_loader))
            # calculate and append accuracy
            train_acc.append(correct / total)

            # EVALUATE _________________________________________________________________________
            model.eval()
            running_loss = 0.
            correct, total = 0, 0
            for img1, img2, target in validation_loader:
                img1, img2, target = img1.to(device=device, dtype=torch.float), \
                                     img2.to(device=device, dtype=torch.float), \
                                     target.to(device=device, dtype=torch.float)
                # TODO : why zeroing before getting the output ?
                # 2. Zero the gradients out (i.e. reset the gradient that the optimizer
                #                       has collected so far with optimizer.zero_grad())
                optimizer.zero_grad()
                # 1. Get the model output (call the model with the data from this batch)
                output = model(img1, img2)
                # 3. Get the Loss (call the loss criterion with the model's output
                #                  and the target values)
                loss = criterion(output, target)
                # Skip 4, 5 <-- these are for training only
                # 6. Keep notes:
                #       set loss = loss.item() in the set_postfix function
                tepochs.set_postfix(loss=loss.item())
                #       Add the loss for this batch
                running_loss += loss.item()
                #       Get how many data-points processed and how many were predicted correctly
                predicted = (output > PREDICTION_THRESHOLD).to(dtype=int)
                total += target.size(0)
                correct += (predicted == target.to(dtype=int)).sum().item()

            # append the loss for this epoch
            # (running loss divided by the number of batches e.g. len(train_loader))
            validation_loss.append(running_loss / len(validation_loader))
            # calculate and append accuracy
            validation_acc.append(correct / total)

    return train_loss, train_acc, validation_loss, validation_acc


def plot_loss_accuracy(train_loss, train_acc,
                       validation_loss, validation_acc):
    """
  Code to plot loss and accuracy

  Args:
    train_loss: list
      Log of training loss
    validation_loss: list
      Log of validation loss
    train_acc: list
      Log of training accuracy
    validation_acc: list
      Log of validation accuracy

  Returns:
    Nothing
  """
    epochs = len(train_loss)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(list(range(epochs)), train_loss, label='Training Loss')
    ax1.plot(list(range(epochs)), validation_loss, label='Validation Loss')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    ax1.set_title('Epoch vs Loss')
    ax1.legend()

    ax2.plot(list(range(epochs)), train_acc, label='Training Accuracy')
    ax2.plot(list(range(epochs)), validation_acc, label='Validation Accuracy')
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Accuracy')
    ax2.set_title('Epoch vs Accuracy')
    ax2.legend()
    fig.set_size_inches(15.5, 5.5)


def my_alexnet_train(model, dataloaders, DEVICE, criterion, optimizer, num_epochs=25, save_every=5):
    PREDICTION_THRESHOLD = 0.5
    since = time.time()

    history = {'acc': {'train': [], 'val': []},
               'loss': {'train': [], 'val': []},
               'f1': {'train': [], 'val': []},
               'cm': {'train': [], 'val': []}}

    confmat = tm.ConfusionMatrix(num_classes=2).to(DEVICE)
    best_model_wts = {'acc': [], 'loss': [], 'f1': []}
    best_acc = 0.0
    best_f1 = 0.0
    best_loss = 10 ^ 6

    augment = transforms.Compose([
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.5)
    ])
    # TODO : also add 90 deg roations to yx

    for epoch in range(num_epochs):
        print(f"Epoch {epoch}/{num_epochs - 1}\n{'-' * 10}")

        # save results every 'save_every' epochs:
        # if epoch % save_every == 1:  # and epoch>0:
        #     save_results(model, train_test_split, best_model_wts, history)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()  # Set model to evaluate mode

            running_loss = 0.0
            tp = 0
            tn = 0
            fp = 0
            fn = 0

            # Process all the batches
            i_batch = -1
            for input1, input2, labels in dataloaders[phase]:
                i_batch = i_batch + 1

                input1 = input1.to(device=DEVICE, dtype=torch.float)
                input2 = input2.to(device=DEVICE, dtype=torch.float)

                input1 = augment(input1)
                input2 = augment(input2)

                labels = labels.to(device=DEVICE, dtype=torch.float)

                # zero the parameter gradients
                optimizer.zero_grad()
                # forward
                # track grads only if in train
                with torch.set_grad_enabled(phase == 'train'):

                    # Get model outputs and calculate loss
                    outputs = model(input1, input2)
                    loss = criterion(outputs, labels)

                    # apply the learning
                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # collect loss info
                current_loss = loss.item() * labels.size(0)
                running_loss += current_loss

                # get confusion matrix and all the elements
                cm = confmat(outputs, labels.to(dtype=int))
                tp += cm[1, 1].item()
                tn += cm[0, 0].item()
                fp += cm[0, 1].item()
                fn += cm[1, 0].item()

            # average loss per item
            total = tp + tn + fp + fn
            epoch_loss = running_loss / total
            epoch_acc = (tp + tn) / total
            epoch_f1 = tp / (tp + 0.5 * (fp + fn))

            print('{} Loss: {:.4f} Acc: {:.4f} F1: {:.4f}\ntp: {:d} tn: {:d} fp: {:d} fn: {:d}\n'.format(phase,
                                                                                                         epoch_loss,
                                                                                                         epoch_acc,
                                                                                                         epoch_f1,
                                                                                                         tp, tn,
                                                                                                         fp, fn))
            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts['acc'] = copy.deepcopy(model.state_dict())

            if phase == 'val' and epoch_loss < best_loss:
                best_loss = epoch_loss
                best_model_wts['loss'] = copy.deepcopy(model.state_dict())

            if phase == 'val' and epoch_f1 > best_f1:
                best_f1 = epoch_f1
                best_model_wts['f1'] = copy.deepcopy(model.state_dict())

            history['acc'][phase].append(epoch_acc)
            history['loss'][phase].append(epoch_loss)
            history['f1'][phase].append(epoch_f1)
            history['cm'][phase].append([[tn, fp], [fn, tp]])

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}\nBest val F1: {:4f}'.format(best_acc, best_f1))

    # load best model weights
    # model.load_state_dict(best_model_wts['loss'])

    return model, best_model_wts, history


def predict(model, dataloader, DEVICE):
    """
    Predict on batch.
    DEVICE should be the same devise on which th model is.
    """
    # Disable grad torch.no_grad() impacts the autograd engine and deactivate it.
    # It will reduce memory usage and
    # speed up computations but you won’t be able to backprop
    # (which you don’t want in an eval script).
    with torch.no_grad():
        # Set model to evaluate mode: model.eval() will notify all your layers that you are in eval mode, that way,
        # batchnorm or dropout layers will work in eval mode instead of training mode.
        model.eval()
        # Process all the batches

        prob = torch.empty((1, )).to(DEVICE)
        for input1, input2 in tqdm(dataloader):
            input1 = input1.to(device=DEVICE, dtype=torch.float)
            input2 = input2.to(device=DEVICE, dtype=torch.float)
            # Get model outputs and calculate loss
            outputs = model(input1, input2)
            # convert to probability
            prob = torch.cat((prob, nn.functional.sigmoid(outputs)), 0)

    return prob


def plot_history(history):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(25, 10), dpi=120)
    ax1.plot(history['acc']['train'])
    ax1.plot(history['acc']['val'])
    ax1.set_title('Accuracy')
    ax1.legend(['train', 'val'])
    ax1.set_ylabel('Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.grid(b=True, which='major', axis='both')
    ax1.margins(0)
    ticks = ax1.set_xticks(range(0, len(history['acc']['train'])))

    ax2.plot(history['loss']['train'])
    ax2.plot(history['loss']['val'])
    ax2.set_title('Loss')
    ax2.legend(['train', 'val'])
    ax2.set_ylabel('Loss')
    ax2.set_xlabel('Epoch')
    ax2.grid(b=True, which='major', axis='both')
    ax2.margins(0)
    ticks = ax2.set_xticks(range(0, len(history['acc']['train'])))


def save_results(model, best_model_wts, history,
                 save_path='D:/Code/repos/',
                 make_it=False):
    # create folder to save:
    if make_it:
        os.makedirs(save_path)
    mydir = os.path.join(save_path, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.makedirs(mydir)
    # Save
    # split_df = pd.DataFrame.from_dict(dict([(k, pd.Series(v)) for k, v in train_test_split.items()]))
    # split_df.to_csv(os.path.join(mydir, "train_test_split.csv"))

    acc_history_df = pd.DataFrame.from_dict(dict([(k, pd.Series(v)) for k, v in history['acc'].items()]))
    acc_history_df.to_csv(os.path.join(mydir, "acc_history.csv"))

    loss_history_df = pd.DataFrame.from_dict(dict([(k, pd.Series(v)) for k, v in history['loss'].items()]))
    loss_history_df.to_csv(os.path.join(mydir, "loss_history.csv"))

    f1_history_df = pd.DataFrame.from_dict(dict([(k, pd.Series(v)) for k, v in history['f1'].items()]))
    f1_history_df.to_csv(os.path.join(mydir, "f1_history.csv"))

    torch.save(best_model_wts['acc'], os.path.join(mydir, "best_ev_acc_weights.pt"))
    torch.save(best_model_wts['loss'], os.path.join(mydir, "best_ev_loss_weights.pt"))
    torch.save(best_model_wts['f1'], os.path.join(mydir, "best_ev_f1_weights.pt"))
    torch.save(model.state_dict(), os.path.join(mydir, "current_weights.pt"))
