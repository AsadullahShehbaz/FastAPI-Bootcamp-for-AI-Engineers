from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import base64
import plotly.express as px
from plotly.io import to_html
from io import BytesIO

app=FastAPI()

df = sns.load_dataset('titanic')
survival_rate = df.groupby('class')['survived'].mean().reset_index()
@app.get('/')
async def root():
    return survival_rate.to_dict(orient='records')

@app.get('/plot',response_class=HTMLResponse)
async def plot():
    fig, ax = plt.subplots()
    sns.barplot(x='class', y='survived', data=df)
    plt.title('Survival Rate by Class')
    plt.xlabel('Class')
    plt.ylabel('Survival Rate')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f'<img src="data:image/png;base64,{image}">'

@app.get('/plotly',response_class=HTMLResponse)
async def plotly():
    fig = px.bar(survival_rate, x='class', y='survived', title='Survival Rate by Class')
    plot_div = to_html(fig)

    html_content= f"""
    <html> 
    <body>
    <h1>Survival Rate by Class</h1>
    <br>
    <p>This plot is created using Plotly in the Day 174 (10 August 2025).</p>
    {plot_div}
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# This feature will work when you run on this command "python main.py"
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=5000) 