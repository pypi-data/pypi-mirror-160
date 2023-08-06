import nss
import pandas as pd
from datetime import datetime as dt


start = dt.now()

inputs = {'DU': pd.Series([1, 21, 42, 63, 126, 252, 378, 504, 630, 756, 882, 1008]),
          'TAXAS': pd.Series([0.126500, 0.129061, 0.130560, 0.131756, 0.133850, 0.134292,
                             0.130359, 0.126828, 0.124085, 0.122952, 0.122667, 0.122455]),
          'PESOS': pd.Series([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])}
df = pd.DataFrame(inputs)

print('Calibragem dos parâmetros')
result = nss.min_sse(df.to_numpy())
params = result.x
print('Success: ' + str(result.success), params)

print('Calculo pelo modelo de Nelson Siegel Svensson')
taxa = nss.nss(params[0], params[1], params[2], params[3], params[4], params[5], 21)
print('Taxa calculada:', taxa)

print('Tempo total: {}'.format(dt.now() - start))
