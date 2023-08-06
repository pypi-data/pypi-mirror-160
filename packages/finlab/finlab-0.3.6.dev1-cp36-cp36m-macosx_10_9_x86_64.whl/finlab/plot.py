import pandas as pd
from finlab import data
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from finlab.utils import logger

"""
Candles
"""


def average(series, n):
    return series.rolling(n, min_periods=int(n / 2)).mean()


def create_bias_df(df, ma_value=20, bias_multiple=2):
    bias_df = pd.DataFrame()
    ma_col_name = f'ma{ma_value}'
    bias_df[ma_col_name] = average(df['close'], ma_value)
    std = df['close'].rolling(ma_value, min_periods=int(ma_value / 2)).std()
    bias_df['upper_band'] = bias_df[ma_col_name] + std * bias_multiple
    bias_df['lower_band'] = bias_df[ma_col_name] - std * bias_multiple
    return bias_df


def create_stoch_df(df, **kwargs):
    from talib import abstract
    kd = abstract.STOCH(df['high'], df['low'], df['close'], **kwargs)
    kd = pd.DataFrame({'k': kd[0], 'd': kd[1]}, index=df.index)
    return kd


def plot_candles(stock_id, close, open_, high, low, volume, recent_days=400, resample='D', overlay_func=None,
                 technical_func=None):
    volume = volume.iloc[-recent_days:]
    if stock_id not in volume.columns:
        print('stock_id is not existed')
        return None
    else:
        volume = volume[stock_id]

    if resample.upper() != 'D':
        close = close.resample(resample).last()
        open_ = open_.resample(resample).first()
        high = high.resample(resample).max()
        low = low.resample(resample).min()
        volume = volume.resample(resample).sum()
    index_value = close.index
    df = pd.DataFrame({'close': close.ffill(), 'open': open_.ffill(), 'high': high.ffill(), 'low': low.ffill(),
                       'volume': volume.ffill()}, index=index_value)

    if overlay_func is None:
        overlay_ind = create_bias_df(df)
    else:
        overlay_ind = pd.DataFrame(index=df.index)
        for overlay_name, overlay_lambda in overlay_func.items():
            overlay_ind[overlay_name] = overlay_lambda(df)

    if isinstance(technical_func, dict):
        technical_func = [technical_func]
    if technical_func is None:
        technical_func_num = 1
    else:
        technical_func_num = len(technical_func)

    # plot
    rows = 2 + technical_func_num
    tech_plot_spec = [[{}]] * technical_func_num
    specs = [[{"rowspan": 2, "secondary_y": True}],
             [None],
             ]
    specs.extend(tech_plot_spec)
    fig = make_subplots(
        rows=rows,
        specs=specs,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=[f'{stock_id} Candle Plot'])

    fig.add_trace(
        go.Bar(x=index_value, y=volume, marker_color='orange', opacity=0.4, name="volume"),
        row=1, col=1
    )

    fig.add_trace(go.Candlestick(x=close.index,
                                 open=open_,
                                 high=high,
                                 low=low,
                                 close=close,
                                 increasing_line_color='#ff5050',
                                 decreasing_line_color='#009900',
                                 name="candle",
                                 ), row=1, col=1, secondary_y=True)

    # overlay plot
    fig_overlay = px.line(overlay_ind)
    for o in fig_overlay.data:
        fig.add_trace(go.Scatter(x=o['x'], y=o['y'], name=o['name'], line=dict(color=o['line']['color'], width=1.5)),
                      row=1, col=1, secondary_y=True)

    if technical_func is None:
        tech_ind = create_stoch_df(df)
        # tech plot
        fig_tech = px.line(tech_ind)
        for t in fig_tech.data:
            fig.add_trace(
                go.Scatter(x=t['x'], y=t['y'], name=t['name'], line=dict(color=t['line']['color'], width=1.5)),
                row=3, col=1)
    else:
        for num, sub_technical_func in enumerate(technical_func):
            tech_ind = pd.DataFrame(index=df.index)
            for tech_name, tech_lambda in sub_technical_func.items():
                tech_ind[tech_name] = tech_lambda(df)
            # tech plot
            fig_tech = px.line(tech_ind)
            for t in fig_tech.data:
                fig.add_trace(
                    go.Scatter(x=t['x'], y=t['y'], name=t['name'], line=dict(color=t['line']['color'], width=1.5)),
                    row=3 + num, col=1)

    # hide holiday
    if resample.upper() == 'D':
        dt_all = pd.date_range(start=index_value[0], end=index_value[-1])
        # retrieve the dates that ARE in the original datset
        dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(index_value)]
        # define dates with missing values
        dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if d not in dt_obs]
        # hide dates with no values
        fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

    fig.update_layout(
        height=800,
        xaxis2=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=3,
                         label="3m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True,
                thickness=0.1,
                bgcolor='gainsboro'
            ),
            type="date",
        ),

        yaxis=dict(
            title="vol",
            titlefont=dict(
                color="#ff9000"
            ),
            tickfont=dict(
                color="#ff9000"
            )
        ),
        yaxis2=dict(
            title="price",
            titlefont=dict(
                color="#d62728"
            ),
            tickfont=dict(
                color="#d62728"
            ),
            showgrid=False
        ),
        hovermode='x unified',
    )

    fig.update_traces(xaxis='x2')
    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)
    return fig


