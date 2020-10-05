#! python3

# CREATE HTML REPORT

import get_data
import analysis
import pickle


def create_html_file():
    with open('report_statistics.pickle', 'rb') as f:
        w_stats = pickle.load(f)

    html_string = f'''
    <html>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
            <style>
                body{{ 
                    margin:80 100; 
                    background:white;
                    font-family: "Courier New", Courier, monospace;
                    font-weight: bold;
                    font-size: 25px;
                }}
            </style>
        </head>
        <body>
            <br>
            <p style="font-size: 30px">WEIGHT REPORT</p>

            <!-- *** Section 1 *** --->
            <p>Subject: Matteo De Stefano<br>
            Date: {w_stats['date']}</p>

            <!-- *** Sparkline *** --->
            <p>
            <img src="file:///C:/Users/deste/Desktop/Varie/python/progetti/weight update/charts/sparkline.png" 
                width="85%"><br>
            Current weight: {w_stats['last_weight']}
            <br></p>

            <!-- *** Chart 30 days *** --->
            <p style="font-size: 27px"><br>Last 30 days:<br>
            <img src="file:///C:/Users/deste/Desktop/Varie/python/progetti/weight update/charts/chart_30days.png" 
                width="85%">
            <br></p>
            <p>Median weight: {round(w_stats['median'], 1)}<br>
            Max weight: &nbsp;&nbsp;&nbsp;{w_stats['max']}<br>
            Min weight: &nbsp;&nbsp;&nbsp;{w_stats['min']}<br><br></p>

            <!-- *** Chart weekdays *** --->
            <p style="font-size: 27px">Distance from the mean - 90 days:<br>
            <img src="file:///C:/Users/deste/Desktop/Varie/python/progetti/weight update/charts/chart_weekdays.png" 
                width="85%">
            </p>
        </body>
    </html>'''

    with open('weight_report.html','w') as f:
        f.write(html_string)
        f.close()


def main():
    # Load Data
    get_data.main()
    print('Data updated.')

    # Create charts and statistics
    analysis.main()
    print('Analysis completed.')

    # Create report in html
    create_html_file()


if __name__ == '__main__':
    main()