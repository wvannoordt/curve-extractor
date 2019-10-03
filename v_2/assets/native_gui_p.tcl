#############################################################################
# Generated by PAGE version 4.25.1
#  in conjunction with Tcl version 8.6
#  Oct 02, 2019 02:30:37 PM MDT  platform: Windows NT
set vTcl(timestamp) ""


if {!$vTcl(borrow) && !$vTcl(template)} {

set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_analog) #ececec
set vTcl(actual_gui_menu_analog) #ececec
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #ececec
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #ececec
set vTcl(active_menu_fg) #000000
}




proc vTclWindow.top42 {base} {
    global vTcl
    if {$base == ""} {
        set base .top42
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background #191919 
    wm focusmodel $top passive
    wm geometry $top 1266x777+120+85
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 1936 1067
    wm minsize $top 160 12
    wm overrideredirect $top 0
    wm resizable $top 0 0
    wm deiconify $top
    wm title $top "New Toplevel"
    vTcl:DefineAlias "$top" "CurveExtWindow" vTcl:Toplevel:WidgetProc "" 1
    canvas $top.can43 \
        -background #2d2d2d -closeenough 1.0 -height 753 \
        -highlightbackground #000000 -insertbackground black -relief ridge \
        -selectbackground #c4c4c4 -selectforeground black -width 973 
    vTcl:DefineAlias "$top.can43" "image_canvas" vTcl:WidgetProc "CurveExtWindow" 1
    button $top.but44 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #606060 -disabledforeground #9e0000 \
        -font {-family {Arial Black} -size 12 -weight bold} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -relief flat -text Import 
    vTcl:DefineAlias "$top.but44" "open_file_button" vTcl:WidgetProc "CurveExtWindow" 1
    button $top.but45 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #606060 -disabledforeground #9e0000 \
        -font {-family {Arial Black} -size 12 -weight bold} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -relief flat -text Export 
    vTcl:DefineAlias "$top.but45" "export_button" vTcl:WidgetProc "CurveExtWindow" 1
    button $top.but46 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #606060 -disabledforeground #9e0000 \
        -font {-family {Arial Black} -size 12 -weight bold} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -relief flat -text X1 
    vTcl:DefineAlias "$top.but46" "x1_button" vTcl:WidgetProc "CurveExtWindow" 1
    button $top.but47 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #606060 -disabledforeground #9e0000 \
        -font {-family {Arial Black} -size 12 -weight bold} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -relief flat -text X2 
    vTcl:DefineAlias "$top.but47" "x2_button" vTcl:WidgetProc "CurveExtWindow" 1
    button $top.but48 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #606060 -disabledforeground #9e0000 \
        -font {-family {Arial Black} -size 12 -weight bold} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -relief flat -text Y1 
    vTcl:DefineAlias "$top.but48" "y1_button" vTcl:WidgetProc "CurveExtWindow" 1
    button $top.but49 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #606060 -disabledforeground #9e0000 \
        -font {-family {Arial Black} -size 12 -weight bold} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -relief flat -text Y2 
    vTcl:DefineAlias "$top.but49" "y2_button" vTcl:WidgetProc "CurveExtWindow" 1
    entry $top.ent50 \
        -background #c6c6c6 -disabledforeground #a3a3a3 \
        -font {-family {Arial Black} -size 12 -weight bold} \
        -foreground $vTcl(actual_gui_fg) -insertbackground black \
        -justify center -relief flat -selectbackground #56a06f \
        -selectforeground #000000 
    vTcl:DefineAlias "$top.ent50" "x1_entry" vTcl:WidgetProc "CurveExtWindow" 1
    entry $top.ent51 \
        -background #c6c6c6 -disabledforeground #a3a3a3 \
        -font {-family {Arial Black} -size 12 -weight bold} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -justify center -relief flat \
        -selectbackground #56a06f -selectforeground #000000 
    vTcl:DefineAlias "$top.ent51" "x2_entry" vTcl:WidgetProc "CurveExtWindow" 1
    entry $top.ent52 \
        -background #c6c6c6 -disabledforeground #a3a3a3 \
        -font {-family {Arial Black} -size 12 -weight bold} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -justify center -relief flat \
        -selectbackground #56a06f -selectforeground #000000 
    vTcl:DefineAlias "$top.ent52" "y1_entry" vTcl:WidgetProc "CurveExtWindow" 1
    entry $top.ent53 \
        -background #c6c6c6 -disabledforeground #a3a3a3 \
        -font {-family {Arial Black} -size 12 -weight bold} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -justify center -relief flat \
        -selectbackground #56a06f -selectforeground #000000 
    vTcl:DefineAlias "$top.ent53" "y2_entry" vTcl:WidgetProc "CurveExtWindow" 1
    entry $top.ent56 \
        -background #c6c6c6 -disabledforeground #a3a3a3 \
        -font {-family {Arial Black} -size 12 -weight bold} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -justify center -relief flat \
        -selectbackground #56a06f -selectforeground #000000 
    vTcl:DefineAlias "$top.ent56" "num_points_entry" vTcl:WidgetProc "CurveExtWindow" 1
    label $top.lab57 \
        -activebackground #191919 -activeforeground #c6c6c6 \
        -background #191919 -disabledforeground #a3a3a3 \
        -font {-family {Arial Black} -size 12 -weight bold} \
        -foreground #c6c6c6 -text {# Points} 
    vTcl:DefineAlias "$top.lab57" "Label1" vTcl:WidgetProc "CurveExtWindow" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.can43 \
        -in $top -x 280 -y 10 -width 973 -relwidth 0 -height 753 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but44 \
        -in $top -x 10 -y 10 -width 136 -relwidth 0 -height 43 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but45 \
        -in $top -x 10 -y 60 -width 136 -relwidth 0 -height 43 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but46 \
        -in $top -x 10 -y 150 -width 66 -relwidth 0 -height 43 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but47 \
        -in $top -x 10 -y 200 -width 66 -height 43 -anchor nw \
        -bordermode ignore 
    place $top.but48 \
        -in $top -x 10 -y 250 -width 66 -height 43 -anchor nw \
        -bordermode ignore 
    place $top.but49 \
        -in $top -x 10 -y 300 -width 66 -height 43 -anchor nw \
        -bordermode ignore 
    place $top.ent50 \
        -in $top -x 120 -y 150 -width 124 -relwidth 0 -height 44 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.ent51 \
        -in $top -x 120 -y 200 -width 124 -height 44 -anchor nw \
        -bordermode ignore 
    place $top.ent52 \
        -in $top -x 120 -y 250 -width 124 -height 44 -anchor nw \
        -bordermode ignore 
    place $top.ent53 \
        -in $top -x 120 -y 300 -width 124 -height 44 -anchor nw \
        -bordermode ignore 
    place $top.ent56 \
        -in $top -x 120 -y 440 -width 124 -height 44 -anchor nw \
        -bordermode ignore 
    place $top.lab57 \
        -in $top -x 10 -y 440 -width 102 -relwidth 0 -height 46 -relheight 0 \
        -anchor nw -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

set btop ""
if {$vTcl(borrow)} {
    set btop .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop $vTcl(tops)] != -1} {
        set btop .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop
Window show .
Window show .top42 $btop
if {$vTcl(borrow)} {
    $btop configure -background plum
}