def plot_tw_stock_candles(stock_id, recent_days=400, adjust_price=False, resample='D', overlay_func=None,
                          technical_func=None):
    """繪製台股技術線圖圖組
    Args:
        stock_id (str): 台股股號，ex:`'2330'`。
        recent_days (int):取近n個交易日資料。
        adjust_price (bool):是否使用還原股價計算。
        resample (str): 技術指標價格週期，ex: `D` 代表日線, `W` 代表週線, `M` 代表月線。
        overlay_func (dict):
            K線圖輔助線，預設使用布林通道。
             ```py
             {
              'ema_5':lambda df:abstract.EMA(df['close'],timeperiod=5),
              'ema_10':lambda df:abstract.EMA(df['close'],timeperiod=10),
              'ema_20':lambda df:abstract.EMA(df['close'],timeperiod=20),
              'ema_60':lambda df:abstract.EMA(df['close'],timeperiod=60),
                  }
             ```
        technical_func (dict or list):
            技術指標子圖，預設使用KD指標。自定義格式如下:
            ```py
            {
              'rsi_10':lambda df:abstract.RSI(df['close'],timeperiod=10),
              'rsi_20':lambda df:abstract.RSI(df['close'],timeperiod=20),
              }
            ```
            設定多組技術指標：
            ```py
            [{
              'rsi_10':lambda df:abstract.RSI(df['close'],timeperiod=10),
               'rsi_20':lambda df:abstract.RSI(df['close'],timeperiod=20),
               },
             {
              'rsi_30':lambda df:abstract.RSI(df['close'],timeperiod=30),
              'rsi_60':lambda df:abstract.RSI(df['close'],timeperiod=60),
               },
            ]
            ```

    Returns:
        (plotly.graph_objects.Figure): 技術線圖

    Examples:
        ```py
        from finlab.plot import plot_tw_stock_candles
        from talib import abstract

        overlay_func={
                      'ema_5':lambda df:abstract.EMA(df['close'],timeperiod=5),
                      'ema_10':lambda df:abstract.EMA(df['close'],timeperiod=10),
                      'ema_20':lambda df:abstract.EMA(df['close'],timeperiod=20),
                      'ema_60':lambda df:abstract.EMA(df['close'],timeperiod=60),
                     }

        technical_func = [{
                            'rsi_10':lambda df:abstract.RSI(df['close'],timeperiod=10),
                            'rsi_20':lambda df:abstract.RSI(df['close'],timeperiod=20),
                           },
                          {
                            'k':lambda df:abstract.STOCH(df['high'], df['low'], df['close'])[0],
                            'd':lambda df:abstract.STOCH(df['high'], df['low'], df['close'])[1],
                           },
                         ]

        plot_tw_stock_candles(stock_id='2330',recent_days=600,adjust_price=False,overlay_func=overlay_func,technical_func=technical_func)
        ```
    ![技術指標圖組](img/plot/candle.png)
    """
    if adjust_price:
        close = data.get('etl:adj_close').iloc[-recent_days:][stock_id]
        open_ = data.get('etl:adj_open').iloc[-recent_days:][stock_id]
        high = data.get('etl:adj_high').iloc[-recent_days:][stock_id]
        low = data.get('etl:adj_low').iloc[-recent_days:][stock_id]
    else:
        close = data.get('price:收盤價').iloc[-recent_days:][stock_id]
        open_ = data.get('price:開盤價').iloc[-recent_days:][stock_id]
        high = data.get('price:最高價').iloc[-recent_days:][stock_id]
        low = data.get('price:最低價').iloc[-recent_days:][stock_id]
    volume = data.get('price:成交股數').iloc[-recent_days:]

    return plot_candles(stock_id, close, open_, high, low, volume, recent_days=recent_days, resample=resample,
                        overlay_func=overlay_func, technical_func=technical_func)


