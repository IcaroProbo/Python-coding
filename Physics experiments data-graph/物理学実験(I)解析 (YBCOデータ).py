import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

data_dir = BASE_DIR / "実験データ"
output_dir = BASE_DIR / "生成されたグラフ"
output_dir.mkdir(parents=True, exist_ok=True)

ybco_excel = data_dir / "物理学実験YBCOデータ.xlsx"
cooling_csv = data_dir / "YBCO_RT_cooling.csv"
heating_csv = data_dir / "YBCO_RT_heating.csv"

# ============================================================
# 1. YBCO magnetic susceptibility graph
# ============================================================

# Read MPMS data
data = pd.read_excel(ybco_excel, header=36)

print("YBCO MPMS data:")
print(data.head())
print(data.columns)

# Sample information
sample_mass_g = 0.0081          # 8.1 mg = 0.0081 g
molar_mass_ybco = 666.2         # g/mol
n_mol = sample_mass_g / molar_mass_ybco

# Magnetic field
H_oe = 1000                     # approximately 1000 Oe

# Data columns
temperature = data["Temperature (K)"]
magnetic_moment = data["DC Moment Fixed Ctr (emu)"]

# Convert magnetic moment to molar magnetic susceptibility
chi_mol = magnetic_moment / (H_oe * n_mol)

# Plot
plt.figure(figsize=(8, 5.5))
plt.scatter(
    temperature,
    chi_mol,
    s=25,
    label=r"$\chi_{\mathrm{mol}}$"
)

plt.xlabel("Temperature $T$ (K)", fontsize=12)
plt.ylabel(r"Molar magnetic susceptibility $\chi_{\mathrm{mol}}$ (emu/mol)", fontsize=12)
plt.title("Temperature Dependence of Molar Magnetic Susceptibility in YBCO", fontsize=13)
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(output_dir / "ybco_susceptibility_vs_temperature.png", dpi=300, bbox_inches="tight")
plt.show()


# ============================================================
# 2. YBCO resistance-temperature graph
#    Cooling and heating curves in the same graph
# ============================================================

# Read resistance data
df_cooling = pd.read_csv(
    cooling_csv,
    skiprows=1,
    header=None,
    names=["Temperature_K", "Resistance_ohm"]
)

df_heating = pd.read_csv(
    heating_csv,
    skiprows=1,
    header=None,
    names=["Temperature_K", "Resistance_ohm"]
)

print("Cooling data:")
print(df_cooling.head())

print("Heating data:")
print(df_heating.head())

# Sort by temperature
df_cooling = df_cooling.sort_values("Temperature_K")
df_heating = df_heating.sort_values("Temperature_K")

# Plot full R-T graph
plt.figure(figsize=(8, 5.5))

plt.scatter(
    df_cooling["Temperature_K"],
    df_cooling["Resistance_ohm"],
    s=20,
    label="Cooling"
)

plt.scatter(
    df_heating["Temperature_K"],
    df_heating["Resistance_ohm"],
    s=20,
    label="Heating"
)

plt.xlabel("Temperature $T$ (K)", fontsize=12)
plt.ylabel(r"Electrical resistance $R$ ($\Omega$)", fontsize=12)
plt.title("Temperature Dependence of Electrical Resistance in YBCO", fontsize=13)
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(output_dir / "ybco_resistance_vs_temperature.png", dpi=300, bbox_inches="tight")
plt.show()


# ============================================================
# 3. Zoom near superconducting transition
# ============================================================

plt.figure(figsize=(8, 5.5))

plt.scatter(
    df_cooling["Temperature_K"],
    df_cooling["Resistance_ohm"],
    s=25,
    label="Cooling"
)

plt.scatter(
    df_heating["Temperature_K"],
    df_heating["Resistance_ohm"],
    s=25,
    label="Heating"
)

plt.xlabel("Temperature $T$ (K)", fontsize=12)
plt.ylabel(r"Electrical resistance $R$ ($\Omega$)", fontsize=12)
plt.title("Superconducting Transition Region in YBCO", fontsize=13)

plt.xlim(85, 100)

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(output_dir / "ybco_resistance_transition_zoom.png", dpi=300, bbox_inches="tight")
plt.show()