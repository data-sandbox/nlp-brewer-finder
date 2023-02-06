import math
import typer
from pathlib import Path
from spacy.util import get_words_and_spaces
from spacy.tokens import Doc, DocBin
import spacy
import json
import random
random.seed(11)


def create_docbin(data):
    nlp = spacy.blank("en")
    db = DocBin()
    for text, annotations in data:
        doc = nlp(text)
        ents = []
        for start, end, label in annotations:
            span = doc.char_span(start, end, label=label)
            if span:
                ents.append(span)
        if ents != []:
            doc.ents = ents
        db.add(doc)
    return db


def main(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    train_path: Path = typer.Argument(..., dir_okay=False),
    valid_path: Path = typer.Argument(..., dir_okay=False)
):
    print(f"Starting preprocessing!")
    labeled_data = []
    with open(input_path) as file:
        lines = file.readlines()
        for train_data in lines:
            data = json.loads(train_data)
            # if len(data['label']) == 0:
            #     continue
            labeled_data.append((data['text'], data['label']))

    # Split the labeled data into training and evaluation sets
    random.shuffle(labeled_data)
    split = 0.8
    n = math.floor(len(labeled_data) * split)
    train_data = labeled_data[:n]
    valid_data = labeled_data[n:]

    # Inspect split point
    if train_data[-1] == valid_data[0]:
        raise IndexError(
            'Integer rounding error. Overlap between training and eval data')

    train_db = create_docbin(train_data)
    valid_db = create_docbin(valid_data)

    # convert to spacy format
    train_db.to_disk(train_path)
    print(f"Processed {len(train_db)} documents: {train_path.name}")
    valid_db.to_disk(valid_path)
    print(f"Processed {len(valid_db)} documents: {valid_path.name}")


if __name__ == "__main__":
    typer.run(main)