"""
Treemap
"""


def df_date_filter(df, start=None, end=None):
    if start:
        df = df[df.index >= start]
    if end:
        df = df[df.index <= end]
    return df


def create_treemap_data(start, end, item='return_ratio', clip=None):
    """產生台股板塊圖資料

    產生繪製樹狀圖所用的資料，可再外加FinLab資料庫以外的指標製作客製化DataFrame，
    並傳入`plot_tw_stock_treemap(treemap_data=treemap_data)。`

    Args:
      start (str): 資料開始日，ex:`"2021-01-02"`。
      end (str):資料結束日，ex:`"2021-01-05"`。
      item (str): 決定板塊顏色深淺的指標。
                  除了可選擇依照 start 與 end 計算的`"return_ratio"`(報酬率)，
                  亦可選擇[FinLab資料庫](https://ai.finlab.tw/database)內的指標顯示近一期資料。
          example:

          * `'price_earning_ratio:本益比'` - 顯示近日產業的本益比高低。
          * `'monthly_revenue:去年同月增減(%)'` - 顯示近月的單月營收年增率。

      clip (tuple): 將item邊界外的值分配給邊界值，防止資料上限值過大或過小，造成顏色深淺變化不明顯。
                    ex:(0,100)，將數值低高界線，設為0~100，超過的數值。
        !!! note

            參考[pandas文件](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.clip.html)更了解`pd.clip`細節。

    Returns:
        (pd.DataFrame): 台股個股指標
    Examples:

        欲下載所有上市上櫃之價量歷史資料與產業分類，只需執行此函式:

        ``` py
        from finlab.plot import create_treemap_data
        create_treemap_data(start= '2021-07-01',end = '2021-07-02')
        ```

        | stock_id   |  close |turnover|category|market|market_value|return_ratio|country|
        |:-----------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
        | 1101       |   20 |  57.85 |  水泥工業 |  sii   |    111  |    0.1  |  TW-Stock|
        | 1102       |  20 |  58.1  |  水泥工業 |  sii    |    111  |    -0.1 |  TW-Stock|


    """
    close = data.get('price:收盤價')
    basic_info = data.get('company_basic_info')
    turnover = data.get('price:成交金額')
    close_data = df_date_filter(close, start, end)
    turnover_data = df_date_filter(turnover, start, end).iloc[1:].sum() / 100000000
    return_ratio = (close_data.loc[end] / close_data.loc[start]).dropna().replace(np.inf, 0)
    return_ratio = round((return_ratio - 1) * 100, 2)

    concat_list = [close_data.iloc[-1], turnover_data, return_ratio]
    col_names = ['stock_id', 'close', 'turnover', 'return_ratio']
    if item not in ["return_ratio", "turnover_ratio"]:
        try:
            custom_item = df_date_filter(data.get(item), start, end).iloc[-1].fillna(0)
        except Exception as e:
            logger.error('data error, check the data is existed between start and end.')
            logger.error(e)
            return None
        if clip:
            custom_item = custom_item.clip(*clip)
        concat_list.append(custom_item)
        col_names.append(item)

    df = pd.concat(concat_list, axis=1).dropna()
    df = df.reset_index()
    df.columns = col_names

    basic_info_df = basic_info.copy()
    basic_info_df['stock_id_name'] = basic_info_df['stock_id'] + basic_info_df['公司簡稱']

    df = df.merge(basic_info_df[['stock_id', 'stock_id_name', '產業類別', '市場別', '實收資本額(元)']], how='left',
                  on='stock_id')
    df = df.rename(columns={'產業類別': 'category', '市場別': 'market', '實收資本額(元)': 'base'})
    df = df.dropna(thresh=5)
    df['market_value'] = round(df['base'] / 10 * df['close'] / 100000000, 2)
    df['country'] = 'TW-Stock'
    return df


