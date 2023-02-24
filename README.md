<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Brewery Finder NER

Capstone Project for The Data Incubator (TDI) Fellowship. This project identifies brewery offerings from webscraped Tripadvisor user reviews and displays the results in an interactive [Brewery Finder](https://brewery-finder.streamlit.app) app, designed to help users find the best brewery for them by streamlining the decision process in one central interface.

The goal of this project is to demonstrate various data science skills including webscraping, data cleaning, data processing, exploratory analysis, NLP model development, and app deployment. On the NLP side, two models are compared; a simple rule-based model and a spaCy Named Entity Recognition (NER) model.

What follows is the spaCy auto-generated docs describing the modeling workflows and commands.

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[spaCy projects documentation](https://spacy.io/usage/projects).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `preprocess` | Convert the data to spaCy's binary format |
| `patternmod` | Generate a named entity recognition model based on rules. |
| `train` | Train a named entity recognition model |
| `evaluate` | Evaluate the model and export metrics |
| `package` | Package the trained model so it can be installed |
| `show-stats` | Show the statistics that compares both models. |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `preprocess` &rarr; `patternmod` &rarr; `train` &rarr; `evaluate` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| [`assets/train.jsonl`](assets/train.jsonl) | Local | JSONL-formatted training data exported from Doccano |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->