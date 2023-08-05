from __future__ import print_function, division
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms

model_path = "model.pth" # Change as needed

device = torch.device("cpu")
model_ft = models.resnet18()
num_ftrs = model_ft.fc.in_features
model_ft.fc = nn.Linear(num_ftrs, 1)
model_ft.load_state_dict(torch.load(model_path))
model_ft = model_ft.to(device)

preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ])

def on_model(img, model = model_ft):

    model.eval()
    pic = Image.open(img)
    pic = preprocess(pic)
    pic = pic.unsqueeze(0)
    #fig = plt.figure()
    with torch.no_grad(): # not training, no need for gradients
        output_tensor = model(pic)
        #prediction = output_tensor
        prediction = torch.sigmoid(output_tensor) # Constraining output to be in range
        prediction = prediction.squeeze(1).tolist()[0]
        print(f'predicted: {prediction}')
        return (prediction)



def test():
    image_path = "test.jpg"
    on_model( image_path)
test()

