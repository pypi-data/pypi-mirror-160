import torch
import torch.nn as nn
import torch.nn.functional as F


class GanglionAsCNN(nn.Module):
    LED_CHANNELS = 4
    NUM_CLUSTERS = 1

    def __init__(self, input_len, input_freq, kernel_len, output_offset):
        """
        Args:
            input_len: length of input.
            input_freq: sampling frequency of input.
            kernel_len: length of kernel to use.
            output_offset: number of time steps after the kernel to predict.
                This is measured from the last element of the kernel, so 
                an offset of zero means that the output predicts the response
                present in the same timestep as the last elment of the kernel.
                This property is similar to the kernel pad length used when
                collecting spike snippets.
        """
        super(GanglionAsCNN, self).__init__()
        self.input_len = input_len
        self.input_freq = input_freq
        self.output_offset = output_offset
        # Input is the LED stimulus and the cell cluster's response.
        self.num_input_channels = self.LED_CHANNELS + self.NUM_CLUSTERS
        
        self.cnn1 = nn.Conv1d(
                in_channels=self.num_input_channels,
                out_channels=self.NUM_CLUSTERS,
                kernel_size=kernel_len,
                stride=1, padding=0, dilation=1)

    def forward(self, stimulus, response):
        x = torch.stack([stimulus, response], dim=1)
        x = self.cnn1(x)
        x = F.log_softmax(x, dim=1)
        return x

    def loss(self, pred, response):
        y = response[self.kernel_len + self.output_offset:]
        # TODO: how to handle the issue that this loss will prioritize 
        # no-spike responses, given that they are so numerous? Maybe we can 
        # use a weight matrix that weights the no-spike loss by the 1/ratio of
        # no-spike:spike.
        loss = F.binary_cross_entropy(pred, y)
        return loss


def train_model(model, data, epochs):
    for epoch in range(epochs):
        for i, (stimulus, response) in enumerate(data):
            pred = model(stimulus, response)
            loss = model.loss(pred, response)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            if i % 100 == 0:
                print(f'Epoch {epoch}, iteration {i}, loss {loss}')
    return model


if __name__ == '__main__':
    model = GanglionAsCNN(input_len=100, input_freq=1000,
                          kernel_len=10, output_offset=0)

    train_madel(model, data, epochs=10)
