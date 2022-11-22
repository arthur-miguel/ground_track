# Traçado de Solo
*Biblioteca em Python para traçado de solo de órbitas fechadas. Parte da disciplina de Mecânica do Voo Espacial da Universidade Federal de Santa Catarina*

## Sobre

A biblioteca `ground_track` inclui o template da classe `Orbit` e seus métodos que permitem a realização do estudo da cinemática de órbitas keplerianas e de problemas de dois corpos.

A forma mais básica de incializar uma órbita é passando o semieixo maior e excentricidade para seu construtor:
```python
orb_eq = Orbit(42157, 0)
```
também podem ser passados como parâmetros para construção de uma órbita: inclinação, longitude do nó ascendende, argumento do periapse, época, unidade de tempo (segundos, minutos, ...), passo de tempo para simulação e parâmetro gravitacional padrão (mu) em km^3/s^2

Para o cálculo da cinemática da órbita, usa-se a função `evaluate`
```python
orb_eq.evaluate(0, orb_eq.period) # início e fim do intervalo de tempo que se quer avaliar
```
além do campo `period`, outras propriedades da órbita podem ser facilmente acessadas como `apoapsis`, `periapsis`, `ang_moment` e `c3`.

É possivel salvar todos os dados em um arquivo texto por meio da função `Orbit.save_data("nome_do_arquivo")`. É necessário salvar esse arquivo para usar os métodos de plotagem da biblioteca.

Outra funcionalidade da biblioteca é a de plotar tanto o traçado de solo quanto a Órbita em três dimensões por meio dos comandos `Orbit.plot_track()` (como parâmetro opcional é possivel passar o nome do arquivo de saída da função `plot_track()`) e `Orbit.plot_3D()`, respectivamente.

Para acessar o valor das anomalias em função do tempo e velocidades, raio da órbita e ângulo de voo em função da anomalia verdadeira estão à disposição as funções `*_at`, como por exemplo:

```python
orb_eq.M_at(tempo)
orb_eq.E_at(tempo)
orb_eq.f_at(tempo)
orb_eq.r_at(anomalia)
orb_eq.v_at(anomalia)
orb_eq.gamma_at(anomalia)
```
para mais detalhes sobre a utilização da biblioteca veja a seção exemplos.

## Dependências
```
Python >= 3.0
Scipy
Gnuplot >= 5.0
```

## Instalação

### Linux

**Dependências**
```sh
pip install --user numpy scipy
# debian distros
sudo apt install gnuplot # para outras distros consulte seu package manager
```
**Código-fonte**
```
git clone https://github.com/arthur-miguel/ground_track.git
```

### Windows

<iframe width="1166" height="656" src="https://www.youtube.com/embed/7ehOTj8OzLk" title="Instalação Biblioteca P2C-Windows" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

1º Instalar Gnuplot através do link: [Gnuplot](https://sourceforge.net/projects/gnuplot/files/gnuplot/)

2ª Instalar o Python;

3ª Instalar Scipy; 

4ª Clonar o repositório.

## Exemplos
O arquivo [`teste.py`](./src/teste.py) possui exemplos e instruções para utilização da biblioteca, fique a vontade para modificá-lo como bem entender e experimentar diferentes parâmetros. Para usá-lo basta emitir o seguinte comando em seu respectivo diretório:
```
python teste.py
```
### Construção do objeto `Orbit`
```python
molnyia = Orbit( 26600,  #major semiaxis
                 0.74,   #eccentricity
                 63.4,   #inclination
                 80,     #accending node
                 270     #periapsis argument
               )
molnyia.evaluate(0, 2*molnyia.period)   # evaluates orbit at two periods
```

### Parâmetros da órbita
**entrada**
```python
Q = molnyia.apoapsis		            # gets orbit apoapsis
q = molnyia.periapsis		            # gets orbit periapsis
energy = molnyia.c3		              # gets orbit specific energy
moment = molnyia.ang_moment	        # gets orbit specific moment
```
**saída**
```
Molnyia parameters
Apoapsis:  46284.0
Periapsis:  6916.0
Specific moment:  69258.130381927
Specific energy:  -0.13346713497240342
```

### Tempo de voo
**entrada**
```python
tQ     = molnyia.period/2
vQ     = molnyia.v_at(180)	          # gets velocity at apoapsis
gammaQ = molnyia.gamma_at(180)        # gets flight angle at apoapsis
vq     = molnyia.v_at(0)	            # gets velocity at periapsis
gammaq = molnyia.gamma_at(0)	        # gets flight angle at periapsis

t1     = molnyia.period*0.17
f1     = molnyia.f_at(t1)             # gets true anomaly at a quarter of period
r1     = molnyia.r_at(f1)             # gets radius at a quarter of period
v1     = molnyia.v_at(f1)		          # gets velocity at a quarter of period
gamma1 = molnyia.gamma_at(f1)		      # gets flight angle at a quarter of period

t2     = molnyia.period*0.33
f2     = molnyia.f_at(t2)             # gets true anomaly at a quarter of period
r2     = molnyia.r_at(f2)             # gets radius at a quarter of period
v2     = molnyia.v_at(f2)		          # gets velocity at a quarter of period
gamma2 = molnyia.gamma_at(f2)		      # gets flight angle at a quarter of period
```
**saída**
```
Time of flight
Time     True anomaly    Radius     Velocity   Flight angle
0.0      0               6916.0     10.01      0.0
2.04     145.57          30887.51   3.29       47.04
3.96     165.61          42489.42   1.94       33.0
6.0      180             46284.0    1.5        0.0
```

### Traçado de solo da ISS (`plot_track()`)
![alt text](./examples/iss.png?raw=true)

### Órbita ISS 3D (`plot_3D()`)
![alt text](./examples/iss_3D.png?raw=true)

### Traçado de solo da Molnyia (`plot_track()`)
![alt text](./examples/molnyia.png?raw=true)

### Órbita Molnyia 3D (`plot_3D()`)
![alt text](./examples/molnyia_3D.png?raw=true)

## Contato

Arthur Gabardo - <arthur.miguel@grad.ufsc.br>

Github - <https://github.com/arthur-miguel/ground_track>

Agradecimentos ao [Prof. Helton da Silva Gaspar](https://helton.paginas.ufsc.br/) pelo script do Gnuplot
