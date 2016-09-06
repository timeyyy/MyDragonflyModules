# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)
import os

from dragonfly import *
from dragonfly.actions.action_base import BoundAction

from supporting import utils, character

def addAlias(dictation):
    alias_name = str(dictation)
    alias_value = utils.getSelectedText()
    if not alias_value or alias_value == "":
        raise StandardError("No value for \"alias_value\".  Select some text to alias.")
    file_path = "C:\\NatLink\\NatLink\\MacroSystem\\_aliases.py"
    lines = []
    with open(file_path, 'r') as aliases:
        lines = aliases.readlines()
    with open(file_path, 'w') as aliases:
        started_mapping = False
        done_adding = False
        for line in lines:
            if done_adding:
                aliases.write(line)
                continue
            if not started_mapping:
                aliases.write(line)
                if line.find("mapping = {") != -1:
                    started_mapping = True
                    continue
            if started_mapping and not done_adding:
                if line.find("}") != -1:
                    aliases.write("\t\t\"" + alias_name + "\": Text(\"" + alias_value + "\"),\n")
                    aliases.write(line)
                    done_adding = True
                else:
                    aliases.write(line)
                

class Example(MappingRule):
    mapping = {
        "alias <dictation>": Function(addAlias),
    }
    extras = [Dictation("dictation")]


example_grammar = Grammar("example grammar")
example_grammar.add_rule(Example())


example_grammar.load()

def unload():
    global example_grammar
    if example_grammar:
        print "unloading " + __name__ + "..."
        example_grammar.unload()
    example_grammar = None
