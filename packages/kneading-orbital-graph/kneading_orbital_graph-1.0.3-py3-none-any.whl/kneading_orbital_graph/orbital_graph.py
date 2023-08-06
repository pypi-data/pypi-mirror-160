import copy
import json
import networkx
import itertools
from pprint import pprint
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from networkx.algorithms.distance_measures import center


# Compute the return values.
def _compute_return_values(all_states, graph, boundary_point, current_node, previous_node, prefixes, sufixes, previous_edge, return_values):
    adjacent_nodes = list(graph[current_node].keys())
    edges = set([graph[current_node][adjacent_node]['fn'] for adjacent_node in adjacent_nodes])
    free_edges = list(all_states.difference(edges))

    if previous_node in adjacent_nodes:
        adjacent_nodes.remove(previous_node)

    if boundary_point == current_node:
        new_prefixes = copy.deepcopy(prefixes)

        for i in range(len(new_prefixes)):
            if isinstance(new_prefixes[i], list):
                new_prefixes[i] = [''] + new_prefixes[i]
        return

    if free_edges:

        if previous_edge != '':
            _return_values = prefixes + [previous_edge] + [free_edges] + [previous_edge] + sufixes
        else:
            _return_values = prefixes + [free_edges] + sufixes

        return_value = []
        for value in _return_values:
                if isinstance(value, list) and not value:
                    continue
                return_value.append(value)

        return_values.append(return_value)

    if adjacent_nodes:
        new_prefixes = []
        new_sufixes = []

        if prefixes:
            nested_list = False
            for prefix in prefixes:
                if isinstance(prefix, list):
                    nested_list = True
                    break

            if nested_list:
                new_prefixes = prefixes
            else:
                new_prefixes = [prefixes]

        if sufixes:
            nested_list = False
            for sufix in sufixes:
                if isinstance(sufix, list):
                    nested_list = True
                    break
            if nested_list:
                new_sufixes = sufixes
            else:
                new_sufixes = [sufixes]

        if previous_edge != '':
            new_prefixes.append(previous_edge)
            new_sufixes.insert(0, previous_edge)

        if free_edges:
            new_prefixes += [free_edges]
            new_sufixes = [free_edges] + new_sufixes

        for adjacent_node in adjacent_nodes:
            _compute_return_values(
                all_states, graph, boundary_point, adjacent_node, current_node, new_prefixes,
                new_sufixes, graph[current_node][adjacent_node]['fn'], return_values
            )


def rule_weight(rule):
    weight = []
    for segment in rule:
        if isinstance(segment, list):
            weight.append(len(segment))
        else:
            weight.append(1)
    return weight

def sort_return_rules(return_rules):
    rules = {}
    for i in range(len(return_rules)):
        sorted_rule = []
        for rule_segment in return_rules[i]:
            if isinstance(rule_segment, list):
                rule_segment.sort()
            sorted_rule.append(rule_segment)
        if len(sorted_rule) not in rules:
            rules[len(sorted_rule)] = []
        rules[len(sorted_rule)].append(sorted_rule)

    sorted_rules = []
    for i in sorted(rules.keys()):
        i_sorted_rules = rules[i]
        i_sorted_rules.sort(key=rule_weight)
        sorted_rules += i_sorted_rules
        # print(i, i_sorted_rules)

    return sorted_rules

