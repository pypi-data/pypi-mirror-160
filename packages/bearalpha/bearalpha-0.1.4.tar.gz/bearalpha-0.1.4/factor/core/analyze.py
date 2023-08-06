import sys
import bearalpha as ba
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..tools import *


def single_factor_analysis(factor_data: 'pd.Series | pd.DataFrame', price: 'pd.Series | pd.DataFrame',
                           grouper: 'pd.Series | pd.DataFrame | dict' = None, benchmark: pd.Series = None,
                           periods: 'list | int' = [5, 10, 15], q: int = 5, commission: float = 0.001, 
                           commission_type: str = 'both', plot_period: 'int | str' = -1, 
                           data_path: str = None, image_path: str = None, show: bool = True):
    if isinstance(factor_data, pd.DataFrame) and factor_data.columns.size > 1:
        ba.CONSOLE.print('[yellow][!][/yellow] Factor data in wide form, transposing ... ')
        factor_data = factor_data.stack()
        factor_data.name = 'factor'
    elif isinstance(factor_data, pd.DataFrame) and factor_data.columns.size == 1:
        factor_data = factor_data.iloc[:, 0]

    if isinstance(price, pd.DataFrame) and price.columns.size > 1:
        ba.CONSOLE.print('[yellow][!][/yellow] price in wide form, transposing ... ')
        price = price.stack()
        price.name = 'price'
    elif isinstance(price, pd.DataFrame) and price.columns.size == 1:
        price = price.iloc[:, 0]

    if isinstance(grouper, pd.DataFrame) and grouper.columns.size > 1:
        ba.CONSOLE.print('[yellow][!][/yellow] Grouper in wide form, transposing ... ')
        grouper = grouper.stack()
        grouper.name = 'grouper'
    elif isinstance(grouper, pd.DataFrame) and grouper.columns.size == 1:
        grouper = grouper.iloc[:, 0]

    periods = ba.item2list(periods)
    data_writer = pd.ExcelWriter(data_path) if data_path is not None else None
    fig, axes = plt.subplots(7, len(periods), figsize=(12 * len(periods), 7 * 8))
    if sys.platform == 'linux':
        plt.rcParams['font.sans-serif'] = ['DejaVu Serif']
    elif sys.platform == 'darwin':
        plt.rcParams['font.sans-serif'] = ['STSong']
        plt.rcParams['axes.unicode_minus'] = False
    elif sys.platform == 'win32':
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

    factor_data.unstack().to_excel(data_writer, sheet_name=f'factor_data')
    
    for i, period in enumerate(periods):
        forward_return = price.converter.price2ret(period=(-period - 1) * ba.CBD)
        # slice the common part of data
        ba.CONSOLE.print(f'[green][PERIOD = {period}][/green] Filtering common part ... ')
        common_index = factor_data.index.intersection(forward_return.index)
        if grouper is not None:
            common_index = common_index.intersection(grouper.index)
        
        factor_data_period = factor_data.loc[common_index]
        forward_return_period = forward_return.loc[common_index]
        if grouper is not None:
            grouper_period = grouper.loc[common_index]
        else:
            grouper_period = None
        
        cross_section_test(factor_data_period, forward_return_period, grouper_period, 
            plot_period=plot_period, boxplot_ax=axes[0, i], 
            scatter_ax=axes[1, i], hist_ax=axes[2, i])
                            
        ba.CONSOLE.rule(f'[PERIOD = {period}] Barra Test')
        if grouper_period is not None:
            barra_test(factor_data_period, forward_return_period, grouper_period,
                data_writer=data_writer, barra_ax=axes[3, i], show=show)
        else:
            ba.CONSOLE.print('[yellow][!][/yellow] You didn\'t provide group information,'
                'so it is impossible to make barra test')
                    
        ba.CONSOLE.rule(f'[PERIOD = {period}] IC Test')
        factor_direction = ic_test(factor_data_period, forward_return_period, 
            grouper_period, data_writer=data_writer, ic_ax=axes[4, i], show=show)
                
        ba.CONSOLE.rule(f'[PERIOD = {period}] Layering Test')
        layering_test(factor_data_period, forward_return_period, factor_direction=factor_direction,
            q=q, commission=commission, commission_type=commission_type,
            benchmark=benchmark, data_writer=data_writer, 
            layering_ax=axes[5, i], turnover_ax=axes[6, i], show=show)

    if image_path is not None:
        plt.savefig(image_path, bbox_inches='tight', dpi=fig.dpi, pad_inches=0.0)
    if show:
        plt.show()
    if data_writer is not None:
        data_writer.close()

