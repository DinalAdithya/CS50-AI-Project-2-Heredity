# Heredity Project

This project explores the application of Bayesian networks to model genetic inheritance. Using Python, the program calculates probabilities of traits being passed from parents to children based on predefined probabilities for genes and traits.

## Features
- Simulates genetic inheritance using Bayesian reasoning.
- Calculates the likelihood of individuals possessing specific genes or traits.
- Accounts for complex relationships between genes and their expression as traits.

## How It Works
1. **Input**: Provide a dataset that includes individuals and their parental relationships.
2. **Gene and Trait Probabilities**: Predefined probabilities determine the likelihood of inheriting genes and expressing traits.
3. **Output**: The program computes the probability distribution for each individual’s gene and trait likelihood.

## Example
For a dataset `data.csv`:
```bash
python heredity.py data.csv
```
The program will output the probability distributions for genes and traits for all individuals in the dataset.

## Dependencies
- Python 3.6+

## Project Insights
This project demonstrates how probabilistic models can be used to solve real-world problems, such as understanding genetic inheritance. It’s an excellent example of applying AI principles to biology.
