#!/usr/bin/gnuplot
reset
####################################################################################################
#
#  Script de gnupot para a disciplina de Mecânica do voo espacial
#  Plota o traçado de solo em função da latitude e longitude
#
#  Autor: Prof. Helton da Silva Gaspar
#  Data:  01 / 11 / 2018
#
#  Adaptado a partir do script 'Plotting Antarctica' elaborado por:
#       AUTHOR: Hagen Wierstorf
#       VERSION: gnuplot 4.6 patchlevel 0
#
####################################################################################################


####################################################################################################
#
## Parâmetros ajustáveis:

 dados = filename; # nome do arquivo de dados de longitude e latitude em função do tempo
 tempo = 1;             # número da coluna do arquivo de dados com o tempo
 lon = 8;               # número da coluna do arquivo de dados com a longitude
 lat = 9;               # número da coluna do arquivo de dados com a latitude
 
 xtempo = delta_t;          # fator de conversão do tempo de sua série para minutos
 
 
 ps0 = 0.5;             # Tamanho padrão do ponto
 psH = 2.0;             # Tamanho do ponto em hora cheia
 
 #Legenda do eixo X
 set xlabel 'longitude (graus)'; # Comente esta linha com '#' para remover a legenda do eixo X
 
 #Legenda do eixo Y
 set ylabel 'latitude (graus)';  # idem ao comando anterior
 
####################################################################################################
#
## funções auxiliares

 wrap( x, xmin, xmax) = x<xmin?wrap(x+xmax-xmin,xmin,xmax):x>xmax?wrap(x-xmax+xmin,xmin,xmax):x;

 t0=0;
 hourflip(t0,t)      = ( int(t/60)-int(t0/60) )>0?(0*(t0=t)+1):0;
 pontohora(row,t0,t) = ( row==0||hourflip(t0,t)>0 )?( 0*(t0=t)+psH ):ps0;
 horario(row,t0,t)   = ( row==0||hourflip(t0,t)>0 )?( sprintf( "%d:%02d", (h=int(t/60)), t-h*60+0*(t0=t)) ):""
 
####################################################################################################


# color definitions
set border lw 1.5
set style line 1 lc rgb 'gray' lt 1 lw 1
set style line 2 lc rgb 'black' lt 1 lw 1

unset key
set border 0

set xtics -180,30,180 out
set mxtics 2

set ytics -90,45,90 out
set mytics 3

set size ratio -1

set grid x y mx my lt 0 dt '.' lw 1 lc rgb 'grey70'

#set lmargin 0
set rmargin 2
set tmargin 0
set bmargin 0

set xrange [-180:180]
set yrange [-90:90]

set term png enhanced size 1024,768

set output outputfile

plot 'world_110m' i 0 w filledcu ls 1, \
     ''               i 1 w filledcu x1 ls 1, \
     ''               w l ls 2,\
     dados u (wrap(column(lon),-180,180)  ):(wrap(column(lat),-90,90)):( pontohora($0,t0,xtempo*column(tempo)) ) w p pt 7 ps var lc rgb 'orangered' ,\
     dados u (wrap(column(lon),-180,180)  ):(wrap(column(lat),-90,90)):( horario($0,t0,xtempo*column(tempo)) ) w labels right offset 0,0.8 tc rgb 'brown'
set output


print sprintf("\n  Rota de solo gerada com sucesso no arquivo '%s'!\n", outputfile );


exit

set output 'world110m_filledcurves1.png'
plot 'world_110m' w filledcu ls 1, \
     ''               w l ls 2

set output 'world110m_filledcurves2.png'
plot 'world_110m' i 0 w filledcu ls 1, \
     ''               i 1 w filledcu x1 ls 1, \
     ''               w l ls 2