def plot_tw_stock_treemap(start=None, end=None, area_ind='market_value', item='return_ratio', clip=None,
                          color_continuous_scale='Temps', treemap_data=None):
    """繪製台股板塊圖資料

    巢狀樹狀圖可以顯示多維度資料，將依照產業分類的台股資料絢麗顯示。

    Args:
      start (str): 資料開始日，ex:`'2021-01-02'`。
      end (str): 資料結束日，ex:`'2021-01-05'`。
      area_ind (str): 決定板塊面積數值的指標。
                      可選擇`["market_value","turnover"]`，數值代表含義分別為市值、成交金額。
      item (str): 決定板塊顏色深淺的指標。
                  除了可選擇依照 start 與 end 計算的`"return_ratio"`(報酬率)，
                  亦可選擇[FinLab資料庫](https://ai.finlab.tw/database)內的指標顯示近一期資料。
          example:

          * `'price_earning_ratio:本益比'` - 顯示近日產業的本益比高低。
          * `'monthly_revenue:去年同月增減(%)'` - 顯示近月的單月營收年增率。

      clip (tuple): 將 item 邊界外的值分配給邊界值，防止資料上限值過大或過小，造成顏色深淺變化不明顯。
                    ex:(0,100)，將數值低高界線，設為 0~100，超過的數值。
        !!!note

            參考[pandas文件](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.clip.html)更了解`pd.clip`細節。
      color_continuous_scale (str):[顏色變化序列的樣式名稱](https://plotly.com/python/builtin-colorscales/)
      treemap_data (pd.DataFrame): 客製化資料，格式參照 `create_treemap_data()` 返回值。
    Returns:
        (plotly.graph_objects.Figure): 樹狀板塊圖
    Examples:
        ex1:
        板塊面積顯示成交金額，顏色顯示'2021-07-01'～'2021-07-02'的報酬率變化，可以觀察市場資金集中的產業與漲跌強弱。
        ```py
        from finlab.plot import plot_tw_stock_treemap
        plot_tw_stock_treemap(start= '2021-07-01',end = '2021-07-02',area_ind="turnover",item="return_ratio")
        ```
        ![成交佔比/報酬率板塊圖](img/plot/treemap_return.png)
        ex2:
        板塊面積顯示市值(股本*收盤價)，顏色顯示近期本益比，可以觀察全市場哪些是權值股？哪些產業本益比評價高？限制數值範圍在(0,50)，
        將過高本益比的數值壓在50，不讓顏色變化突兀，能分出高低階層即可。
        ```py
        from finlab.plot import plot_tw_stock_treemap
        plot_tw_stock_treemap(area_ind="market_value",item="price_earning_ratio:本益比",clip=(0,50), color_continuous_scale='RdBu_r')
        ```
        ![市值/本益比板塊圖](img/plot/treemap_pe.png)
    """
    if treemap_data is None:
        df = create_treemap_data(start, end, item, clip)
    else:
        df = treemap_data.copy()

    if df is None:
        return None
    df['custom_item_label'] = round(df[item], 2).astype(str)

    if area_ind not in df.columns:
        return None

    if item in ['return_ratio']:
        color_continuous_midpoint = 0
    else:
        color_continuous_midpoint = np.average(df[item], weights=df[area_ind])

    fig = px.treemap(df,
                     path=['country', 'market', 'category', 'stock_id_name'],
                     values=area_ind,
                     color=item,
                     color_continuous_scale=color_continuous_scale,
                     color_continuous_midpoint=color_continuous_midpoint,
                     custom_data=['custom_item_label', 'close', 'turnover'],
                     title=f'TW-Stock Market TreeMap({start}~{end})'
                           f'---area_ind:{area_ind}---item:{item}',
                     width=1600,
                     height=800)

    fig.update_traces(textposition='middle center',
                      textfont_size=24,
                      texttemplate="%{label}<br>(%{customdata[1]})<br>%{customdata[0]}",
                      )
    return fig


"""
Radar
"""


def plot_radar(df, mode='line_polar', line_polar_fill=None, title=None):
    args = dict(data_frame=df, r="value", theta="variable", color="stock_id", line_close=True,
                color_discrete_sequence=px.colors.sequential.Plasma_r,
                template="plotly_dark")
    if mode is not 'line_polar':
        args.pop('line_close')

    fig = getattr(px, mode)(**args)
    if title is None:
        title = 'Features Radar'
    fig.update_layout(
        title={
            'text': title,
            'x': 0.49,
            'y': 0.99,
            'xanchor': 'center',
            'yanchor': 'top'},
        paper_bgcolor='rgb(41, 30, 109)',
        width=1200,
        height=600)
    if mode is 'line_polar':
        # None,toself,tonext
        fig.update_traces(fill=line_polar_fill)
    return fig


