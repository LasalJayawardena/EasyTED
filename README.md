# EasyTED Library

The EasyTED Library offers a straightforward approach for calculating the syntactic tree edit distance (TED) between two sentences. Utilizing advanced Natural Language Processing (NLP) techniques, EasyTED parses sentences to their constituency trees, facilitating in-depth linguistic analyses with minimal setup. Beyond calculating distances, it features tree visualization and transformation tools, making it an indispensable resource for linguistics research and NLP applications.

## Features

- **Tree Edit Distance Calculation:** Compute the TED between any two sentences.
- **Constituency Tree Parsing:** Transform sentences into their underlying constituency tree structures.
- **Tree Visualization:** Generate and save visual representations of constituency trees.
- **Bracketed String Transformation:** Convert constituency trees into a bracketed string format for easy comparison and analysis.
- **Simple Integration:** Designed to seamlessly integrate with broader NLP and linguistic analysis workflows.

## Installation

Install EasyTED directly from the Python Package Index (PyPI) using pip:

```bash
pip install easyted
```

## High-Level Usage

### Calculating Full Tree Edit Distance
```python
from easyted.ted import TreeEditDistanceCalculator

# Initialize the calculator
calculator = TreeEditDistanceCalculator()

# Calculate the tree edit distance between two sentences
distance = calculator.calculate_ted("This is a test.", "This is only a test.")
print(f"Tree Edit Distance: {distance}")
```

### Calculating N Tree Edit Distance
```python
from easyted.ted import TreeEditDistanceCalculator

# Initialize the calculator
calculator = TreeEditDistanceCalculator()

# Calculate the tree edit distance between two sentences for first 3 layers
distance = calculator.calculate_ted("This is a test.", "This is only a test.", 3)
print(f"Tree Edit Distance for first 3 layers: {distance}")

# Calculate the tree edit distance between two sentences considering only the first 3 layers
distance_first_3 = calculator.calculate_ted("This is a test.", "This is only a test.", 3)
print(f"Tree Edit Distance (First 3 Layers): {distance_first_3}")
```


### Visualizing Constituency Trees
```python
# Draw and save the constituency tree to a file
calculator.draw_and_save_tree("A visualization of a constituency tree.", "tree_visualization.ps")
```


## Main Features and Methods

The `TreeEditDistanceCalculator` class provides a suite of methods for parsing, manipulating, and visualizing constituency trees, as well as calculating the tree edit distance between sentences. Here's a breakdown of its core functionalities:

### Initialization
```python
calculator = TreeEditDistanceCalculator(language='en')
```
Initializes the calculator with a specified language for the NLP pipeline. The default language is English ('en').

### Parsing Sentences into Constituency Trees
```python
tree = calculator.get_constituency_tree("This is a test sentence.")
```
Parses a sentence and returns its constituency tree, enabling further linguistic analysis.

### Simplifying Tree Representations
```python
cleaned_string = calculator.remove_non_terminal_labels("(S (NP This) (VP is))")
Removes non-terminal labels from a tree string, simplifying its structure for comparison or analysis.
```

### Converting Trees to Bracketed String Format
```python
bracket_string = calculator.nltk_tree_to_bracket_string(tree)
```
Converts a constituency tree into a bracketed string format, facilitating easy comparison and visualization.


### Limiting Tree Depth
```python
limited_bracket_string = calculator.nltk_tree_to_n_bracket_string(tree, max_depth=3)
```
Converts a tree to a bracketed string while limiting its depth, useful for focusing on higher-level structural similarities or differences.

### Visualizing and Saving Trees
```python
calculator.draw_and_save_tree("This is a test sentence.", "tree_output.ps")
```
Draws the constituency tree of a sentence and saves the visualization to a file, perfect for presentations or further analysis.

### Calculating Tree Edit Distance
```python
distance = calculator.calculate_ted("Sentence one.", "Sentence two.", depth='full')
```
Calculates the Tree Edit Distance (TED) between two sentences. The depth can be 'full' for complete trees or an integer for a specific depth, offering flexibility in analyzing tree similarities.


## Requirements
- Python 3.6+
- NLTK
- stanza
- APTED

## Contributing

We welcome contributions to the EasyTED Library! If you have suggestions for improvements or wish to contribute new features, please feel free to open an issue or submit a pull request. Ensure your contributions adhere to the coding standards set forth by the project.

## License
EasyTED is licensed under the MIT License. See the LICENSE file in the project repository for more details.

## Acknowledgments
Thanks to NLTK for providing the foundational tools for working with natural language data.
Appreciation to the Stanford NLP Group for the development of the stanza library, which powers the linguistic analysis capabilities of EasyTED.
Gratitude to the developers of the APTED algorithm for their work on efficient tree edit distance computation.

## Citations

If you use EasyTED in your research, please consider citing the following:

```bibtex
@inproceedings{qi2020stanza,
    title={Stanza: A {Python} Natural Language Processing Toolkit for Many Human Languages},
    author={Qi, Peng and Zhang, Yuhao and Zhang, Yuhui and Bolton, Jason and Manning, Christopher D.},
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics: System Demonstrations",
    year={2020}
}

@article{pawlik2016tree,
    title={Tree edit distance: Robust and memory- efficient},
    author={Pawlik, Mateusz and Augsten, Nikolaus},
    journal={Information Systems},
    volume={56},
    year={2016}
}

@article{pawlik2015efficient,
    title={Efficient Computation of the Tree Edit Distance},
    author={Pawlik, Mateusz and Augsten, Nikolaus},
    journal={ACM Transactions on Database Systems (TODS)},
    volume={40},
    number={1},
    year={2015}
}

@article{pawlik2011rted,
    title={RTED: A Robust Algorithm for the Tree Edit Distance},
    author={Pawlik, Mateusz and Augsten, Nikolaus},
    journal={PVLDB},
    volume={5},
    number={4},
    year={2011}
}
