import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


paths = [
    '/Users/icaroprobo/Desktop/absorption/D0.txt',
    '/Users/icaroprobo/Desktop/absorption/D1.txt',
    '/Users/icaroprobo/Desktop/absorption/D2.txt',
    '/Users/icaroprobo/Desktop/absorption/D3.txt'
]

paths_emissao = [
    '/Users/icaroprobo/Desktop/excitations/D0_new.txt',
    '/Users/icaroprobo/Desktop/excitations/D1_new.txt',
    '/Users/icaroprobo/Desktop/excitations/D2_new.txt',
    '/Users/icaroprobo/Desktop/excitations/D3_new.txt'
]

dados = []
dados_emissao = []

for i in range(4):
    data = pd.read_csv(paths[i], 
                       sep=r',', 
                       header=None,
                       skiprows = 2,
                       names = ['wavelength', 'absorbance'],
                       encoding='cp932')
    dados.append(data)

    print(f'D{i}')
    print(data.head())

for i in range(4):
    data = pd.read_csv(
        paths_emissao[i],
        sep=r'\s+',
        header=None,
        skiprows=13,  
        names=['wavelength', 'intensity'],
        encoding='latin1'
    )

    dados_emissao.append(data)

    print(f'Emissão D{i}')
    print(data.head())

plt.figure(figsize=(10, 6))

for i in range(4):
    plt.plot(
        dados_emissao[i]['wavelength'],
        dados_emissao[i]['intensity'],
        label=f'D{i}'
    )

plt.xlabel('Wavelength (nm)')
plt.ylabel('Emission intensity (a.u.)')
plt.title('Emission spectra of cyanine dyes')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# Comprimento de onda do pico de cada corante
intervalos = [
    (380, 460),  # D0
    (510, 590),  # D1
    (610, 690),  # D2
    (710, 810)   # D3
]

resultados = []

for i in range(4):
    minimo, maximo = intervalos[i]
    data = dados[i]

    banda = data[
        (data['wavelength'] >= minimo) &
        (data['wavelength'] <= maximo)
    ]

    indice = banda['absorbance'].idxmax()

    lambda_max = banda.loc[indice, 'wavelength']
    absorbancia_max = banda.loc[indice, 'absorbance']

    resultados.append({
        'Corante': f'D{i}',
        'lambda_max (nm)': lambda_max,
        'Absorbancia_max': absorbancia_max,
        'Energia (eV)': 1239.84 / lambda_max
    })

tabela = pd.DataFrame(resultados)

print('\nPicos de absorção:')
print(tabela.to_string(index=False))

picos_emissao = []

for i in range(4):
    data = dados_emissao[i]
    indice = data['intensity'].idxmax()
    picos_emissao.append(data.loc[indice, 'wavelength'])

resumo = pd.DataFrame({
    'Corante': tabela['Corante'],
    'Absorcao (nm)': tabela['lambda_max (nm)'],
    'Emissao (nm)': picos_emissao,
    'E_abs (eV)': tabela['Energia (eV)'],
    'E_em (eV)': 1239.84 / np.array(picos_emissao)
})

print('\nPicos de absorção e emissão:')
print(resumo.to_string(
    index=False,
    formatters={
        'Absorcao (nm)': '{:.0f}'.format,
        'Emissao (nm)': '{:.0f}'.format,
        'E_abs (eV)': '{:.3f}'.format,
        'E_em (eV)': '{:.3f}'.format
    }
))

# Comprimento da cadeia conjugada
comprimento_simples = 1.54  # Å
comprimento_dupla = 1.34   # Å

comprimento_medio = (comprimento_simples + comprimento_dupla) / 2
R = comprimento_medio * np.cos(np.deg2rad(30))

duplas = np.array([2, 3, 4, 5])  # D0, D1, D2, D3
ligacoes = 2 * duplas

L_angstrom = ligacoes * R
L_metros = L_angstrom * 1e-10

# Número de elétrons π
N_pi = 2 * duplas + 2

estrutura = pd.DataFrame({
    'Corante': ['D0', 'D1', 'D2', 'D3'],
    'Duplas': duplas,
    'Ligacoes': ligacoes,
    'Eletrons_pi': N_pi,
    'L (angstrom)': L_angstrom,
    'L (nm)': L_angstrom / 10
})

print(estrutura.to_string(index=False))



plt.figure(figsize = (10, 6))

for i in range(4):
    wavelenght = dados[i].iloc[:, 0]
    absorbance = dados[i].iloc[:, 1]

    plt.plot(wavelenght, absorbance, label=f'D{i}')

plt.xlabel('Wavelength (nm)')
plt.ylabel('Absorbance')
plt.title('Absorption spectra of cyanine dyes')
plt.legend()
plt.grid(alpha = 0.3)
plt.tight_layout()
plt.show()

# Item 7: comparação entre absorção e emissão normalizadas

limites = [
    (350, 650),  # D0
    (480, 750),  # D1
    (580, 850),  # D2
    (680, 900)   # D3
]

fig, eixos = plt.subplots(2, 2, figsize=(12, 8))

for i in range(4):
    ax = eixos.flat[i]

    absorcao = dados[i]
    emissao = dados_emissao[i]

    A_norm = absorcao['absorbance'] / absorcao['absorbance'].max()
    I_norm = emissao['intensity'] / emissao['intensity'].max()

    ax.plot(
        absorcao['wavelength'], A_norm,
        label='Absorption', color='tab:blue'
    )

    ax.plot(
        emissao['wavelength'], I_norm,
        label='Emission', color='tab:red'
    )
    ax.set_ylim(-0.05, 1.10)
    ax.set_title(f'D{i}')
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Normalized signal')
    ax.set_xlim(*limites[i])
    ax.legend()
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.show()