def get_rank(item: str, iloc_num=-1, cut_bins=10):
    df = data.get(item)
    df_rank = df.iloc[iloc_num].dropna().rank(pct=True)
    df_rank = pd.cut(x=df_rank, bins=cut_bins, labels=[i for i in range(1, cut_bins + 1)])
    return df_rank


def get_rank_df(feats: list, iloc_num=-1, cut_bins=10):
    df = pd.concat([get_rank(f, iloc_num, cut_bins) for f in feats], axis=1)
    columns_name = [f[f.index(':') + 1:] for f in feats]
    df = df.fillna(1)
    df.columns = columns_name
    df.index.name = 'stock_id'
    return df


def plot_tw_stock_radar(df=None, feats=None, select_targets=None, mode='line_polar', line_polar_fill=None,
                        cut_bins=10, title=None):
    """繪製台股雷達圖

    比較持股組合的指標分級特性。

    Args:
      df (pd.DataFrame): 客製化指標分級，欄名為特徵
                    格式範例:

        | stock_id   |  營業毛利率 |營業利益率|稅後淨利率|
        |:-----------|-------:|-------:|-------:|
        | 1101       |   2    |    5   |      3|
        | 1102       |   1    |    8   |      4|

      feats (list): 選定FinLab資料庫內的指標組成資料集。預設為18項財務指標
                    ex:['fundamental_features:營業毛利率','fundamental_features:營業利益率'].
      select_targets (list):持股組合，ex:`['1101','1102']`。
      mode (str): 雷達圖模式 ，ex:`'line_polar','bar_polar','scatter_polar'`。
        !!!note

            參考[不同模式的差異](https://plotly.com/python-api-reference/generated/plotly.express.html)
      line_polar_fill (str):將區域設置為用純色填充 。ex:`None,'toself','tonext'`
                           `'toself'`將跡線的端點（或跡線的每一段，如果它有間隙）連接成一個封閉的形狀。
                           如果一條完全包圍另一條（例如連續的等高線），則`'tonext'`填充兩條跡線之間的空間，如果之前沒有跡線，
                           則其行為類似於`'toself'`。如果一條跡線不包含另一條跡線，則不應使用`'tonext'`。
        !!!note

            參考[plotly.graph_objects.Scatterpolar.fill](https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Scatterpolar.html)

      cut_bins (int):特徵分級級距。
      title (str):圖片標題名稱。
    Returns:
        (plotly.graph_objects.Figure): 雷達圖
    Examples:
        ex1:比較持股組合累計分數，看持股組合偏重哪像特徵。
        ```py
        from finlab.plot import plot_tw_stock_radar
        plot_tw_stock_radar(select_targets=["1101", "2330", "8942", "6263"],mode="bar_polar" ,line_polar_fill='None')
        ```
        ![持股組合雷達圖](img/plot/radar_many.png)
        ex2:看單一個股特徵分級落點。
        ```py
        from finlab.plot import plot_tw_stock_radar
        feats = ['fundamental_features:營業毛利率', 'fundamental_features:營業利益率', 'fundamental_features:稅後淨利率',
                 'fundamental_features:現金流量比率', 'fundamental_features:負債比率']
        plot_tw_stock_radar(select_targets=["9939"],feats=feats, mode="line_polar" ,line_polar_fill='toself', cut_bins=8)
        ```
        ![單檔標的子選指標雷達圖](img/plot/radar_single.png)
    """
    if df is None:
        if feats is None:
            feats = ['fundamental_features:營業毛利率', 'fundamental_features:營業利益率', 'fundamental_features:稅後淨利率',
                     'fundamental_features:ROA綜合損益', 'fundamental_features:ROE綜合損益', 'fundamental_features:業外收支營收率',
                     'fundamental_features:現金流量比率', 'fundamental_features:負債比率',
                     'fundamental_features:流動比率', 'fundamental_features:速動比率', 'fundamental_features:存貨週轉率',
                     'fundamental_features:營收成長率', 'fundamental_features:營業毛利成長率',
                     'fundamental_features:營業利益成長率', 'fundamental_features:稅前淨利成長率', 'fundamental_features:稅後淨利成長率',
                     'fundamental_features:資產總額成長率', 'fundamental_features:淨值成長率'
                     ]
        df = get_rank_df(feats, cut_bins=cut_bins)

    col_name = df.columns
    if select_targets is None:
        select_targets = df.index[:2]
    df = df.loc[select_targets]
    df = df.reset_index()
    df = pd.melt(df, id_vars=['stock_id'], value_vars=col_name)
    fig = plot_radar(df=df, mode=mode, line_polar_fill=line_polar_fill, title=title)
    return fig