def cross_section_test(factor_data: pd.Series, forward_return: pd.Series,
                       grouper: pd.Series = None, plot_period: 'int | str' = -1,
                       scatter_ax: plt.Axes = None, boxplot_ax: plt.Axes = None, 
                       hist_ax: plt.Axes = None) -> None:
    """"""
    concated_data = pd.concat([factor_data, forward_return, grouper], axis=1, join='inner')
    datetime_index = concated_data.dropna().index.get_level_values(0).unique()
    if isinstance(plot_period, int):
        plot_period = datetime_index[plot_period]

    if boxplot_ax is not None and grouper is not None:
        concated_data.drawer.draw('box', datetime=plot_period, whis=(5, 95),
            by=grouper.name, ax=boxplot_ax, indicator=[factor_data.name, grouper.name])
    if scatter_ax is not None:
        concated_data.drawer.draw('scatter', datetime=plot_period,
            x=factor_data.name, y=forward_return.name, ax=scatter_ax, s=1)
    if hist_ax is not None:
        # if grouper is not None:
        #     for group in grouper.dropna().unique():
        #         group_cs = concated_data.loc[plot_period].loc[
        #             (concated_data[grouper.name] == group).loc[plot_period], factor_data.name]
        #         if group_cs.empty:
        #             continue
        #         group_cs.drawer.draw('hist', bins=100, ax=hist_ax, label=group, indicator=factor_data.name, alpha=0.7)
        # else:
        concated_data.loc[plot_period].drawer.draw('hist', ax=hist_ax, 
            indicator=factor_data.name, bins=100, alpha=0.7)
        # hist_ax.legend()

def barra_test(factor_data: pd.Series, forward_return: pd.Series,
               grouper: pd.Series, data_writer: pd.ExcelWriter = None,
               barra_ax: plt.Axes = None, show: bool = True) -> None:
    freq = forward_return.index.levels[0].freq.n - 1
    grouper_dummies = pd.get_dummies(grouper).iloc[:, 1:]
    barra_x = pd.concat([grouper_dummies, factor_data], axis=1)
    barra_y = forward_return
    mkt_value = market_value(barra_y.index.levels[0].min(), barra_y.index.levels[0].max(), freq=(freq + 1) * ba.CBD)
    weight = 1/np.sqrt(mkt_value)
    barra_result = barra_x.regressor.wls(barra_y, weight)
    barra_result = barra_result.groupby(level=0).apply(lambda x: 
        pd.DataFrame({"coef": x.iloc[0].params, "t": x.iloc[0].tvalues, "p": x.iloc[0].pvalues}))
    barra_sigtest = barra_result.loc[:, 'coef'].tester.sigtest().unstack()
    barra_sigtest['abs(t(coef)) > 2'] = barra_result.loc[:, 't'].groupby(level=1
        ).apply(lambda x: x[x.abs() >= 2].count() / x.count())

    if show:
        barra_result.round(4).printer.display(title='barra result', asset=factor_data.name)
        barra_sigtest.round(4).printer.display(title='barra sigtest')

    if data_writer is not None:
        barra_result.to_excel(data_writer, sheet_name=f'barra result {freq}D')
        barra_sigtest.to_excel(data_writer, sheet_name=f'barra sigtest {freq}D')

    if barra_ax is not None:
        barra_ax.set_title(f'barra test {freq}D')
        barra_result.drawer.draw('bar', ax=barra_ax, asset=factor_data.name, indicator='coef', width=5)
        barra_result.drawer.draw('line', color='#aa1111', 
            ax=barra_ax.twinx(), asset=factor_data.name, indicator='t')

def ic_test(factor_data: pd.Series, forward_return: pd.Series,
            grouper: pd.Series = None, data_writer: pd.ExcelWriter = None,
            ic_ax: plt.Axes = None, show: bool = True) -> None:
    freq = forward_return.index.levels[0].freq.n - 1

    if grouper is not None:
        ic = factor_data.describer.ic(forward=forward_return, grouper=grouper)
        ic = ic.loc[ic.index.get_level_values(1) != 'nan'].iloc[:, 0]
        ic = pd.concat([factor_data.describer.ic(forward_return), ic.unstack()], axis=1)
    else:
        ic = factor_data.describer.ic(forward_return)

    evaluation = ic.tester.sigtest(0)
    sigportion = ic[ic.abs() >= 0.03].count() / ic.count()
    if isinstance(evaluation, pd.Series):
        evaluation['abs(ic) > 0.03'] = sigportion.iloc[0]
    else:
        evaluation['abs(ic) > 0.03'] = sigportion
    
    if show:
        ic.round(4).printer.display(title=f'IC {freq}D')
        evaluation.round(4).printer.display(title=f'IC sigtest {freq}D')

    if data_writer is not None:
        ic.to_excel(data_writer, sheet_name=f'IC {freq}D')
        evaluation.to_excel(data_writer, sheet_name=f'IC sigtest {freq}D')
            
    if ic_ax is not None:
        ic.drawer.draw('bar', ax=ic_ax, width=3, indicator=factor_data.name)
        ic.rolling(12).mean().drawer.draw('line', ax=ic_ax, 
            title=f'IC test {freq}D', indicator=factor_data.name)
        ic_ax.hlines(y=0.03, xmin=ic_ax.get_xlim()[0], 
            xmax=ic_ax.get_xlim()[1], color='#aa3333', linestyle='--')
        ic_ax.hlines(y=-0.03, xmin=ic_ax.get_xlim()[0], 
            xmax=ic_ax.get_xlim()[1], color='#aa3333', linestyle='--')
    
    # Return the factor direction, for layering to construct long short portfolio
    return np.sign(ic.iloc[:, 0].mean())

