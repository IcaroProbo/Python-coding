import pandas as pd #pandas is used to read tables
import matplotlib.pyplot as plt #matplotli.pyplot is used to plot graphics

#Reads the file
data = pd.read_excel(r"Physics experiments data-graph\エクセルデータ\物理学実験YBCOデータ.xlsx", header = 36) 

#This comand serves to see the table and shows us the first lines of the table
print(data.head()) 
print(data.columns)

x = data["Temperature (K)"] #Usually time but put any unit you want, equal as it is written in the excel file
y = data["DC Moment Fixed Ctr (emu)"] #IDEM

plt.scatter(x, y) #Point graphic

#Graph information
plt.xlabel("Temperature (K)")
plt.ylabel("Magnetic moment m (emu)")
plt.title("Temperature Dependence of Magnetic Moment in YBCO")
plt.grid(True)
plt.legend()

#Save the figure for report
plt.savefig("ybco_graph.png", dpi = 300, bbox_inches = "tight")

plt.show()