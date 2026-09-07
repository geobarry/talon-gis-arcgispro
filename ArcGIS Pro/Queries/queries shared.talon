os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen
-
select [<user.ordinals>] clause: user.arc_select_nth_clause_item(ordinals or 1)
clause select [<user.ordinals>] {user.arc_clause_component}: user.arc_select_nth_clause_item(ordinals or 1,arc_clause_component)
clause select {user.dynamic_query_clause}: user.arc_act_on_clause(dynamic_query_clause,'value','select')

clause add$: user.arc_query_add_clause()
clause add [{user.conjunction}] {user.arc_field_name} [{user.arc_selection_predicate}]$:
	user.arc_populate_new_clause(conjunction or "or",arc_field_name,arc_selection_predicate or "is equal to")
clause add [{user.conjunction}] {user.arc_field_name} [{user.arc_selection_predicate}] <user.geo_list>: user.arc_query_add_multiple(conjunction or "or",arc_field_name,arc_selection_predicate or "is equal to",geo_list)

(city|cities) include <user.city_list>: user.arc_query_add_multiple("or","name","is equal to",city_list)

test <user.geo_list>: print(geo_list)

[clause] remove {user.dynamic_query_clause}+ [and {user.dynamic_query_clause}]: user.arc_act_on_clauses(dynamic_query_clause_list,'remove button','invoke')
remove <user.ordinals> clause:
	user.arc_select_nth_clause_item(ordinals,"remove button","invoke")
clause remove all: user.arc_query_remove_all()

clause {user.conjunction} {user.arc_field_name} {user.arc_selection_predicate}: user.arc_populate_selected_clause(conjunction,arc_field_name,arc_selection_predicate)

clause where {user.arc_field_name} {user.arc_selection_predicate}: user.arc_populate_selected_clause("",arc_field_name,arc_selection_predicate)

clause {user.conjunction}: user.arc_populate_selected_clause(conjunction)
clause {user.arc_selection_predicate}: user.arc_populate_selected_clause('','',arc_selection_predicate)

