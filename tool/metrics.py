"""Implements the Distinct-n metric for evaluating diversity in dialogues.
The implementation is copied from Joko et al. (2024) which is based on Tevet et al. (2021).
For more details, refer to Joko et al. (2024).

References:
- Joko et al. (2024): https://dl.acm.org/doi/10.1145/3626772.3657815
    (GitHub: https://github.com/informagi/laps)
- Tevet et al. (2021): https://aclanthology.org/2021.eacl-main.25/
"""

import random
from nltk.tokenize import word_tokenize
import numpy as np
from typing import List, Tuple, Union

def _truncate_response_set(response_set: List[str], max_token_length: int) -> List[str]:
    truncated_response_set = []
    token_count = 0
    for line in response_set:
        words = line.split()
        if token_count + len(words) <= max_token_length:
            truncated_response_set.append(line)
            token_count += len(words)
        else:
            remaining_space = max_token_length - token_count
            words_to_append = words[:remaining_space]
            truncated_response_set.append(' '.join(words_to_append))
            token_count += len(words_to_append)
            break
    
    # Check if total token count is less than max_token_length
    if token_count < max_token_length:
        print("\033[93mWarning: The response did not reach the maximum token limit.\033[0m")

    return truncated_response_set

class DistinctNgrams:
    """Class to calculate Distinct-n metric as per Tevet's implementation."""

    def __init__(self, n: int = 2, tokenizer_name: str = 'split', use_lower_case: bool = True) -> None:
        self.n = n
        self.tokenizer_name = tokenizer_name
        self.use_lower_case = use_lower_case

    def _tokenize(self, line: str) -> List[str]:
        """Tokenizes the input line based on the specified tokenizer_name.

        Args:
            line (str): The input line to _tokenize.

        Returns:
            list: A list of tokens from the input line.
        """
        if self.use_lower_case:
            line = line.lower() # this is because M2M is lowercased dataset, thus for fair comparison we need to lowercase the other datasets as well.
        if self.tokenizer_name == 'split':
            return [e for e in line.replace('.','').replace('\n','').split(' ') if e != ''] # The same as Tevet's implementation
        elif self.tokenizer_name == 'nltk':
            return word_tokenize(line)
        else:
            raise ValueError("Invalid tokenizer_name. Valid options are 'split' and 'nltk'.")

    def lines_to_ngrams(self, lines: List[str]) -> List[List[Tuple[str, ...]]]:
        ngram_lists = []
        for line in lines:
            words = self._tokenize(line)
            ngrams = [tuple(words[i:i+self.n]) for i in range(len(words)-self.n+1)]
            ngram_lists.append(ngrams)
        return ngram_lists

    def _calculate_unique_ngram_ratio(self, ngram_lists: List[List[Tuple[str, ...]]]) -> float:
        ngrams = [item for sublist in ngram_lists for item in sublist]  # flatten
        return len(set(ngrams)) / len(ngrams) if len(ngrams) > 0 else 0.

    def calculate_distinct_n(self, response_set: List[str]) -> float:
        return self._calculate_unique_ngram_ratio(self.lines_to_ngrams(response_set))

    def calculate_normalized_distinct_n(self, response_set: List[str], return_avg: bool = True, max_token_length: int = 7012, iterations: int = 100, seed: int = 42) -> Union[float, List[float]]:
        """Calculates the truncated Distinct-n metric for a set of responses.

        This method implements the truncated Distinct-n metric as described in Joko et al. (2024).
        For more details, refer to: https://dl.acm.org/doi/10.1145/3626772.3657815

        Args:
            response_set (list): A list of responses to calculate the Distinct-n metric for.
            return_avg (bool): If True, return the average of the Distinct-n metric across iterations.
            max_token_length (int, optional): The maximum number of tokens to consider. Defaults to 7012.
                This truncation is necessary because Distinct-n is sensitive to text length.
            iterations (int, optional): The number of times to repeat the calculation. Defaults to 100.
                Used for calculating the average if return_avg is True.
            seed (int, optional): The random seed for shuffling responses. Defaults to 42.

        Returns:
            float or list: If return_avg is True, returns the average Distinct-n metric.
                           Otherwise, returns a list of Distinct-n values for each iteration.

        Note:
            The parameters used here are consistent with those in Joko et al. (2024).
        """

        distinct_n_values = []
        random.seed(seed)
        for _ in range(iterations):
            shuffled_response_set = random.sample(response_set, len(response_set))
            truncated_response_set = _truncate_response_set(shuffled_response_set, max_token_length)
            distinct_n = self.calculate_distinct_n(truncated_response_set)
            distinct_n_values.append(distinct_n)

        if return_avg:
            return sum(distinct_n_values) / iterations
        else:
            return distinct_n_values
