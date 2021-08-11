from matplotlib import pyplot as plt
import base64
from io import BytesIO



def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x_range, y_range, currency_code):
    plt.switch_backend('AGG')
    plt.title(f'{currency_code} course')
    plt.ylabel('Value')

    plt.plot(x_range, y_range)
    plt.xticks(rotation=90)
    plt.xlabel('Date')
    plt.tight_layout()
    graph = get_graph()
    return graph