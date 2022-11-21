# Traçado de Solo
*Biblioteca em Python para traçado de solo de órbitas fechadas. Parte da disciplina de Mecânica do Voo Espacial da Universidade Federal de Santa Catarina*

## Sobre (TODO)

## Dependências
```
Python >= 3.0
Scipy
Gnuplot >= 5.0
```

## Instalação

### Linux

**Dependências**
```
pip install --user numpy scipy
# debian distros
sudo apt install gnuplot
# fedora distros
sudo dnf install gnuplot
# suse distros
sudo zypper in gnuplot
# arch distros
sudo pacman -S gnuplot
# gentoo
sudo emerge -av gnuplot
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
![alt text](./example/iss.png?raw=true)
### Traçado de solo da Molnyia
![alt text](./example/molnyia.png?raw=true)

## Contato

Arthur Gabardo - <arthur.miguel@grad.ufsc.br>

Github - <https://github.com/arthur-miguel/ground_track>

Agradecimentos ao [Prof. Helton Gaspar da Silva](https://helton.paginas.ufsc.br/) pelo script do Gnuplot
