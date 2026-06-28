os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen
-
(select|unselect) feature: key(ctrl-space)
next feature$: 
	key(enter)
	sleep(0.6)
	user.arc_attribute_table_feature_command("ctrl-n")

# ELEMENT SELECTION
new field select: user.arc_fields_view_focus_new_field()
table select: user.arc_focus_table()


# TABLE VIEW
[open] attribute table: key(ctrl-t)
toggle (select|selection): key(ctrl-space)
(switch|invert) selection: key(ctrl-u)
clear table selection: key(ctrl-shift-a)
(column|field) next: key(tab)
(column|field) previous: key(shift-tab)
(column|field) first: key(home)
(column|field) last: key(end)

(column|field) commands: key("menu o")
(column|field) sort: key("menu o s")
(column|field) sort descending: key("menu o d")
(column|field) hide: 
	key("menu o h")
	sleep(0.5)

(row|record|feature) commands: key("menu r")

(row|record|feature) next: key(enter)
(row|record|feature) first: key(ctrl-up)
(row|record|feature) last: key(ctrl-down)
(row|record|feature) select: key(ctrl-space)
(row|record|feature) unselect: key(ctrl-space)

(row|record|feature) go$: key(ctrl-g)
(row|record|feature) go <number>$:
	key(ctrl-g)
	insert(number)
	key(enter esc)
(row|record|feature) flash: user.arc_attribute_table_feature_command("ctrl-8")
(row|record|feature) zoom to: user.arc_attribute_table_feature_command("ctrl-=")
(row|record|feature) pan [to]: user.arc_attribute_table_feature_command("ctrl-n")
(row|record|feature) popup: user.arc_attribute_table_feature_command("ctrl-i")


show selected (records|features|rows): user.arc_show_records("Selected")
show all (records|features|rows): user.arc_show_records("All")

extend down: key(shift-down)
extend up: key(shift-up)
select next: key(ctrl-enter)
select previous: key(shift-enter)
[custom] sort: key(ctrl-shift-s)
toggle aliases: key(ctrl-shift-n)
copy table:
	# copies contents of table for pasting into Microsoft excel
	key(ctrl-shift-a ctrl-u ctrl-shift-c)

