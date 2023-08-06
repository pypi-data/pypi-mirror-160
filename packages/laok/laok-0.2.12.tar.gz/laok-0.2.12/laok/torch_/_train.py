#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/4/21 21:28:54

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import torch
import torch.nn as nn
#===============================================================================
'''         
'''
#===============================================================================


def train_class_model(model, train_loader, optimizer, num_epochs):
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Train the model
    total_step = len(train_loader)
    for epoch in range(num_epochs):
        for i ,(images, labels) in enumerate(train_loader):
            images = images.to(device)
            labels = labels.to(device)

            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Backward and optimizer
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i+1) % 100 == 0:
                print(f'Epoch: [{epoch+1}/{num_epochs}], Step: [{i+1}/{total_step}], Loss: {loss.item()}')


def val_class_model(model, loader, device=None):
    from . import get_device
    if device is None:
        device = get_device()
    from tqdm import tqdm
    model.eval()  # eval mode(batch norm uses moving mean/variance instead of mini-batch mean/variance)
    correct = 0
    total = 0
    img_total = 0
    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)
            img_total += len(images)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        print(f'accuracy of the model on the {img_total} test images: {100 * correct / total} %')