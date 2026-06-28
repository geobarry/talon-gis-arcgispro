os: windows
app.exe: arcgispro.exe
#win.title: /Layer Properties.*/
mode: command
mode: user.zen
-
(select|go to) [<user.ordinals>] query: user.query_select_nth(ordinals or 1)
query activate: user.query_activate_selected()
query rename$: user.query_rename_selected()
query rename <user.constructed_text>: user.query_rename_selected(constructed_text)
[query] toggle SQL: user.query_toggle_sql()

SQL {user.arc_field_name} equals <user.win_nav_target>: 
	insert("{arc_field_name} = '{win_nav_target}'")
SQL include {user.arc_field_name} equals <user.constructed_text> [and <user.constructed_text>]+:
	user.query_include_multiple(arc_field_name,constructed_text_list)
SQL (add|append) {user.arc_field_name} equals <user.constructed_text> [and <user.constructed_text>]+:
	user.query_include_multiple(arc_field_name,constructed_text_list,true)
# append an or clause without specifying a value, e.g. "include name is equal to"
#include {user.arc_field_name} {user.arc_selection_predicate}$:
#	user.query_add_clause(arc_field_name,"","or",arc_selection_predicate)

# append a where clause without specifying a value, e.g. "include name is equal to"
#where {user.arc_field_name} {user.arc_selection_predicate}$:
#	user.query_add_clause(arc_field_name,"","or",arc_selection_predicate,true)

# append an or clause with a text value, e.g. "include name contains river"
#include {user.arc_field_name} {user.arc_selection_predicate} <user.text>$:
#	user.query_add_clause(arc_field_name,text,"or",arc_selection_predicate)
	
# append an or clause with a place name value, e.g. "include place name is equal to Brahmaputra"
#include place {user.arc_field_name} {user.arc_selection_predicate} {user.place}$:
#	user.query_add_clause(arc_field_name,place,"or",arc_selection_predicate)

#remove place {user.place}$:
#	user.query_remove_item(place)
