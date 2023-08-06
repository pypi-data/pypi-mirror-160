
from __future__ import print_function, division
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from importlib import resources


print("scuffed documentation")
print("model.eval(images) where images = an array of image paths for model to rate")


def eval(images):
    
    model_path = "p_model.pth" # Change as needed
    
    device = torch.device("cpu")
    model_ft = models.resnet18()
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Linear(num_ftrs, 1)
    with resources.path("exposuremodelf", model_path) as pp:
        model_ft.load_state_dict(torch.load(pp))
    model_ft = model_ft.to(device)

    preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
        ])


    model_ft.eval()
    predictions = []
    for img in images:
        pic = Image.open(img)
        pic = preprocess(pic)
        pic = pic.unsqueeze(0)
        #fig = plt.figure()
        with torch.no_grad(): # not training, no need for gradients
            output_tensor = model_ft(pic)
            #prediction = output_tensor
            prediction = torch.sigmoid(output_tensor) # Constraining output to be in range
            prediction = prediction.squeeze(1).tolist()[0]
            predictions.append(predictions)
            print(f'predicted: {prediction}')
            if (prediction > 0.7):
                print("image is good")
            else:
                print("image does not meet quality requirments")
    return (predictions)
  

def test():
    image_path = "test.jpg"
    eval( [image_path])



