from talon import Module, Context, actions, registry, clip, imgui, registry
import re
import os
from collections import defaultdict
import time

mod=Module()

""" path to the base folder within the user's talent directory"""
base_folder=os.path.dirname(os.path.abspath(__file__))

def get_module_id(rel_path):
    item_list=base_folder.split("\\")
    item_list=item_list[item_list.index("user"):]
    item_list += rel_path.split(".")
    if item_list[-1] != "talon":
        item_list += ["talon"]
    mod_id=".".join(filter(None, item_list))
    return mod_id

def group_subfolders_by_name(root_dir):
    """
    Walks root_dir and returns a dict mapping the lowercase folder name ->
    list of full paths for every folder with that name (case-insensitive)
    found anywhere under root_dir.
    """
    folder_map = defaultdict(list)

    for dirpath, dirnames, _ in os.walk(root_dir):
        for name in dirnames:
            folder_map[name.lower()].append(os.path.join(dirpath, name))

    r={"main":[base_folder]} | dict(sorted(folder_map.items()))
    for name in r.keys():
        r[name] = ",".join(r[name])
    return r

mod.list("arc_folders", "Say 'arc help folder {arc_folder}' to show modules in folder.")

ctx_arc=Context()

# CONSTRUCT DICTIONARY OF FOLDERS WITHIN TALON ArcGIS Pro
folder_path_dict=group_subfolders_by_name(base_folder)
folder_list=list(folder_path_dict.keys())
ctx_arc.lists["user.arc_folders"] = folder_list

# CONSTRUCT TALON LIST OF COMMAND MODULES (.TALON FILES) WITHIN EACH FOLDER
cmd_mod_dict={}
cmd_mod_list: list[str] = []
for folder in folder_list:
    path_list_str=folder_path_dict[folder]
    path_list=path_list_str.split(",")
    cmd_file_list=[]
    for path in path_list:        
        partial_path=path[len(base_folder)+1:].replace("\\",".")      
        for f in os.listdir(path):
            if f.endswith(".talon"):
                cmd_mod_name=f[:-6]
                val=".".join(filter(None, [partial_path,cmd_mod_name,'talon']))
                cmd_mod_list.append(get_module_id(val))
                cmd_mod_dict[cmd_mod_name] = val
                cmd_file_list.append(cmd_mod_name)

    mod.list(f"arc_command_modules_{folder}","Say 'arc help {command_set}' to show commands within a command set.")
    ctx_arc.lists[f"user.arc_command_modules_{folder}"] = cmd_file_list
mod.list("arc_command_modules", "Say 'arc help {arc_command_module}' to show commands in a command module.")
ctx_arc.lists["user.arc_command_modules"] = cmd_mod_dict

# CONSTRUCT LIST OF TALON LISTS ASSOCIATED WITH ARC

from talon.scripting import types
arc_list_dict={}
arc_list_key=sorted(list(registry.lists.keys()))
for key in arc_list_key:
    if key.startswith("user.arc") and not key.startswith("user.arc_command_module") and not key == "user.arc_list":
        val=registry.lists[key]
        talon_list = actions.user.talon_get_active_registry_list(key)
        if not isinstance(talon_list, types.DynamicList):
            arc_list_dict[key[9:].replace("_", " ")] = str(key)

mod.list("arc_list","Say 'arc help list {arc_list}' to show list items.")
print(f'arc_list_dict: {arc_list_dict}')
ctx_arc.lists["user.arc_list"] = arc_list_dict

print(f"CONTEXT ARC LIST {ctx_arc.lists['user.arc_list']}")

my_search_phrase: str | None = None

def get_commands_for_contexts(context_names: list[str]) -> dict[str, dict[str, str]]:
    result = {}
    for name in context_names:
        context = registry.contexts.get(name)
        # print(f'ctx: {context}')
        if context is None:
            continue
        commands = {
            str(val.rule.rule): val.script.code
            for val in context.commands.values()
        }
        if commands:
            result[name] = commands
    return result

def build_rule_word_map(commands_by_context: dict[str, dict[str, str]]):
    """word -> set of (context_name, rule) pairs, scoped to this group only"""
    rule_word_map = defaultdict(set)
    for context_name, commands in commands_by_context.items():
        for rule in commands:
            tokens = {t for t in re.split(r"\W+", rule) if t.isalpha()}
            for token in tokens:
                rule_word_map[token].add((context_name, rule))
    return rule_word_map

def filter_commands_by_phrase(
    commands_by_context: dict[str, dict[str, str]], phrase: str
) -> dict[str, dict[str, str]]:
    if not phrase:
        return commands_by_context

    rule_word_map = build_rule_word_map(commands_by_context)
    tokens = phrase.lower().split(" ")

    viable = rule_word_map[tokens[0]]
    for token in tokens[1:]:
        viable &= rule_word_map[token]

    filtered = defaultdict(dict)
    for context_name, rule in viable:
        filtered[context_name][rule] = commands_by_context[context_name][rule]
    return dict(filtered)


@imgui.open(y=0)
def gui_my_context_group(gui: imgui.GUI):
    global cmd_mod_list, my_search_phrase

    commands_by_context = get_commands_for_contexts(cmd_mod_list)
    
    commands_by_context = filter_commands_by_phrase(commands_by_context, my_search_phrase)

    title = f"Selected contexts (search: {my_search_phrase})" if my_search_phrase else "Selected contexts"
    gui.text(title)
    gui.line()

    if not commands_by_context:
        gui.text("No matching commands")

    for context_name, commands in commands_by_context.items():
        gui.text(context_name)
        gui.line()
        for rule, code in commands.items():
            gui.text(f"{rule}")
        gui.spacer()

    gui.spacer()
    if gui.button("Help close"):
        gui_my_context_group.hide()

@mod.action_class
class arc_help_utils_Actions:
    def arc_help_module(rel_path: str):
        """brings up help imgui for given module"""
        mod_id=get_module_id(rel_path)
        print(f'mod_id: {mod_id}')
        clip.set_text(mod_id)
        actions.user.help_selected_context(mod_id, show_code=False)


    def arc_help_search(phrase: str = None):
        """Show commands for a specific list of contexts, optionally filtered by a search phrase"""
        global cmd_mod_list, my_search_phrase

        my_search_phrase = phrase.lower() if phrase else None
        gui_my_context_group.show()
        
    def close_arc_help_search():
        """Closes the imgui for arc help search"""
        gui_my_context_group.hide()