
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# ==========================================
# 1. Leitura dos dados experimentais
# ==========================================

path = '/Users/icaroprobo/Desktop/物理学実験icaro_data.txt'

data = pd.read_csv(
    path,
    sep=r'\s+',
    skiprows=1,
    header=None,
    usecols=[0, 1],
    names=['wavenumber', 'Transmittance']
)

data = data.apply(pd.to_numeric, errors='coerce').dropna()
data = data.sort_values('wavenumber')

# ==========================================
# 2. Gráfico original de transmitância
# ==========================================

plt.figure(figsize=(10, 6))

plt.plot(
    data['wavenumber'],
    data['Transmittance'],
    color='blue',
    linewidth=1
)

plt.title('HCl Transmittance Spectrum')
plt.xlabel('Wavenumber (cm$^{-1}$)')
plt.ylabel('Transmittance (%)')

plt.xlim(2600, 3100)
plt.ylim(70, 110)
plt.grid(True)

plt.savefig(
    '/Users/icaroprobo/Desktop/transmittance_plot.png',
    dpi=300
)
plt.show()

# ==========================================
# 3. Conversão para absorbância
# ==========================================

data = data[data['Transmittance'] > 0].copy()

data['Absorbance'] = -np.log10(
    data['Transmittance'] / 100
)

plt.figure(figsize=(10, 6))

plt.plot(
    data['wavenumber'],
    data['Absorbance'],
    color='blue',
    linewidth=1
)

plt.title('HCl Absorption Spectrum')
plt.xlabel('Wavenumber (cm$^{-1}$)')
plt.ylabel('Absorbance')

plt.xlim(2600, 3100)
plt.grid(True)

plt.savefig(
    '/Users/icaroprobo/Desktop/absorbance_plot.png',
    dpi=300
)
plt.show()


# ==========================================
# 4. Duas lorentzianas + background linear
# ==========================================

def lorentz(x, xc, S, gamma):
    return (S / np.pi) * (gamma / 2) / (
        (x - xc)**2 + (gamma / 2)**2
    )

x_ref = 2906.0

def double_lorentz(x, xc1, S1, g1, xc2, S2, g2, a, b):
    background = a + b * (x - x_ref)

    return (
        background
        + lorentz(x, xc1, S1, g1)
        + lorentz(x, xc2, S2, g2)
    )

# ==========================================
# 5. Seleção dos dados
# ==========================================

x_min = 2902.5
x_max = 2909.5

peak_data = data[
    (data['wavenumber'] >= x_min) &
    (data['wavenumber'] <= x_max)
]

x = peak_data['wavenumber'].to_numpy()
y = peak_data['Absorbance'].to_numpy()

# Estimativas iniciais dos dois picos
p0 = [
    2904.4, 0.01, 0.5,
    2906.5, 0.06, 0.6,
    0.025, -0.003
]

lower = [
    2903.8, 0, 0.05,
    2905.8, 0, 0.05,
    -np.inf, -np.inf
]

upper = [
    2905.0, np.inf, 3,
    2907.2, np.inf, 3,
    np.inf, np.inf
]

params, covariance = curve_fit(
    double_lorentz,
    x, y,
    p0=p0,
    bounds=(lower, upper),
    maxfev=30000
)

xc1, S1, g1, xc2, S2, g2, a, b = params

# ==========================================
# 6. Resultados
# ==========================================

print("=== Isotopic Peak Fitting ===")

print("\nPeak 1 (possible H37Cl)")
print(f"Center: {xc1:.4f} cm^-1")
print(f"Area: {S1:.6f}")
print(f"FWHM: {g1:.4f} cm^-1")

print("\nPeak 2 (possible H35Cl)")
print(f"Center: {xc2:.4f} cm^-1")
print(f"Area: {S2:.6f}")
print(f"FWHM: {g2:.4f} cm^-1")

print(f"\nArea ratio H35/H37: {S2/S1:.3f}")

# ==========================================
# 7. Visualização
# ==========================================

x_fit = np.linspace(x_min, x_max, 1000)

background = a + b * (x_fit - x_ref)

peak1 = lorentz(x_fit, xc1, S1, g1)
peak2 = lorentz(x_fit, xc2, S2, g2)

total = background + peak1 + peak2

plt.figure(figsize=(10, 6))

