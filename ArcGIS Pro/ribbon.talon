os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen
-

# RIBBON
^menu {user.arc_menu_heading}$: user.arc_open_ribbon(arc_menu_heading)
^{user.arc_menu_item}$: user.arc_call_ribbon_item(arc_menu_item)
# more verbose version
[open the] {user.arc_menu_heading} menu: user.arc_open_ribbon(arc_menu_heading)
# inserts text into the textbox just after the label with a given text
toggle ribbon: key("ctrl-f1")



# DEVELOPMENT
^ribbon copy {user.arc_menu_heading} items$: user.arc_get_ribbon_items(arc_menu_heading) 

# MENU ITEM SHORTCUTS - do we need these anymore?
# insert menu shortcuts
# new map command already mapped above
new layout: key(alt n n l)
new custom layout: key(alt n n l c tab:4)
(new|add) map frame: key(alt n m g)

# analysis menu shortcuts
new jupyter notebook: user.slow_key_press("alt-a p f down right:3 enter",1.0)

# edit menu shortcuts
save edits:
	key(esc:5)
	key(alt)
	sleep(0.2)
	key(e s v)
	
# layout menu shortcuts

# table menu shortcuts
add field:
	key(esc:5)
	key(alt)
	sleep(0.2)
	key(t v f n)
zoom [to] selected: key(alt t v r z)
flash (selected|active): key(alt t v r f)
pan [to] (selected|active): key(alt t v r p)

	
# field menu shortcuts
save fields:
	key(esc:5)
	key(alt)
	sleep(0.2)
	key(f s v)
# share menu shortcuts
export layout:
	key(esc:5)
	key(alt)
	sleep(0.2)
	key(s x l)
	sleep(0.5)
	key(down:3)
# map frame menu shortcuts
[set] (text|map|legend|scale bar|north arrow|arrow|line|shape) position: 
	key(esc:5 alt j f s p)
	user.key_to_elem_by_val("tab","TextBox","class_name")
	key(ctrl-a)
flip vertical: key(alt j f r v)
flip horizontal: key(alt j f r v)


