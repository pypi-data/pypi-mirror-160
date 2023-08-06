import networkx
import itertools
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure


class SubshiftFiniteType:
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def _compute_space_size(self, restrictions):
        longest = []
        for rest in restrictions:
            if len(rest) > len(longest):
                longest = rest
        return len(longest)-1

    def _generate_space(self, restrictions=[]):
        size = self._compute_space_size(restrictions)

        if size < 1:
            raise ValueError("Restrictions should be at least lenght 2")

        space = list(itertools.product(self.alphabet, repeat=size))
        alphabet_restictions = [[x, x] for x in self.alphabet]
        filtered_restrictions = [tuple(x) for x in restrictions+alphabet_restictions if len(x) <= size]

        clean_space = []
        for element in space:
            str_element = str(element)[1:-1]
            is_free = True
            for _restriction in filtered_restrictions:
                str_restriction = str(_restriction)[1:-1]
                if str_element in str_restriction or str_restriction in str_element:
                    is_free = False
                    break
            if is_free:
                clean_space.append(element)
        return clean_space

    def generate_graph(self, restrictions):
        space = self._generate_space(restrictions)

        # list of n-1 word, n-1 word, n word/transition.
        structure = []
        graph = networkx.Graph()
        tupled_restrictions = [tuple(x) for x in restrictions]
        words_restrictions = [''.join(x) for x in restrictions]

        def check_if_squish(left, right):
            if left[-1] == right[0]:
                return tuple(list(left) + list(right[1:]))

        for fixed_element in space:
            for element in space:
                if fixed_element == element:
                    continue
                squished = check_if_squish(fixed_element, element)
                if squished is not None and squished not in tupled_restrictions:
                    is_subword = False
                    word_squished = ''.join(squished)

                    for word_restriction in words_restrictions:
                        if word_restriction in word_squished:
                            is_subword = True
                            break

                    if not is_subword:
                        graph.add_edge(**{'u_of_edge': fixed_element, 'v_of_edge': element, 'fn': squished})
        return graph

    def default_subshift_graph_plot(self, sft_graph):
        figure(num=None, figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')
        pos = networkx.spiral_layout(sft_graph)
        pos = networkx.kamada_kawai_layout(sft_graph)
        pos = networkx.circular_layout(sft_graph)

        networkx.draw(sft_graph, with_labels=True, pos=pos, connectionstyle='arc3, rad = 0.1')
        edge_labels = networkx.get_edge_attributes(sft_graph,'fn')
        networkx.draw_networkx_edge_labels(sft_graph, pos, edge_labels=edge_labels)
        plt.show()
