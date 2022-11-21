reset

set parametric
set view equal xyz
set hidden3d
unset colorbox

set xlabel "x [Rt]"
set ylabel "y [Rt]"
set zlabel "z [Rt]"

set isosample 31,31

Rt = 6371

splot filename u ($5)/Rt:($6)/Rt:($7)/Rt title "Orbit", \
	cos(u)*cos(v), cos(u)*sin(v), sin(u) title "" w l lc "blue"

pause -1