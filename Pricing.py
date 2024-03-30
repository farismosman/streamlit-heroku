import pandas as pd
import streamlit as st
import plotly.express as px


def optimize(pm, tns, cns, cr, cap, oc, baseline) -> float:
    tr = oc + (pm * oc)
    ctc = (oc - cr)/(1 + (tns - cns))
    ctc = ctc if ctc > 0 else 0
    return (1./3.) * (ctc + (tr/tns) + baseline + 0.2 * cap)


def simulate(pms, tns, cns, cr, cap, ocs, baseline):
  estimates = []

  for oc in ocs:
    for pm in pms:
      pm_ = pm * 0.01
    
      min_price = optimize(pm_, tns, cns, cr, cap, oc, baseline)

      estimates.append({
        'profit_margin': pm,
        'targeted_no_sales': tns,
        'operation_cost': oc,
        'current_no_sales': cns,
        'current_revenue': cr,
        'competitor_average_price': cap,
        'baseline': baseline,
        'price': min_price
      })

  return pd.DataFrame(
    [(e['price'], e['operation_cost'], e['profit_margin']) for e in estimates],
    columns=['Price', 'Operation Cost', 'Profit Margin']
    )


targeted_no_sales = st.sidebar.number_input(label='Targeted No Sales', min_value=1)
current_no_sales = st.sidebar.number_input(label='Current No Sales', min_value=0)
current_revenue = st.sidebar.number_input(label='Current Revenue', min_value=0, step=500)
competitor_average_price = st.sidebar.number_input(label='Competitor Average Price', min_value=0, step=50)
baseline = st.sidebar.number_input(label='Baseline', min_value=0, step=50)

operation_cost = st.sidebar.slider(
  label='Operation Cost',
  min_value=0,
  max_value=10000,
  value=(1000, 4000),
  step=500)

profit_margins = st.sidebar.slider(
   label='Profit Margin % of Ops Cost',
   min_value=0,
   max_value=100,
   value=(5, 15),
   step=1,
   help="Presented as a percentage of operation cost")

prices = simulate(
            pms=range(profit_margins[0], profit_margins[1]),
            tns=targeted_no_sales,
            cns=current_no_sales,
            cr=current_revenue,
            cap=competitor_average_price,
            ocs=range(operation_cost[0], operation_cost[1], 100),
            baseline=baseline
          )

fig = px.scatter(
    prices,
    x="Operation Cost",
    y="Price",
    color="Profit Margin",
  )

fig.update_traces(
   marker=dict(
       size=2,
      #  symbol="arrow",
    )
)

st.plotly_chart(fig, use_container_width=True)