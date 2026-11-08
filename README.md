# NEAT Steering Model

A little AI agent learns to go to a target coördinate by steering left and right. Built using my own [barebones_neat library](https://github.com/IAmDaanE/bare-bones-neat).

---

<img width="1050" height="854" alt="Schermafbeelding 2026-11-08 110816" src="https://github.com/user-attachments/assets/424babf0-f5ed-42d5-85e4-2cac26ef6c4b" />

This repo contains the environments, the training script and also inference_ui.py where you can load the saved model and see how it performs.

The input to the neural network is the relative angle of the way the agent is facing. If it's negative the agent should turn left and vice versa. This is a very simple state and action space and use case of NEAT. I mainly built this project to test my algorithms and learn how to use the library. Therefore, when training the v1 model i made everything very simple: no new nodes or connections can spawn, the evolution is based solely on evolving weights and biases.

## Getting Started

**Requires:** Python 3.11 - 3.13

Always install the needed packages first, preferably in a venv.
```
pip install -r requirements.txt
```

### Training a Model

1. Change the hyperparameters in train.py

2. Run the training, replace the string with the path to the folder where your model will be saved.

```
python src/train.py "models/v2"
```

3. Press Ctrl + C when you are satisfied with the agents' behaviour during training to stop it and save the model

### Running the Inference

Run this command and watch what the resulting network looks like and how the model behaves. Replace the string with the path to the saved model.

```
python src/inference_ui.py "models/v1"
```

## License

This project is open-source and available under the MIT License.
