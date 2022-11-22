# Traçado de Solo
*Biblioteca em Python para traçado de solo de órbitas fechadas. Parte da disciplina de Mecânica do Voo Espacial da Universidade Federal de Santa Catarina*

## Sobre

A biblioteca `ground_track` inclui o tamplate da classe `Orbit` e seus metodos que permitem a realização do estudo da cinematica de órbitas keplerianas e de problemas de dois corpos.

A forma mais basica de incializar uma orbita é passando o semieixo maior e excentricidade para seu construtor:
```python
orb_eq = Orbit(42157, 0)
```
também podem ser passados como parametros para construção de uma orbita sua inclinação, longitude do nó ascendende, argumento do periapse, época, unidade de tempo (segundos, minutos, ...), passo de tempo para simulação e parametro gravitacional padrão (mu) em km^3/s^2

Para o calculo da cienematica da órbita usa-se a função `evaluate`
```python
orb_eq.evaluate(0, orb_eq.period) # inicio e fim do intervalo de tempo que se quer avaliar
```
além do campo `period` outras propriedades da órbita podem ser facilmente acessadas como `apoapsis`, `periapsis`, `ang_moment` e `c3`.

É possivel salvar todos os dados em um arquivo texto por meio da função `Orbit.save_data("nome_do_arquivo")`, é necessario salvar esse arquivo para usar os metodos de plotagem da biblioteca.

Outra funcionalidade da biblioteca é a de plotar tanto o traçado de solo quanto a orbita em tres dimensões por meio dos comandos `Orbit.plot_track()` (como parametro opcional é possivel passar o nome do arquivo de saida da função `plot_track()`) e `Orbit.plot_3D()` respectivamente.

Para acessar o valor das anolias em função do tempo e velocidades, raio da orbita e angulo de voo em função da anomalia verdadeira estão a disposição as funções `*_at`, como por exemplo:

```python
Orbit.M_at(tempo)
Orbit.E_at(tempo)
Orbit.f_at(tempo)
Orbit.r_at(anomalia)
Orbit.v_at(anomalia)
Orbit.gamma_at(anomalia)
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

1º Instalar Gnuplot através do link: [Gnuplot](https://sourceforge.net/projects/gnuplot/files/gnuplot/)

2ª Instalar o Python;

3ª Instalar Scipy;

4ª Clonar o repositório.

## Exemplos
O arquivo [`teste.py`](./src/teste.py) possui exemplos e instrucoes para utilizacao da biblioteca, fique a vontade para modifica-lo como bem entender e experimentar diferentes parametros, para usa-lo basta emitir o seguinte comando em seu respectivo diretorio:
```
python teste.py
```
### Construcao do objeto `Orbit`
```python
molnyia = Orbit( 26600,  #major semiaxis
                 0.74,   #eccentricity
                 63.4,   #inclination
                 80,     #accending node
                 270     #periapsis argument
               )
molnyia.evaluate(0, 2*molnyia.period)   # evaluates orbit at two periods
```

### Parametros da orbita
**entrada**
```python
Q = molnyia.apoapsis		            # gets orbit apoapsis
q = molnyia.periapsis		            # gets orbit periapsis
energy = molnyia.c3		              # gets orbit specific energy
moment = molnyia.ang_moment	        # gets orbit specific moment
```
**saida**
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
**saida**
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

### Orbita ISS 3D (`plot_3D()`)
![alt text](./examples/iss_3D.png?raw=true)

### Traçado de solo da Molnyia (`plot_track()`)
![alt text](./examples/molnyia.png?raw=true)

### Orbita Molnyia 3D (`plot_3D()`)
![alt text](./examples/molnyia_3D.png?raw=true)

## Contato

Arthur Gabardo - <arthur.miguel@grad.ufsc.br>

Github - <https://github.com/arthur-miguel/ground_track>

Agradecimentos ao [Prof. Helton da Silva Gaspar](https://helton.paginas.ufsc.br/) pelo script do Gnuplot
