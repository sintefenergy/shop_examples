import pandas as pd

def add_tunnel_gate(shop):
    tunnel2=shop.model.tunnel["Tunnel2"]
    tunnel2.gate_opening_curve.set(pd.Series([0,1],index=[0,1]))
    tunnel2.continuous_gate.set(1)