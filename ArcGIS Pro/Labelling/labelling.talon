os: windows
app.exe: arcgispro.exe
mode: command
mode: user.zen

-
# LABEL CLASS PANEL
label class: user.arc_label_group(".*LabelClass.*")
label symbol: user.arc_label_group("Symbol","General")
label position: user.arc_label_group("Position",'1')

label expression: user.arc_label_group('.*LabelClass.*','Label Expression')
label query: user.arc_label_group('.*LabelClass.*','SQL query')
label visibility: user.arc_label_group('.*LabelClass.*','Visibility range')

label formatting: user.arc_label_group("Symbol",'Formatting')
label paragraph: user.arc_label_group("Symbol",'Paragraph')

label fitting strategy: user.arc_label_group('Position','2')
label conflict resolution: user.arc_label_group('Position','3')