class OrbitalGraph:

    def __init__(self, automata=[]) -> None:
        self.automata = automata

        # split the different type of nodes so we easile count and make the state progression
        self.a_states = []
        self.b_states = []

        # a set to keep track of all states
        self.all_states = {'b1'}

        for state in self.automata:
            if state[0].startswith('a'):
                self.a_states.append(state)
            elif state[0].startswith('b'):
                self.b_states.append(state)

            self.all_states.add(state[0])


    def _generate_graph_structure(self, states=[]):
        if len(states) == 0:
            return [{'u': '0', 'v': '1', 'fn': 'b1'}]

        graph = []
        # case of b1
        case = ["".join(seq) for seq in itertools.product("01", repeat=len(states))]
        for word in case:
            graph.append({'u': '0'+word, 'v': '1'+word, 'fn': 'b1'})

        # generarate all cases
        case = ["".join(seq) for seq in itertools.product("01", repeat=len(states)+1)]

        current_start_with = ''
        for state, fn in reversed(states):
            current_start_with = fn + current_start_with
            start = [x for x in case if x.startswith(current_start_with)]
            offset = int(len(start)/2)
            if len(start) > 2:
                for i in range(0, int(len(start)/2)):
                    graph.append({'u': start[i], 'v': start[i+offset], 'fn': state})
            else:
                graph.append({'u': start[0], 'v': start[1], 'fn': state})

        return graph

    def _generate_graph_boundary(self, graph_path):
        graph = networkx.Graph()
        all_nodes = []
        for element in self._generate_graph_structure(graph_path):
            params = {}
            params['u_of_edge'] = element['u']
            params['v_of_edge'] = element['v']
            params['fn'] = element['fn']
            graph.add_edge(**params)
            all_nodes.append(params)

        boundary = [center(graph)[0][:-1]]
        mapping  = {}
        for param in all_nodes:
            mapping[param['u_of_edge']] = param['u_of_edge'][:-1]
            mapping[param['v_of_edge']] = param['v_of_edge'][:-1]

        graph = networkx.relabel_nodes(graph, mapping)

        for node in graph.nodes():
            if node in graph[node]:
                graph.remove_edge(node, node)

        return graph, boundary


    def plot_orbital_graph(self, graph, boundary_point, fixed_points=None, nx_layout=None):
        if fixed_points is None:
            fixed_points = []

        figure(num=None, figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')

        if nx_layout is None:
            pos = networkx.kamada_kawai_layout(graph)
        else:
            pos = nx_layout(graph)

        boundary_point = [boundary_point]
        networkx.draw(graph, with_labels=True, pos=pos, connectionstyle='arc3, rad = 0.1')
        edge_labels = networkx.get_edge_attributes(graph,'fn')
        networkx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        networkx.draw_networkx_nodes(graph, pos, nodelist=set(graph.nodes)-set(boundary_point)-set(fixed_points))
        networkx.draw_networkx_nodes(graph, pos, nodelist=boundary_point, node_color='r')

        if fixed_points:
            networkx.draw_networkx_nodes(graph, pos, nodelist=fixed_points, node_color='g')

        plt.show()

    def orbital_graph(self, level=1):
        original_level = level
        level -= 1

        states = []

        if level > 0:
            if level >= len(self.b_states):
                level -= len(self.b_states)
                states = self.b_states
            else:
                states = self.b_states[-1 * level:]
                level = 0

            if level > 0:
                repetitions = int(level/(len(self.a_states)-1))
                mod = level%(len(self.a_states)-1)
                new_a_states = []
                if repetitions > 0:
                    new_a_states = self.a_states[:-1] * repetitions
                if mod > 0:
                    new_a_states = self.a_states[:-1][-1 * mod:] + new_a_states
                states = new_a_states + [self.a_states[-1]] + states

        graph, boundary = self._generate_graph_boundary(states)

        # compute fixed points
        points = [self.a_states[i][1] for i in reversed(range(len(self.a_states)))][1:]

        fixed_points = []

        for i in range(len(points)):
            fixed_point = []
            current_point = i
            for j in range(original_level):
                if current_point < len(points):
                    fixed_point.append(points[current_point])
                    current_point += 1
                else:
                    current_point -= len(points)
                    fixed_point.append(points[current_point])
                    current_point += 1
            fixed_points.append(''.join(fixed_point))

        fixed_points = list(set(fixed_points))

        all_fixed_points = []
        for state in graph.nodes():
            for fixed_point in fixed_points:
                if state.startswith(fixed_point) and state != boundary:
                    all_fixed_points.append(state)
        fixed_points = list(set(all_fixed_points))

        if boundary[0] in fixed_points:
            fixed_points.remove(boundary[0])

        return graph, boundary[0], fixed_points

    # # Compute the return values.
    def compute_return_rules(self, graph, boundary_point, fixed_points):
        return_rules = []
        for fixed_point in fixed_points:
            _compute_return_values(self.all_states, graph, boundary_point, fixed_point, '', [], [], '', return_rules)
        print('Number of return rules', len(return_rules))
        return_rules = sort_return_rules(return_rules)
        return return_rules

    def expand_return_rules(self, rules, n_rules=-1):
        all_return_values = []
        print('Rules longest lenght', max([len(x) for x in rules]))
        print('Using the first {} rules'.format(n_rules))

        iters = 0
        for i in range(len(rules)):
            if len(rules[i]) < 2:
                continue

            if iters == n_rules:
                break
            print('Lenght', len(rules[i]), 'Rule', rules[i])

            return_point_rule = []
            for value in rules[i]:
                if isinstance(value, str):
                    return_point_rule.append([value])
                else:
                    return_point_rule.append(value)
            for return_point in itertools.product(*return_point_rule):
                return_point = list(return_point)
                while '' in return_point:
                    return_point.remove('')

                simplified_return_point = []
                for transition in return_point:
                    if not simplified_return_point:
                        simplified_return_point.append(transition)
                    else:
                        if transition == simplified_return_point[-1]:
                            continue
                        else:
                            simplified_return_point.append(transition)
                all_return_values.append(simplified_return_point)

            iters += 1
        print('all values', len(all_return_values))
        return all_return_values

    def reduce_return_values(self, all_values):
        str_return_values = [str(value)[1:-1] for value in all_values]
        unique_return_values = []
        to_remove = []

        for i in range(len(str_return_values)):
            value = str_return_values[i]

            if value in to_remove or value in unique_return_values:
                continue

            unique_return_values.append(value)

            for j in range(len(str_return_values)):
                if i == j:
                    continue

                if str_return_values[i] in str_return_values[j] or str_return_values[j] in str_return_values[i]:
                    to_remove.append(str_return_values[j])
                    continue

            unique_return_values.sort(key=len)
        return unique_return_values