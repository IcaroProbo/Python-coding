import matplotlib.pyplot as plt 
import pandas as pd
from pathlib import Path

#Save the graphs in another folder
fig_path = Path(r"C:\Users\icaro\OneDrive\Desktop\北海道大学\LaTeX\3年\物理学実験I\Figures")
fig_path.mkdir(parents=True, exist_ok=True)


#File names
files = {"MT":r"Physics experiments data-graph\実験データ\MnF2_MT.dat",
         "MH_5K": r"Physics experiments data-graph\実験データ\MnF2_MH_5K.dat",
         "MH_100K": r"Physics experiments data-graph\実験データ\MnF2_MH_100K.dat"}

#Read data (.dat format)
df_MT = pd.read_csv(files["MT"], skiprows = 35)
df_5K = pd.read_csv(files["MH_5K"], skiprows = 35)
df_100K = pd.read_csv(files["MH_100K"], skiprows = 35)

#Graph 1: M-T Curve
x_MT = df_MT["Temperature (K)"]
y_MT = df_MT["DC Moment Fixed Ctr (emu)"]

plt.figure(figsize = (7, 5))
plt.plot(x_MT, y_MT,)

plt.title("Temperature Dependence of Magnetization of MnF2")
plt.xlabel("Temperature T (K)")
plt.ylabel("Magnetic Moment M (emu)")
plt.grid(True)

plt.savefig(fig_path / "MnF2_MT_curve.png")
plt.show()



#Graph 2: M-H Curve at 5K
x_MH_5K = df_5K["Magnetic Field (Oe)"] / 10000 #Oe to T
y_MH_5K = df_5K["DC Moment Fixed Ctr (emu)"]

plt.figure(figsize = (7, 5))
plt.plot(x_MH_5K, y_MH_5K,)

plt.title("Magnetic-Field Dependence of Magnetization of MnF2 at 5K")
plt.xlabel("Magnetic Field B (T)")
plt.ylabel("Magnetic Moment M (emu)")
plt.grid(True)

plt.savefig(fig_path / "MnF2_MH_5K_curve.png")
plt.show()



#Graph 3: M-H curve at 100K
x_MH_100K = df_100K["Magnetic Field (Oe)"] / 10000 #Oe to T
y_MH_100K = df_100K["DC Moment Fixed Ctr (emu)"]

plt.figure(figsize = (7, 5))
plt.plot(x_MH_100K, y_MH_100K,)

plt.title("Magnetic-Field Dependence of Magnetization of MnF2 at 100K")
plt.xlabel("Magnetic Field B (T)")
plt.ylabel("Magnetic Moment M (emu)")
plt.grid(True)

plt.savefig(fig_path / "MnF2_MH_100K_curve.png")
plt.show()
