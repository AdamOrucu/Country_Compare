from flask import Flask, render_template, request, redirect, url_for
import unicodedata
from scrape import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compare')
def compare():
    first_country = request.args.get('firstcountry')
    second_country = request.args.get('secondcountry')
    if(first_country == 'Select Country' or second_country == 'Select Country'):
        return redirect(url_for('index'))
    
    soup1 = get_html(first_country)
    soup2 = get_html(second_country)

    title_info = [first_country, second_country, get_flag(soup1), get_flag(soup2)]
    info1 = get_info_table(soup1)
    info2 = get_info_table(soup2)

    keywords_first = [first_country] + get_demonyms(soup1)
    keywords_second = [second_country] + get_demonyms(soup2)
    print(keywords_first)
    res1 = list(dict.fromkeys(check_word_in_soup(keywords_first, soup2)))
    res2 = list(dict.fromkeys(check_word_in_soup(keywords_second, soup1)))
    # print(check_word_in_soup(keywords_first, soup2))
    # print(res2)
    return render_template('compare.html', title_info=title_info, info=[info1, info2], res=[res1, res2])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run()