import itertools


class SimpleInverseSection:

    def __init__(self, generators) -> None:
        self.generators = generators

    def find_inverse_section(self, section):
        # order matters
        posible_sections = []

        # The intermidiate representation is a list of list of tuples, each tuple contains the
        # generator and the index such as ('a1', 0) that means that the value we are looking for
        # is 'b1'. In the case there are multiple options the results will be a list of all possible
        # options.
        for generator in section:
            options = []
            for generator_value, rules in self.generators.items():
                if generator not in rules:
                    continue

                index = rules.index(generator)
                options.append((generator_value, index))
            if not options:
                raise ValueError("Cannot find a generator associated with value {}".format(generator))

            posible_sections.append(options)

        # We compute the dot product of this to get all the posible sections
        posible_sections = list(itertools.product(*posible_sections))

        # We proceed to find the switch which is the generator with the value '01'
        switch = None
        for generator, rules in self.generators.items():
            if '01' in rules:
                switch = generator
                break
        else:
            raise ValueError("No switch was provided")

        identity = None
        for generator, rules in self.generators.items():
            if '1' in rules and '01' not in rules:
                for i, rule in enumerate(rules):
                    if '1' == rule:
                        identity = (generator, i)
                break

        # We add switch between all the posible self.generators we want to flip.
        inverted_sections = {}
        for restriciton in [0, 1]:
            restricted_section = []
            for posible_section in posible_sections:
                original_section = []
                for generator, index in posible_section:
                    if index == restriciton:
                        original_section.append(switch)
                    original_section.append(generator)

                updated_section = []
                using_switch = False
                consecutive_section = 0

                current_state = []
                last_section = None
                for section in original_section:
                    if not using_switch and section == switch:
                        using_switch = True
                        updated_section.append(section)
                        last_section = section
                        continue

                    if section != switch:
                        consecutive_section += 1
                    else:
                        consecutive_section = 0

                    if using_switch and consecutive_section > 1 and last_section != switch:
                        using_switch = False
                        updated_section.append(switch)


                    if section != switch:
                        updated_section.append(section)
                        last_section = section


                restricted_section.append(updated_section)
            inverted_sections[restriciton] = restricted_section

        original_sections = {0: inverted_sections[1], 1: inverted_sections[0]}

        if identity:
            identity_val = identity[0]
            identity_res = identity[1]
            special_cases = []

            for section in original_sections[identity_res]:
                # check if the last word is inverse if that is the case add switch and identity
                if section[-2] == switch:
                    special_cases.append(section + [switch, identity_val])

            original_sections[identity_res] += special_cases
            special_cases = []

            for section in original_sections[identity_res]:
                # check if we can add identity at the start
                if section[0] != identity_val:
                    special_cases.append([identity_val] + section)

            original_sections[identity_res] += special_cases

        return original_sections






# # Generators must be a dictionary of string with string tuples
# # generators = {
# #     'b1': ('01'),
# #     'a1': ('b1', 'a2'),
# #     'a2': ('0', 'a1'),
# #     'a3': ('0', 'a1'),
# # }
# _generators = {
#     'b1': ('01'),
#     'a1': ('b1', 'a2'),
#     'a2': ('1', 'a1'),
# }

# _section = ['b1', 'a1']

# inverse_section = SimpleInverseSection(_generators)
# print(inverse_section.find_inverse_section(_section))