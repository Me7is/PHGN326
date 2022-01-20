import numpy as np
import matplotlib

energy = []
bin = []

model = np.polyfit(bin,energy,1)
predict = np.polyid(model)
