"""
Construction class and related functions are to represent constructions
given in a grammar-like syntax. With them, one can
- change/set relations between machines
- ???

TODO:
- matching based on Control class
- do() function to make the changes implied by @command
- unique S construction whose rule is distinguished from any others
  - lookup the Verb in construction in definition collection
  - use Nouns and their deep cases in construction to insert them into
    the verb machine
"""
from control import PosControl as Control

class Command:
    """
    Abstract class for commands in constructions
    """

    """
    @pairs if a mapping between Control and Machine instances
    keys of @pairs are Control instances,
    values of @pairs are Machine instances.

    runs the command over the machines
    returns None if there is nothing to be changed,
    otherwise a new machine list
    """
    def run(self, pairs):
        pass

    """
    Factory method
    """
    @staticmethod
    def get_instance(type_str, terminals):
        import re
        append_regex_pattern = re.compile("([^\[]*)\[([^\]]*)\]")
        m = append_regex_pattern.match(type_str)
        if m is not None:
            return AppendRegexCommand(m.groups()[0], m.groups()[1])

        one_rule_pattern = re.compile("|".join(terminals))
        m = one_rule_pattern.match(type_str)
        if m is not None:
            return OneCommand(m.group(0))

        if type_str == "*":
            return VerbCommand()


class AppendRegexCommand(Command):
    """
    Appends one of the machines at a partition of the other one
    """
    def __init__(self, into, what):
        self.into = Control(into)
        self.what = Control(what)

    def run(self, pairs):
        pairs[self.into].append(1, pairs[self.what])
        return [pairs[self.into]]

class OneCommand(Command):
    """
    Removes one from the @machines. The other is kept.
    """
    def __init__(self, stay):
        self.stay = Control(stay)

    def run(self, pairs):
        filterer = lambda a: a[0] == self.stay
        return [m for c, m in filter(filterer, pairs.items())]

class VerbCommand(Command):
    """
    The machine of the verb is looked up in the defining dictionary,
    and any deep cases found in that machine get matched by NP cases
    """
    def __init__(self):
        pass
        #raise NotImplementedError()
    
    def run(self, pairs):
        return None

class Construction:
    """
    instructions about how to perform transformations in machines
    """

    """
    @rule_left: now this is not used
    @rule_right: on what machines to perform operations, based on their Control
    @command: what to do
    """
    def __init__(self, rule_left, rule_right, command):
        self.rule_left = rule_left
        self.rule_right = [Control(part) for part in rule_right]
        self.command = Command.get_instance(command, rule_right)

    """
    checks if the given @machines are possible inputs for this construction
    uses only @self.rule_right

    returns False if not matched
    returns a dictionary with (control, machine) pairs
    """
    def __match__(self, machines):
        if len(machines) != len(self.rule_right):
            return False

        possible_pairs = {}
        for machine in machines:
            pair_for_machine = []
            for c in self.rule_right:
                if machine.control.is_a(c):
                    pair_for_machine.append(c)
            possible_pairs[machine] = pair_for_machine
        
        pairs = {}
        for m, pp in possible_pairs.items():
            if len(pp) > 1:
                raise NotImplementedError("Now only definite matches (only 1-1) are supported")
            elif len(pp) == 0:
                return False
            else:
                """if two machines match the same rule, then it's not
                a real match"""
                if m in pairs.values():
                    return False
                pairs[pp[0]] = m

        """if there is no mapping for each part of the rule, then it's not
        a real match"""
        if len(pairs) != len(self.rule_right):
            return False

        return pairs

    def do(self, machines):
        pairs = self.__match__(machines)
        if not pairs:
            return None
        else:
            return self.command.run(pairs)

def read_constructions(f):
    constructions = set()
    for l in f:
        l = l.strip().split("\t")
        constructions.add(Construction(l[0], l[1].split(), l[2]))
    return constructions

if __name__ == "__main__":
    pass

