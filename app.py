from flask import Flask, render_template, request
import sqlite3
import plotly.graph_objects as go

app = Flask(__name__)

def get_results(sort_by, sort_order, source_district):
    conn = sqlite3.connect('sanfrancisco.db')
    cur = conn.cursor()
    
    if sort_by == 'Rating':
        sort_column = 'Rating'
    elif sort_by == 'Price':
        sort_column = 'Price'
    else:
        sort_column = 'ReviewCount'

    where_clause = ''
    if (source_district != 'All'):
        where_clause = f'WHERE district = "{source_district}"'

    q = f'''
        SELECT Name, {sort_column}
        FROM SF_Foods2
        {where_clause}
        ORDER BY {sort_column} {sort_order}
        LIMIT 20
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    sort_by = request.form['sort']
    sort_order = request.form['dir']
    source_district = request.form['district']
    results = get_results(sort_by, sort_order, source_district)

    plot_results = request.form.get('plot', False)
    if (plot_results):
        x_vals = [r[0] for r in results]
        y_vals = [r[1] for r in results]
        biz_data = go.Bar(
            x=x_vals,
            y=y_vals
        )
        fig = go.Figure(data=biz_data)
        div = fig.to_html(full_html=False)
        return render_template("plot.html", plot_div=div)
    else:
        return render_template('results.html', 
            sort=sort_by, results=results,
            district=source_district)



if __name__ == '__main__':
    app.run(debug=True)