plt.scatter(x, y, s=18, color='black',
            label='Experimental data')

plt.plot(x_fit, total, color='red',
         linewidth=2, label='Total fit')

plt.plot(x_fit, background + peak1,
         '--', label='Peak 1 + background')

plt.plot(x_fit, background + peak2,
         '--', label='Peak 2 + background')

plt.plot(x_fit, background, ':',
         color='gray', label='Background')

plt.xlabel('Wavenumber (cm$^{-1}$)')
plt.ylabel('Absorbance')
plt.title('HCl - Double Lorentzian Fit')
plt.grid(True)
plt.legend()
plt.show()



# ==========================================
# 8. Identificação dos picos do HCl
# ==========================================

from scipy.signal import find_peaks, savgol_filter

# Região do espectro a analisar
region = data[
    (data['wavenumber'] >= 2650) &
    (data['wavenumber'] <= 3050)
].copy()

x_all = region['wavenumber'].to_numpy()
y_all = region['Absorbance'].to_numpy()

# Suavização leve para reduzir o ruído
y_smooth = savgol_filter(
    y_all,
    window_length=5,
    polyorder=2
)

# Distância mínima entre picos
dx = np.median(np.diff(x_all))
min_distance = max(1, int(np.ceil(0.9 / dx)))

# Detecção dos máximos locais
peaks, properties = find_peaks(
    y_smooth,
    prominence=0.008,
    distance=min_distance
)

# Construção da tabela de picos candidatos
peak_table = pd.DataFrame({
    'Peak ID': np.arange(1, len(peaks) + 1),
    'Wavenumber': x_all[peaks],
    'Absorbance': y_all[peaks],
    'Prominence': properties['prominences']
})

print("=== Detected Peak Candidates ===")
print(peak_table.to_string(index=False))

# ==========================================
# 9. Gráfico com os picos identificados
# ==========================================

plt.figure(figsize=(14, 7))

plt.plot(
    x_all, y_all,
    color='blue',
    linewidth=1,
    label='Experimental spectrum'
)

plt.scatter(
    x_all[peaks],
    y_all[peaks],
    color='red',
    s=25,
    zorder=3,
    label='Detected peaks'
)

# Identificação numérica de cada pico
for i, p in enumerate(peaks):
    plt.annotate(
        str(i + 1),
        (x_all[p], y_all[p]),
        xytext=(0, 7),
        textcoords='offset points',
        ha='center',
        fontsize=8
    )

plt.xlabel('Wavenumber (cm$^{-1}$)')
plt.ylabel('Absorbance')
plt.title('HCl - Peak Detection')

plt.grid(True)
plt.legend()

