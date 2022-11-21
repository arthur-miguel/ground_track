# Traçado de Solo
*Biblioteca em Python para traçado de solo de órbitas fechadas. Parte da disciplina de Mecânica do Voo Espacial da Universidade Federal de Santa Catarina*

## Sobre (TODO)

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

### Windows (TODO)

## Exemplos
```python
orb1 = Orbit(semieixo, excentricidade, inclinação, long. do periapse, arg. periapse) # veja arquivo gorundtrack.py para mais opções
orb1.evaluate(0, orb1.period) # calcula a trajetoria e traçado de solo da orb1 no tempo de um periodo
orb1.save_data("orb1.txt") # salva os dados calculados no arquivo orb1.txt
orb1.plot_track() # gera um plot com o traçao de solo
```
O arquivo `teste.py` possui exemplos do traçado da ISS e Molnya durante o curso de um dia. Para executar o script basta emitir o seguinte comando em seu diretório:

```
python teste.py
```
### Traçado de solo da ISS
![alt text](./examples/iss.png?raw=true)

### Orbita ISS 3D
![alt text](./examples/iss_3D.png?raw=true)

### Traçado de solo da Molnyia
![alt text](./examples/molnyia.png?raw=true)

### Orbita Molnyia 3D
![alt text](./examples/molnyia_3D.png?raw=true)

## Contato

Arthur Gabardo - <arthur.miguel@grad.ufsc.br>

Github - <https://github.com/arthur-miguel/ground_track>

Agradecimentos ao [Prof. Helton Gaspar da Silva](https://helton.paginas.ufsc.br/) pelo script do Gnuplot
