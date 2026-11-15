import argparse
import pandas as pd

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--forecast',required=True); p.add_argument('--routes',required=True)
    p.add_argument('--route',required=True); p.add_argument('--date',required=True); p.add_argument('--price',type=float,required=True)
    a=p.parse_args(); f=pd.read_csv(a.forecast); r=pd.read_csv(a.routes)
    row=f[(f.route==a.route)&(f.date.astype(str).str[:10]==a.date)].iloc[0]
    info=r[r.route==a.route].iloc[0]; b=float(info.price_sensitivity); p0=float(info.base_price); seats=int(row.seats)
    for q in [f"0.{i}" for i in range(1,10)]:
        wanted=max(0,float(row[f"{q}_base_demand"])-b*(a.price-p0)); sold=min(seats,wanted)
        print(q, 'спрос=',round(wanted,1),'продажи=',round(sold,1))
if __name__=='__main__': main()