def layering_test(factor_data: pd.Series, forward_return: pd.Series, q: int = 5, factor_direction: int = 1, 
                  commission_type: str = 'both', commission: float = 0.001,
                  benchmark: pd.Series = None, data_writer: pd.ExcelWriter = None,
                  layering_ax: plt.Axes = None, turnover_ax: plt.Axes = None, show: bool = True) -> None:
    freq = forward_return.index.levels[0].freq.n - 1
    # TODO: finish layering within group
    factor_data = factor_direction * factor_data
    quantiles = factor_data.groupby(level=0).apply(pd.qcut, q=q, labels=False) + 1
    weight = pd.Series(np.ones_like(quantiles), index=quantiles.index)
    profit = weight.groupby(quantiles).apply(
        lambda x: x.relocator.profit(forward_return)).swaplevel().sort_index()
    turnover = weight.groupby(quantiles).apply(
        lambda x: x.relocator.turnover(side=commission_type)).swaplevel().sort_index()
    profit = profit - turnover * commission
    profit = profit.groupby(level=1).shift(1).fillna(0).unstack()
    profit['long_short'] = profit.iloc[:,-1] - profit.iloc[:,0]
    netvaluecurve = (profit + 1).cumprod()
    
    if benchmark is not None:
        benchmark_netvalue = benchmark / benchmark.iloc[0]
    else:
        benchmark_netvalue = netvaluecurve.iloc[:,0].copy()
        benchmark_netvalue.name = 'benchmark'
        benchmark_netvalue[:] = 1
    netvaluecurve = pd.concat([netvaluecurve, benchmark_netvalue], axis=1).dropna()
    benchmark_profit = netvaluecurve.iloc[:,-1].pct_change().fillna(0)
    profit = pd.concat([profit, benchmark_profit], axis=1).dropna()

    # TODO: Find something to present the risk free rate, and apply it here
    rf = pd.Series([0.04] * netvaluecurve.shape[0], index=netvaluecurve.index) * freq / 252

    premium = profit.apply(lambda x: x - rf)
    sharpe = premium.mean() / premium.std()
    if benchmark is None:
        sharpe['benchmark'] = np.nan
    sharpe.name = 'sharpe'

    drawdown = netvaluecurve - netvaluecurve.cummax()
    maxdrawdown = drawdown.min().abs()
    maxdrawdown.name = 'maxdrawdown'

    var95 = profit.quantile(.05)
    var95.name = 'var95'

    win_rate = profit.apply(lambda x: x > benchmark_profit).sum() / len(profit)
    win_rate.name = 'win_rate'

    date_size = pd.date_range(start=profit.index[0], end=profit.index[-1], freq = ba.CBD).size
    annual_ret = (netvaluecurve.iloc[-1] / netvaluecurve.iloc[0] - 1) * 252 / date_size
    annual_ret.name = 'annual_ret'

    evaluation = pd.concat([sharpe, maxdrawdown, var95, win_rate, annual_ret], axis=1)
    
    if show:
        profit.round(4).printer.display(title=f'profit {freq}D')
        netvaluecurve.round(4).printer.display(title=f'cumulative profit {freq}D')
        evaluation.round(4).printer.display(title=f'evaluation {freq}D')
        turnover.round(2).printer.display(title=f'turnover {freq}D')

    if data_writer is not None:
        profit_data = pd.concat([profit.stack(), netvaluecurve.stack()], axis=1)
        profit_data.index.names = ['datetime', 'quantiles']
        profit_data.columns = ['profit', 'netvaluecurve']
        profit_data.unstack().to_excel(data_writer, sheet_name=f'layering {freq}D')

    if layering_ax is not None:
        layering_ax_twinx = layering_ax.twinx()
        profit.drawer.draw('bar', ax=layering_ax, width=2)
        netvaluecurve.drawer.draw('line', ax=layering_ax_twinx, title=f'layering test {freq}D')
        # layering_ax_twinx.hlines(y=1, xmin=layering_ax.get_xlim()[0], 
        #     xmax=layering_ax.get_xlim()[1], color='grey', linestyle='--')

    if turnover_ax is not None:
        turnover.unstack().drawer.draw('line', ax=turnover_ax, title=f'turnover {freq}D')

    if data_writer is not None:
        turnover.unstack().to_excel(data_writer, sheet_name=f'turnover {freq}D')

    
if __name__ == "__main__":
    pass
