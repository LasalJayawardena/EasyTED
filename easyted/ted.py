import re
from typing import Union
import stanza
import nltk
from nltk.tree import Tree as NLTKTree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
from apted import APTED, Config
from apted.helpers import Tree as APTEDTree

class TreeEditDistanceCalculator:
    """
    A class for calculating the Tree Edit Distance (TED) between sentences, along with utilities for parsing
    and visualizing constituency trees.
    
    Attributes:
    language (str): The language configuration for the stanza NLP pipeline.
    """

    def __init__(self, language: str = 'en'):
        """
        Initializes the TreeEditDistanceCalculator with a specified language for the NLP pipeline.
        
        Args:
        language (str): The language code to be used by the stanza pipeline for parsing sentences.
        """
        self.nlp = stanza.Pipeline(lang=language, processors='tokenize,pos,constituency', use_gpu=True)
    
    def get_constituency_tree(self, sentence: str) -> NLTKTree:
        """
        Parses a sentence and returns its constituency tree.
        
        Args:
        sentence (str): The sentence to parse.
        
        Returns:
        NLTKTree: The constituency tree of the parsed sentence.
        """
        doc = self.nlp(sentence)
        nltk_tree = doc.sentences[0].constituency
        return nltk_tree

    def remove_non_terminal_labels(self, tree_string: str) -> str:
        """
        Removes non-terminal labels from a tree string to simplify comparison.
        
        Args:
        tree_string (str): The string representation of a tree.
        
        Returns:
        str: A cleaned tree string without non-terminal labels.
        """
        cleaned_tree_string = re.sub(r'\([A-Z$]+ ', '(', tree_string)
        cleaned_tree_string = re.sub(r'\s+', '', cleaned_tree_string)
        return cleaned_tree_string

    def nltk_tree_to_bracket_string(self, tree: NLTKTree) -> str:
        """
        Converts an NLTK tree to a full bracket string representation.
        
        Args:
        tree (NLTKTree): The NLTK tree to convert.
        
        Returns:
        str: The bracket string representation of the tree.
        """
        tree_string = str(tree)
        cleaned_tree_string = self.remove_non_terminal_labels(tree_string)
        bracket_string = cleaned_tree_string.replace(")", "}").replace("(", "{")
        return bracket_string
    
    def nltk_tree_to_n_bracket_string(self, tree, max_depth=None, current_depth=0):
        """
        Converts an NLTK tree to a bracket string with an optional depth limitation.
        
        Args:
        tree: The NLTK tree to convert.
        max_depth (Optional[int]): The maximum depth to include in the conversion.
        current_depth (int): The current depth in the recursion (used internally).
        
        Returns:
        str: The bracket string representation of the tree with limited depth.
        """
        if max_depth is not None and current_depth > max_depth or not tree:
            return ""

        tree_string = "(" + tree.label() + " "
        if tree.height() > 2:
            for child in tree:
                tree_string += self.nltk_tree_to_n_bracket_string(child, max_depth, current_depth + 1)
        else:
            tree_string += " ".join(tree.leaves())
        tree_string += ")"
        return tree_string
    
    def clean_string(self, tree_string: str) -> str:
        """
        Cleans and transforms a tree string to a specific bracket format.
        
        Args:
        tree_string (str): The tree string to clean.
        
        Returns:
        str: The cleaned and formatted tree string.
        """
        cleaned_tree_string = self.remove_non_terminal_labels(tree_string)
        bracket_string = cleaned_tree_string.replace(")", "}").replace("(", "{")
        return bracket_string

    def get_bracketed_string(self, sentence: str) -> str:
        """
        Gets the bracket string representation of a sentence's constituency tree.
        
        Args:
        sentence (str): The sentence to process.
        
        Returns:
        str: The bracket string representation of the constituency tree.
        """
        tree = self.get_constituency_tree(sentence)
        return self.nltk_tree_to_bracket_string(tree)

    def get_nltk_tree(self, sentence: str) -> NLTKTree:
        """
        Gets the NLTK tree representation of a sentence's constituency tree.
        
        Args:
        sentence (str): The sentence to process.
        
        Returns:
        NLTKTree: The NLTK tree of the constituency tree.
        """
        return self.get_constituency_tree(sentence)

    def draw_and_save_tree(self, sentence: str, filepath: str):
        """
        Draws the constituency tree of a sentence and saves it to a file.
        
        Args:
        sentence (str): The sentence to process.
        filepath (str): The path to the file where the tree visualization will be saved.
        """
        nltk_tree = self.get_constituency_tree(sentence)
        t = NLTKTree.fromstring(str(nltk_tree))
        cf = CanvasFrame()
        tc = TreeWidget(cf.canvas(), t)
        cf.add_widget(tc, 10, 10)
        cf.print_to_file(filepath)
        cf.destroy()

    def calculate_ted(self, sent1: str, sent2: str, depth: Union[str, int] = 'full') -> int:
        """
        Calculates the Tree Edit Distance (TED) between two sentences with an optional tree depth.
        
        Args:
        sent1 (str): The first sentence.
        sent2 (str): The second sentence.
        depth (Union[str, int]): The depth for the tree comparison, 'full' for complete trees or an integer for a specific depth.
        
        Returns:
        int: The computed edit distance.
        """
        if not isinstance(sent1, str) or not isinstance(sent2, str):
            raise TypeError("Both sent1 and sent2 must be strings.")
        if not isinstance(depth, (str, int)) or (isinstance(depth, int) and depth < 0):
            raise TypeError("Depth must be 'full' or a non-negative integer.")
        
        cons_tree1 = self.get_constituency_tree(sent1)
        cons_tree2 = self.get_constituency_tree(sent2)
        
        nltk_tree1 = NLTKTree.fromstring(str(cons_tree1))
        nltk_tree2 = NLTKTree.fromstring(str(cons_tree2))
        
        max_depth = None if depth == 'full' else depth

        tree_string1 = self.nltk_tree_to_bracket_string(nltk_tree1) if max_depth is None else self.nltk_tree_to_n_bracket_string(nltk_tree1, max_depth)
        tree_string2 = self.nltk_tree_to_bracket_string(nltk_tree2) if max_depth is None else self.nltk_tree_to_n_bracket_string(nltk_tree2, max_depth)

        tree_string1 = self.clean_string(tree_string1)
        tree_string2 = self.clean_string(tree_string2)

        apted = APTED(APTEDTree.from_text(tree_string1), APTEDTree.from_text(tree_string2))
        edit_distance = apted.compute_edit_distance()

        return edit_distance
