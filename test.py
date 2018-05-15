from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import websocket
from websocket import create_connection

ws = create_connection("ws://localhost:5000")

ts = TimeSeries(key='NSBVLTCPXHA7R2I5',output_format='pandas')
data, meta_data = ts.get_intraday('GOOGL',interval='1min', outputsize='full')

sub_data = data[['5. volume', '4. close']]
sub_data = sub_data.rename(index=str, columns={"5. volume": "volume", "4. close": "price"})

for index, row in sub_data.iterrows():
	index = index.replace('-','.').replace(' ','D') + ('.00000000')
	msg = ';'.join([index,'`GOOGL',str(row['price']),str(row['volume']),'0'])
	msg = ".u.upd[" + msg + "];"
	ws.send(msg)
