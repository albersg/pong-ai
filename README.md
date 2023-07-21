# Pong with DQN AI

Welcome to Pong with DQN AI! This project combines the classic game Pong with the power of Deep Q-Networks (DQN) to create an exciting and challenging gaming experience. The game allows two human players to play against each other or test their skills against an intelligent AI opponent trained using Reinforcement Learning techniques.

## Table of Contents

- [Introduction](#introduction)
- [Gameplay](#gameplay)
- [Features](#features)
- [Usage](#usage)
- [Training the AI](#training-the-ai)
- [Playing against the AI](#playing-against-the-ai)
- [License](#license)

## Introduction

Pong with DQN AI is a Python-based implementation of the classic Pong game using the popular Pygame library. The game offers both traditional player-vs-player gameplay and an AI mode, where an intelligent agent powered by DQN can challenge players. The AI agent learns to play Pong through reinforcement learning, achieving progressively better scores as it gains experience.

## Gameplay

Pong is a simple 2D table tennis-like game where two paddles control the vertical movement of a ball. The objective is to prevent the ball from hitting the edges of the screen while attempting to make the ball pass the opponent's paddle. The player who allows the ball to pass their paddle loses a point. The game continues until one player reaches the pre-defined score limit.

## Features

- Classic Pong gameplay with smooth controls and interactive visuals.
- Two-player mode for engaging head-to-head matches.
- AI opponent powered by Deep Q-Networks for a challenging single-player experience.
- Reinforcement Learning training environment with customizable parameters.
- Experience Replay to improve AI training efficiency and performance.

## Usage

To play Pong with a human opponent, simply run the `pong.py` script:

Use the following controls to move the paddles:

- Player 1 (Left paddle): W (Up), S (Down)
- Player 2 (Right paddle): Up Arrow (Up), Down Arrow (Down)

## Training the AI

To train the AI agent using the DQN algorithm, use the `train.py` script:

The training process can be customized through various parameters such as the number of episodes, learning rate, and exploration rate. Feel free to experiment and fine-tune these values to achieve better AI performance.

## Playing against the AI

Once you have a trained AI model, you can play against the AI using the `pong_ai.py` script:

Test your skills against the AI and see if you can outsmart the intelligent opponent!

## License

This project is licensed under the [MIT License](LICENSE), allowing you to modify and distribute the code while providing credit to the original authors.

Enjoy Pong with DQN AI, and have fun challenging your friends or the AI-powered opponent!
