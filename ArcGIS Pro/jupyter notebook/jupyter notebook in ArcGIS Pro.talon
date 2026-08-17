os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen
-
#jupiter save: user.arc_invoke_jupyter_button("save")
jupyter notebook {user.jupyter_toolbar_command}: user.arc_invoke_jupyter_command(jupyter_toolbar_command)
jupyter notebook content: user.arc_go_to_jupyter_content()
jupyter notebook go to cell <number>: user.arc_go_to_jupyter_cell(number)