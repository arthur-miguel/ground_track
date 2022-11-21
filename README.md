# Traçado de Solo


## Dependencias
```
Python >= 3.0
Gnuplot >= 5.0
```

## Instalação

### Linux
```
pip install --user numpy scipy
sudo apt install gnuplot
git clone https://github.com/arthur-miguel/mec_voo.git
```

## Exemplos
```python
orb1 = Orbita(semieixo, excentricidade, inclinação, long. do periapse, arg. periapse) # veja arquivo gorundtrack.py para mais opções
t = np.linspace(0, orb1.period) # cria uma serie temporal no ontervalo de um periodo da orb1
orb1.evaluate(t) # calcula a trajetoria e traçado de solo da orb1 no tempo t
orb1.save_data("orb1.txt") # salva os dados calculados no arquivo orb1.txt
orb1.plot_track() # gera um plot com o traçao de solo
```
O arquivo `teste.py` possui exemplos do traçado da ISS e Molnya durante o curso de um dia. Para executar os script basta dar o seguinte comando

```
python teste.py
```
