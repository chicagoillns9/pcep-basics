import sys
import platform
import numpy as np
import matplotlib.pyplot as plt

print("✅ Environment OK")
print("Python:", sys.version.split()[0])
print("Platform:", platform.platform())

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)
plt.plot(x, y)
plt.title("Environment Ready - Test Plot")
plt.show()
