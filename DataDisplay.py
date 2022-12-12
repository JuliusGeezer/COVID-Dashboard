from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import row, column
from bokeh.models.widgets import Select
from bokeh.models import CustomJS, TabPanel, Tabs, Dropdown
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
import pandas as pd


def read_data(json_file):
    # read json file, returns dataframe
    return pd.read_json(json_file)


def data_from_dates(start_date, end_date, stat='TotalDeaths'):
    # get list of dates in Y-m-d format
    dates = pd.date_range(start=start_date, end=end_date).strftime('%Y-%m-%d').to_list()

    # initialize empty dictionary
    covid_data_dict = {}

    # get data for specific stat over the range of dates for all countries
    # reformat data so countries are under column Country, then the remaining
    # columns are the values for the specified stat for the corresponding date
    for date in dates:
        covid_data = read_data('COVID-Dashboard/worldometer-' + date + '.json').transpose()
        covid_data_dict['Country'] = covid_data.index
        covid_data_list = covid_data[stat].to_list()
        covid_data_dict[date] = covid_data_list

    # convert dictionary to dataframe
    covid_data_frame = pd.DataFrame.from_dict(covid_data_dict)

    return covid_data_frame


def get_index(covid_data, country):
    return covid_data.loc[covid_data['Country'] == country].index[0]


def get_stats(covid_data, countries, dates):
    stats = []
    for place in countries:
        index = get_index(covid_data, place)
        stats.append(covid_data.loc[index, dates].tolist())
    return stats


def world_line_plot(covid_data, dates):
    world_list = ['North America', 'Asia', 'Europe', 'South America', 'Oceania', 'Africa']#, 'World']
    world_stats = get_stats(covid_data, world_list, dates)
    print(world_stats)
    p = figure(width=600, height=500, title='Total Deaths Worldwide', x_range=dates,
               x_axis_label='Date',
               y_axis_label='Deaths')
    color_list = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange']
    for world_stat, name, color in zip(world_stats, world_list, color_list):
        p.line(dates, world_stat, legend_label=name, color=color)
    p.legend.location = 'top_left'
    p.legend.click_policy = 'hide'
    return p


def wc_bar_graph(covid_data, stat):
    """
    makes a bar graph comparing the covid statistics of different countries still in the world cup.
    :param covid_data: dataframe of a specific statistic with columns Country, stat on date1, stat on date2...
    :param stat: specific statistic to use for bar graph e.g Total Deaths
    :return: bar graph for specific stat
    """
    countries = ['Argentina', 'Croatia', 'France', 'Morocco']
    dates = '2022-12-02'
    countries_stats = get_stats(covid_data, countries, dates)

    output_file('index.html')
    p = figure(width=600, height=500, title=stat, y_range=countries,
              x_axis_label=stat,
              y_axis_label='Countries')
    p.hbar(right=countries_stats, y=countries, left=0, height=0.4)

    return p


def countries_line_plot(covid_data, dates):
    country_list = covid_data['Country'].to_list()
    country_stats = get_stats(covid_data, country_list, dates)
    p = figure(width=600, height=500, title='Total Deaths', x_range=dates,
               x_axis_label='Date',
               y_axis_label='Deaths')
    #color_list = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange']
    for country_stat, name in zip(country_stats, country_list):
        p.line(dates, country_stat, legend_label=name)
    p.legend.location = 'top_left'
    p.legend.click_policy = 'hide'
    return p


def create_data_tabs(stats):
    """
    creates a tab for each statistic in stats e.g tab for Total Deaths
    :param stats: list of statistics at interest
    :return: panel widget with tabs for each statistic
    """
    tab = []
    for stat in stats:
        covid_data = data_from_dates('2022-11-30', '2022-12-02', stat=stat)
        p = wc_bar_graph(covid_data, stat)
        tab.append(TabPanel(child=p, title=stat))
    tabs = Tabs(tabs=tab)
    return tabs

def make_plot(dates, country_list, country_index):
    p = figure(width=600, height=500, title='Total Deaths', x_range=dates,
               x_axis_label='Date',
               y_axis_label='Deaths')
    p.line(dates, country_list[country_index])
    return p

def selection_plot(covid_data, dates):

    #source = ColumnDataSource(covid_data)
    country_list = covid_data['Country'].to_list()
    covid_data = covid_data.transpose()
    covid_data.columns = country_list
    covid_data = covid_data.drop('Country')
    source = ColumnDataSource(covid_data)
    print(covid_data)
    country_select = Select(title='Select Country:', value=country_list[0], options=country_list)
    #country_select.on_change('value', update_plot)

    # # create figure
    #
    #
    # p = figure(x_range=dates, width=600, height=300)
    # country_list = covid_data['Country'].to_list()
    # counties_stats = get_stats(covid_data, country_list, dates)
    #
    # plot_list = []
    # plot_dict = {}
    # for country_stats, name in zip(counties_stats, country_list):
    #     plot_list.append(p.line(dates, country_stats))
    #     plot_dict[name] = plot_list[-1]
    #
    # for plot in plot_list[1:]:
    #     plot.visible = False
    #
    # print(plot_dict)
    # source = ColumnDataSource(data=plot_dict)
    # select = Select(title='Select Country:', value=country_list[0], options=country_list)
    # select.js_on_change("value", CustomJS(args=dict(plot_dict=plot_dict), code="""
    # India.visible = true
    # if (this.value === "North America") {
    #     India.visible = true
    # } else {
    #     North America.visible = false
    # }
    #
    # """))
    # layout = column(select, p)
    # show(layout)

data_stats = ['TotalDeaths', 'Deaths/1M pop']
p_tabs = create_data_tabs(data_stats)

covid_data = data_from_dates('2022-11-30', '2022-12-02')
dates = covid_data.columns[1:].tolist()
p_line = world_line_plot(covid_data, dates)
countries = covid_data.index
p_country_line = countries_line_plot(covid_data, dates)
show(row(p_line, p_country_line, p_tabs))