plt.savefig(
    '/Users/icaroprobo/Desktop/HCl_detected_peaks.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()



# ==========================================
# 10. Ajuste dos pares isotópicos
# ==========================================

# Centros estimados a partir de find_peaks
# Formato: ramo, J, H37Cl, H35Cl

pairs = [
    ('P', 6, 2750.58288, 2752.27065),
    ('P', 5, 2774.21166, 2775.89943),
    ('P', 4, 2797.11711, 2799.04599),
    ('P', 3, 2819.78145, 2821.71033),
    ('P', 2, 2841.96357, 2843.89245),
    ('P', 1, 2863.42236, 2865.35124),
    ('R', 0, 2904.41106, 2906.58105),
    ('R', 1, 2923.94097, 2926.11096),
    ('R', 2, 2942.98866, 2945.15865),
    ('R', 3, 2961.31302, 2963.48301),
    ('R', 4, 2979.15516, 2981.32515),
    ('R', 5, 2996.03286, 2998.20285),
    ('R', 6, 3012.42834, 3014.83944),
    ('R', 7, 3028.10049, 3030.27048)
]

results = []
pair_results = []

fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(
    data['wavenumber'],
    data['Absorbance'],
    color='lightgray',
    linewidth=1,
    label='Experimental spectrum'
)

for branch, J, c37, c35 in pairs:

    # Janela local do par isotópico
    xmin = c37 - 3.2
    xmax = c35 + 3.2

    subset = data[
        (data['wavenumber'] >= xmin) &
        (data['wavenumber'] <= xmax)
    ]

    xx = subset['wavenumber'].to_numpy()
    yy = subset['Absorbance'].to_numpy()

    if len(xx) < 12:
        print(f"Poucos dados em {branch}({J})")
        continue

    xmid = (c37 + c35) / 2

    # Modelo: duas lorentzianas + fundo linear
    def model(x, xc37, S37, xc35, S35, gamma, a, b):

        bg = a + b * (x - xmid)

        return (
            bg
            + lorentz(x, xc37, S37, gamma)
            + lorentz(x, xc35, S35, gamma)
        )

    # Background inicial
    left = np.median(yy[:4])
    right = np.median(yy[-4:])

    b0 = (right - left) / (xx[-1] - xx[0])
    a0 = left + b0 * (xmid - xx[0])

    # Estimativas de altura e área
    g0 = 0.9

    h37 = max(
        np.interp(c37, xx, yy)
        - (a0 + b0*(c37-xmid)),
        0.001
    )

    h35 = max(
        np.interp(c35, xx, yy)
        - (a0 + b0*(c35-xmid)),
        0.001
    )

    S37_0 = np.pi * g0 * h37 / 2
    S35_0 = np.pi * g0 * h35 / 2

    
    p0 = [
    c37, S37_0,
    c35, S35_0,
    g0, a0, b0
    ]

    lower = [
    c37 - 0.8, 0,
    c35 - 0.8, 0,
    0.45, -np.inf, -np.inf
    ]

    upper = [
    c37 + 0.8, np.inf,
    c35 + 0.8, np.inf,
    1.6, np.inf, np.inf
    ]

    try:
        params, cov = curve_fit(
            model,
            xx, yy,
            p0=p0,
            bounds=(lower, upper),
            maxfev=30000
        )

    except (RuntimeError, ValueError) as e:
        print(f"Falha no ajuste {branch}({J}): {e}")
        continue

    xc37, S37, xc35, S35, gamma, a, b = params

    g37 = gamma
    g35 = gamma

    residuals = yy - model(xx, *params)
    rmse = np.sqrt(np.mean(residuals**2))

    # Salvar parâmetros de cada linha
    for isotope, xc, S, gamma in [
        ('H37Cl', xc37, S37, g37),
        ('H35Cl', xc35, S35, g35)
    ]:
        results.append({
            'Branch': branch,
            'J': J,
            'Isotope': isotope,
            'Center_cm-1': xc,
            'Area_cm-1': S,
            'FWHM_cm-1': gamma,
            'RMSE': rmse
        })

    pair_results.append({
        'Branch': branch,
        'J': J,
        'Area_ratio_35_37': S35 / S37
    })

    # Desenhar o fitting de cada região
    xf = np.linspace(xmin, xmax, 300)

    ax.plot(
        xf,
        model(xf, *params),
        linewidth=1.5
    )

# ==========================================
# 11. Tabela dos resultados
# ==========================================

results_df = pd.DataFrame(results)
ratios_df = pd.DataFrame(pair_results)

print("\n=== Lorentzian Fit Results ===")

print(
    results_df.to_string(
        index=False,
        float_format=lambda v: f'{v:.5f}'
    )
)

print("\n=== Isotopic Area Ratios ===")
print(ratios_df.to_string(index=False))

print(
    "\nMedian area ratio:",
    ratios_df['Area_ratio_35_37'].median()
)

# Salvar em CSV
results_df.to_csv(
    '/Users/icaroprobo/Desktop/HCl_all_peaks.csv',
    index=False
)

ratios_df.to_csv(
    '/Users/icaroprobo/Desktop/HCl_isotope_ratios.csv',
    index=False
)

# ==========================================
# 12. Gráfico final
# ==========================================

ax.set_xlim(2700, 3050)
ax.set_ylim(-0.015, 0.18)

ax.set_xlabel('Wavenumber (cm$^{-1}$)')
ax.set_ylabel('Absorbance')
ax.set_title('HCl - Lorentzian Fits')

ax.grid(True)
ax.legend()

plt.savefig(
    '/Users/icaroprobo/Desktop/HCl_all_fits.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()


# ==========================================
# 13. Teste de fitting com largura comum
# ==========================================

c37 = 2904.41106
c35 = 2906.58105

x_ref = (c37 + c35) / 2

def pair_model(x, xc37, S37, xc35, S35,
               gamma, a, b):

    background = a + b * (x - x_ref)

    return (
        background
        + lorentz(x, xc37, S37, gamma)
        + lorentz(x, xc35, S35, gamma)
    )

# Comparar diferentes janelas
for margin in [2.0, 2.5, 3.2]:

    subset = data[
        (data['wavenumber'] >= c37-margin) &
        (data['wavenumber'] <= c35+margin)
    ]

    xx = subset['wavenumber'].to_numpy()
    yy = subset['Absorbance'].to_numpy()

    # Background inicial estimado nas bordas
    edge_x = np.r_[xx[:5], xx[-5:]]
    edge_y = np.r_[yy[:5], yy[-5:]]

    slope, intercept = np.polyfit(
        edge_x - x_ref, edge_y, 1
    )

    # Estimativas iniciais das áreas
    gamma0 = 1.0

    h37 = max(
        np.interp(c37, xx, yy)
        - (intercept + slope*(c37-x_ref)),
        0.001
    )

    h35 = max(
        np.interp(c35, xx, yy)
        - (intercept + slope*(c35-x_ref)),
        0.001
    )

    p0 = [
        c37, np.pi*h37*gamma0/2,
        c35, np.pi*h35*gamma0/2,
        gamma0, intercept, slope
    ]

    lower = [
        c37-0.55, 0,
        c35-0.55, 0,
        0.45, -np.inf, -np.inf
    ]

    upper = [
        c37+0.55, np.inf,
        c35+0.55, np.inf,
        1.6, np.inf, np.inf
    ]

    params, cov = curve_fit(
        pair_model,
        xx, yy,
        p0=p0,
        bounds=(lower, upper),
        maxfev=30000
    )

    xc37, S37, xc35, S35, gamma, a, b = params

    residuals = yy - pair_model(xx, *params)
    rmse = np.sqrt(np.mean(residuals**2))

    print(f"\nMargin: {margin}")
    print(f"H37Cl center: {xc37:.4f}")
    print(f"H35Cl center: {xc35:.4f}")
    print(f"Common FWHM: {gamma:.4f}")
    print(f"Area ratio: {S35/S37:.4f}")
    print(f"RMSE: {rmse:.6f}")

    # Visualizar a janela intermediária
    if margin == 2.5:

        xf = np.linspace(xx.min(), xx.max(), 1000)
        yf = pair_model(xf, *params)
        bg = a + b*(xf-x_ref)

        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(9, 7),
            sharex=True,
            gridspec_kw={'height_ratios': [3, 1]}
        )

        ax1.scatter(xx, yy, s=20,
                    color='black', label='Data')
        ax1.plot(xf, yf, color='red',
                 label='Total fit')
        ax1.plot(xf, bg, '--',
                 color='gray', label='Background')

        ax1.plot(
            xf, bg + lorentz(xf, xc37, S37, gamma),
            '--', label='H37Cl'
        )

        ax1.plot(
            xf, bg + lorentz(xf, xc35, S35, gamma),
            '--', label='H35Cl'
        )

        ax1.set_ylabel('Absorbance')
        ax1.legend()
        ax1.grid(True)

        ax2.scatter(xx, residuals, s=20,
                    color='black')
        ax2.axhline(0, color='red', linestyle='--')
        ax2.set_xlabel('Wavenumber (cm$^{-1}$)')
        ax2.set_ylabel('Residual')
        ax2.grid(True)

        plt.tight_layout()
        plt.show()


# ==========================================
# 14. 解析④ - Massa reduzida do HCl
# ==========================================

u = 1.6605402e-27  # kg

# Massas atômicas em unidades u
m_H = 1.007825
m_Cl35 = 34.968853
m_Cl37 = 36.965903

# Função para calcular a massa reduzida
def reduced_mass(m1, m2):
    return (m1 * m2) / (m1 + m2)

# Massas reduzidas em u
mu35_u = reduced_mass(m_H, m_Cl35)
mu37_u = reduced_mass(m_H, m_Cl37)

# Conversão para kg
mu35 = mu35_u * u
mu37 = mu37_u * u

print("\n=== Reduced Mass ===")
print(f"H35Cl: {mu35_u:.6f} u")
print(f"H35Cl: {mu35:.6e} kg")

print(f"H37Cl: {mu37_u:.6f} u")
print(f"H37Cl: {mu37:.6e} kg")



# ==========================================
# 15. 解析⑤ - Abundância isotópica
# ==========================================

# Mediana das razões entre áreas
ratio = ratios_df['Area_ratio_35_37'].median()

# Frações isotópicas
f35 = ratio / (1 + ratio)
f37 = 1 / (1 + ratio)

print("\n=== Isotopic Abundance ===")

print(f"Area ratio H35/H37: {ratio:.4f}")
print(f"Cl35 abundance: {f35*100:.2f}%")
print(f"Cl37 abundance: {f37*100:.2f}%")

# Comparação com valores naturais
natural35 = 0.758
natural37 = 0.242

print("\n=== Difference from Natural Abundance ===")
print(f"Cl35: {(f35-natural35)*100:+.2f} p.p.")
print(f"Cl37: {(f37-natural37)*100:+.2f} p.p.")

# Conferência alternativa: razão das áreas totais
areas = results_df.groupby('Isotope')['Area_cm-1'].sum()

ratio_total = areas['H35Cl'] / areas['H37Cl']

print(f"\nRatio from summed areas: {ratio_total:.4f}")



# ==========================================
# 16. 解析⑦ - Propriedades rotacionais
# ==========================================

h = 6.62607015e-34       # J s
c = 2.99792458e10        # cm/s

# Obter os centros ajustados de H35Cl
def get_center(branch, J):
    row = results_df[
        (results_df['Branch'] == branch) &
        (results_df['J'] == J) &
        (results_df['Isotope'] == 'H35Cl')
    ]
    return row['Center_cm-1'].iloc[0]

R0 = get_center('R', 0)
P1 = get_center('P', 1)

# Constante rotacional aproximada (cm^-1)
B = (R0 - P1) / 4

# Momento de inércia (kg m^2)
I = h / (8 * np.pi**2 * c * B)

# Distância internuclear (m)
r = np.sqrt(I / mu35)

print("\n=== Rotational Analysis ===")
print(f"R(0): {R0:.5f} cm^-1")
print(f"P(1): {P1:.5f} cm^-1")
print(f"B: {B:.5f} cm^-1")
print(f"I: {I:.6e} kg m^2")
print(f"r: {r:.5e} m")
print(f"r: {r*1e10:.4f} Angstrom")



# ==========================================
# 17. 解析⑧ - Vibrational Analysis
# ==========================================

# Número de onda vibracional (cm^-1)
nu0 = (R0 + P1) / 2

# Frequência vibracional (Hz)
# c foi definido anteriormente em cm/s
f = c * nu0

# Frequência angular (rad/s)
omega = 2 * np.pi * f

# Constante de força (N/m)
k = mu35 * omega**2

print("\n=== Vibrational Analysis ===")
print(f"Vibrational wavenumber: {nu0:.5f} cm^-1")
print(f"Vibrational frequency: {f:.6e} Hz")
print(f"Angular frequency: {omega:.6e} rad/s")
print(f"Force constant: {k:.4f} N/m")


# ==========================================
# 18. 解析⑨ - Rotational Constants B0, B1
# ==========================================

# Centros dos picos H35Cl
R0 = get_center('R', 0)
R1 = get_center('R', 1)

P1 = get_center('P', 1)
P2 = get_center('P', 2)

# Constantes rotacionais (cm^-1)
B0 = (R0 - P2) / 6
B1 = (R1 - P1) / 6

# Frequência central corrigida
nu0_R = R0 - 2*B1
nu0_P = P1 + 2*B0

nu0_corrected = (nu0_R + nu0_P) / 2

print("\n=== Rotational Constants ===")
print(f"B0 = {B0:.6f} cm^-1")
print(f"B1 = {B1:.6f} cm^-1")
print(f"B0 - B1 = {B0-B1:.6f} cm^-1")

print(f"Band origin = {nu0_corrected:.6f} cm^-1")


# ==========================================
# 19. 解析⑩ - Centrifugal Distortion
# ==========================================

# Selecionar apenas H35Cl
hcl35 = results_df[
    results_df['Isotope'] == 'H35Cl'
].copy()

# Construir a matriz dos coeficientes
X = []
y = []
labels = []

for _, row in hcl35.iterrows():

    branch = row['Branch']
    J = int(row['J'])
    nu_obs = row['Center_cm-1']

    # Estado rotacional inicial
    F0 = J * (J + 1)

    # Estado rotacional final
    if branch == 'R':
        F1 = (J + 1) * (J + 2)
    elif branch == 'P':
        F1 = J * (J - 1)
    else:
        continue

    # Coeficientes de:
    # nu0, B0, B1, D0, D1
    X.append([
        1,
        -F0,
        F1,
        F0**2,
        -F1**2
    ])

    y.append(nu_obs)
    labels.append(f'{branch}({J})')

X = np.array(X, dtype=float)
y = np.array(y, dtype=float)

# Normalização para estabilidade numérica
scale = np.linalg.norm(X, axis=0)
X_scaled = X / scale

# Ajuste por mínimos quadrados
params_scaled, _, rank, _ = np.linalg.lstsq(
    X_scaled, y, rcond=None
)

params = params_scaled / scale

nu0_fit, B0_fit, B1_fit, D0_fit, D1_fit = params

# Valores previstos pelo modelo
y_fit = X @ params

# Resíduos
residuals = y - y_fit
rmse = np.sqrt(np.mean(residuals**2))

# ==========================================
# Comparação com rotor rígido (D0 = D1 = 0)
# ==========================================

X_rigid = X[:, :3]

rigid_params = np.linalg.lstsq(
    X_rigid, y, rcond=None
)[0]

y_rigid = X_rigid @ rigid_params

rmse_rigid = np.sqrt(
    np.mean((y - y_rigid)**2)
)

# ==========================================
# Resultados
# ==========================================

print("\n=== Centrifugal Distortion Analysis ===")

print(f"Band origin = {nu0_fit:.6f} cm^-1")
print(f"B0 = {B0_fit:.6f} cm^-1")
print(f"B1 = {B1_fit:.6f} cm^-1")
print(f"D0 = {D0_fit:.8f} cm^-1")
print(f"D1 = {D1_fit:.8f} cm^-1")

print(f"\nRMSE (rigid rotor): {rmse_rigid:.6f}")
print(f"RMSE (with distortion): {rmse:.6f}")

# Tabela de comparação
comparison = pd.DataFrame({
    'Transition': labels,
    'Observed': y,
    'Calculated': y_fit,
    'Residual': residuals
})

print("\n=== Observed vs Calculated ===")
print(comparison.to_string(index=False))

comparison.to_csv(
    '/Users/icaroprobo/Desktop/HCl_centrifugal_fit.csv',
    index=False
)

# ==========================================
# Gráfico dos resíduos
# ==========================================

plt.figure(figsize=(11, 5))

plt.scatter(
    range(len(y)),
    y - y_rigid,
    label='Rigid rotor',
    marker='o'
)

plt.scatter(
    range(len(y)),
    residuals,
    label='With centrifugal distortion',
    marker='x'
)

plt.axhline(0, color='black', linestyle='--')

plt.xticks(
    range(len(labels)),
    labels,
    rotation=45
)

plt.xlabel('Transition')
plt.ylabel('Observed - Calculated (cm$^{-1}$)')
plt.title('HCl - Centrifugal Distortion Analysis')
plt.grid(True)
plt.legend()

plt.savefig(
    '/Users/icaroprobo/Desktop/HCl_centrifugal_distortion.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()


# ==========================================
# 解析⑪ - Comparação dos dois métodos
# ==========================================


# Constante de Boltzmann
kB = 1.380649e-23  # J/K

# Temperatura rotacional característica
theta_rot = h * c * B0_fit / kB

theta_rot = h * c * B0_fit / kB

for branch in ['P', 'R']:

    subset = results_df[
        (results_df['Isotope'] == 'H35Cl') &
        (results_df['Branch'] == branch)
    ].sort_values('J')

    J = subset['J'].to_numpy()
    S = subset['Area_cm-1'].to_numpy()
    X = J * (J + 1)

    factors = {
        'Professor': 2 * J + 1,
        'Hönl-London': J if branch == 'P' else J + 1
    }

    for method, factor in factors.items():

        Y = np.log(S / factor)

        slope, intercept = np.polyfit(X, Y, 1)
        T = -theta_rot / slope

        print(f"{branch}-branch | {method}")
        print(f"Temperature: {T:.2f} K")
        print(f"Celsius: {T-273.15:.2f} C\n")