"""
PE PB River
"""


def get_pe_river_data(start=None, end=None, stock_id='2330', mode='pe', split_range=6):
    if mode not in ['pe', 'pb']:
        logger.error('mode error')
        return None
    close = df_date_filter(data.get('price:收盤價'), start, end)
    pe = df_date_filter(data.get('price_earning_ratio:本益比'), start, end)
    pb = df_date_filter(data.get('price_earning_ratio:股價淨值比'), start, end)
    df = eval(mode)
    if stock_id not in df.columns:
        logger.error('stock_id input is not in data.')
        return None
    df = df[stock_id]
    max_value = df.max()
    min_value = df.min()
    quan_value = (max_value - min_value) / split_range
    river_borders = [round(min_value + quan_value * i, 2) for i in range(0, split_range + 1)]
    result = (close[stock_id] / df).dropna().to_frame()
    index_name = f'{mode}/close'
    result.columns = [index_name]
    result['close'] = close[stock_id]
    result['pe'] = pe[stock_id]
    result['pb'] = pb[stock_id]
    for r in river_borders:
        col_name = f"{r} {mode}"
        result[col_name] = result[index_name] * r
    result = round(result, 2)
    return result


def plot_tw_stock_river(stock_id='2330', start=None, end=None, mode='pe', split_range=8):
    """繪製台股河流圖

    使用 PE or PB 的最高與最低值繪製河流圖，判斷指標所處位階。

    Args:
      stock_id (str): 台股股號，ex:`'2330'`。
      start (str): 資料開始日，ex:`'2020-01-02'`。
      end (str): 資料結束日，ex:`'2022-01-05'`。
      mode (str): `'pe'` or `'pb'` (本益比或股價淨值比)。
      split_range (int): 河流階層數。
    Returns:
        (plotly.graph_objects.Figure): 河流圖
    Examples:
      ```py
      from finlab.plot import plot_tw_stock_river
      plot_tw_stock_river(stock_id='2330', start='2015-1-1', end='2022-7-1', mode='pe', split_range=10)
      ```
      ![單檔標的子選指標雷達圖](img/plot/pe_river.png)
    """
    df = get_pe_river_data(start, end, stock_id, mode, split_range)
    if df is None:
        logger.error('data error')
        return None
    col_name_set = [i for i in df.columns if any(map(str.isdigit, i))]

    fig = go.Figure()
    for n, c in enumerate(col_name_set):
        if n == 0:
            fill_mode = None
        else:
            fill_mode = 'tonexty'
        fig.add_trace(
            go.Scatter(x=df.index, y=df[c], fill=fill_mode, line=dict(width=0, color=px.colors.qualitative.Prism[n]),
                       name=c))
    customdata = [(c, p) for c, p in zip(df['close'], df[mode])]
    hovertemplate = "<br>date:%{x|%Y/%m/%d}<br>close:%{customdata[0]}" + f"<br>{mode}" + ":%{customdata[1]}"
    fig.add_trace(go.Scatter(x=df.index, y=df['close'], line=dict(width=2.5, color='#2e4391'), customdata=customdata,
                             hovertemplate=hovertemplate, name='close'))

    security_categories = data.get('security_categories').set_index(['stock_id'])
    stock_name = security_categories.loc[stock_id]['name']
    fig.update_layout(title=f"{stock_id} {stock_name} {mode.upper()} River Chart",
                      template="ggplot2",
                      yaxis=dict(
                          title='price',
                      ),
                      # hovermode='x unified',
                      )
    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)
    return fig


class StrategySunburst:
    def __init__(self):

        """繪製策略部位旭日圖

        監控多策略。
        """
        self.s_data = data.get_strategies()

    def process_position(self, s_name, s_weight=1):
        if s_name == '現金':
            result = pd.DataFrame({'return': 0, 'weight': 1, 'category': '現金', 'market': '現金'}, index=['現金'])
            result.index.name = 'stock_id'
        else:
            df = pd.DataFrame(self.s_data[s_name]['positions'])
            df = df.drop(columns=['last_updated', 'next_trading_date', 'trade_at', 'update_date'])
            df = df.T
            df = df[df['weight'] > 0]
            if len(df) == 0:
                df['weight'] = 0
            df.index.name = 'stock_id'
            old_security_categories = data.get('security_categories')
            security_categories = old_security_categories.copy()
            security_categories['category'] = security_categories['category'].fillna('other_securities')
            security_categories['stock_id'] = security_categories['stock_id'] + ' ' + security_categories['name']
            security_categories = security_categories.set_index(['stock_id'])
            result = df.join(security_categories)

            asset_type = self.s_data[s_name]['asset_type']
            if asset_type == '':
                asset_type = 'tw_stock'
            elif asset_type == 'crypto':
                category = 'crypto'
                result['category'] = category

            result['market'] = asset_type
            cash = pd.DataFrame({'return': 0, 'weight': 1 - (df['weight'].sum()), 'category': '現金', 'market': '現金'},
                                index=['現金'])
            cash.index.name = 'stock_id'
            result = pd.concat([result, cash])

        result['s_name'] = s_name
        result['s_weight'] = s_weight
        return result

    def get_strategy_df(self, select_strategy=None):
        """獲取策略部位與分配權重後計算的資料

        Args:
          select_strategy (dict): 選擇策略名稱並設定權重，預設是抓取權策略並平分資金比例到各策略。
                                 ex:`{'低波動本益成長比':0.5,'研發魔人':0.2, '現金':0.2}`
        Returns:
            (pd.DataFrame): strategies data
        """
        if select_strategy is None:
            s_name = self.s_data.keys()
            s_weight = [1 / len(s_name)] * len(s_name)
        else:
            s_name = select_strategy.keys()
            s_weight = select_strategy.values()

        all_position = pd.concat([self.process_position(name, weight) for name, weight in zip(s_name, s_weight)])
        all_position['weight'] *= all_position['s_weight']
        all_position['return'] = round(all_position['return'].astype(float), 2)
        all_position['color'] = round(
            all_position['return'].clip(all_position['return'].min() / 2, all_position['return'].max() / 2), 2)
        all_position = all_position[all_position['weight'] > 0]
        all_position = all_position.reset_index()
        return all_position

    def plot(self, select_strategy=None, path=None, color_continuous_scale='RdBu_r'):
        """繪圖

        Args:
          select_strategy (dict): 選擇策略名稱並設定權重，預設是抓取權策略並平分資金比例到各策略。
                                 ex:`{'低波動本益成長比':0.5,'研發魔人':0.2, '現金':0.2}`
          path (list): 旭日圖由裡到外的顯示路徑，預設為`['s_name', 'market', 'category', 'stock_id']`。
                       `['market', 'category','stock_id','s_name']`也是常用選項。
          color_continuous_scale (str):[顏色變化序列的樣式名稱](https://plotly.com/python/builtin-colorscales/)

        Returns:
            (plotly.graph_objects.Figure): 策略部位旭日圖
        Examples:
            ```py
            from finlab.plot import StrategySunburst

            # 實例化物件
            strategies = StrategySunburst()
            strategies.plot().show()
            strategies.plot(select_strategy={'高殖利率烏龜':0.4,'營收強勢動能瘋狗':0.25,'低波動本益成長比':0.2,'現金':0.15},path =  ['market', 'category','stock_id','s_name']).show()
            ```
        ex1:策略選到哪些標的?
        ![市值/本益比板塊圖](img/plot/sunburst1.png)

        ex2:部位被哪些策略選到，標的若被不同策略選到，可能有獨特之處喔！
        ![市值/本益比板塊圖](img/plot/sunburst2.png)
        """
        position = self.get_strategy_df(select_strategy)
        if path is None:
            path = ['s_name', 'market', 'category', 'stock_id']
        fig = px.sunburst(position, path=path, values='weight',
                          color='color', hover_data=['return'],
                          color_continuous_scale=color_continuous_scale,
                          color_continuous_midpoint=0,
                          width=1000, height=800)
        return fig
