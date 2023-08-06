import six
from datetime import date
from dateutil.relativedelta import relativedelta
from rqalpha.data.base_data_source import BaseDataSource, data_source
from rqalpha.const import *
import pymongo
import pytz
import pandas as pd


class TushareKDataSource(BaseDataSource):
    def __init__(self, path, custom_future_info):
        super(TushareKDataSource, self).__init__(path, custom_future_info)

    @staticmethod
    def get_tushare_k_data(instrument, start_dt, end_dt):
        order_book_id = instrument.order_book_id
        code = order_book_id.split(".")[0]
        mkt = order_book_id.split(".")[1]
        mkt = '.SH' if mkt == 'XSHG' else '.SZ'
        ts_code = code+mkt

        if instrument.type == 'CS':  # stock
            record_list = TushareKDataSource.db_get_dict_from_mongodb(
                mongo_db_name='db_tushare',
                col_name='stock_daily',
                query_dict={
                    'ts_code': ts_code,
                    'trade_date': {
                        '$gte': start_dt.strftime('%Y%m%d'),
                        '$lte': end_dt.strftime('%Y%m%d')
                    }
                }
            )
            result = pd.DataFrame(record_list)
        elif instrument.type == 'INDX':  # index
            record_list = TushareKDataSource.db_get_dict_from_mongodb(
                mongo_db_name='db_tushare',
                col_name='index_daily',
                query_dict={
                    'ts_code': ts_code,
                    'trade_date': {
                        '$gte': start_dt.strftime('%Y%m%d'),
                        '$lte': end_dt.strftime('%Y%m%d')
                    }
                }
            )
            result = pd.DataFrame(record_list)
            if result.empty:  # 非const中的指数，例如债券指数，从akshare中获取
                code = order_book_id.split(".")[0]
                mkt = order_book_id.split(".")[1]
                mkt = 'sh' if mkt == 'XSHG' else 'sz'
                ak_code = mkt+code
                index_record = TushareKDataSource.db_get_dict_from_mongodb(
                    mongo_db_name='db_akshare',
                    col_name='aks_index',
                    query_dict={
                        'code': ak_code,
                    }
                )
                hist_df = pd.DataFrame(index_record[0]['index'])
                hist_df['date'] = pd.to_datetime(
                    hist_df['date'], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y%m%d'))  # 将XXXX-XX-XX日期转换成，XXXXXXXX格式
                result = hist_df
                result = result.loc[result['date']
                                    <= end_dt.strftime('%Y%m%d'), ]
                result = result.loc[result['date']
                                    >= start_dt.strftime('%Y%m%d'), ]
                if not result.empty:
                    result.rename(columns={
                        'date': 'trade_date',
                        'volume': 'vol'
                    }, inplace=True)
        elif instrument.type == 'ETF':  # fund
            record_list = TushareKDataSource.db_get_dict_from_mongodb(
                mongo_db_name='db_tushare',
                col_name='fund_daily',
                query_dict={
                    'ts_code': ts_code,
                    'trade_date': {
                        '$gte': start_dt.strftime('%Y%m%d'),
                        '$lte': end_dt.strftime('%Y%m%d')
                    }
                }
            )
            result = pd.DataFrame(record_list)
        elif instrument.type == 'LOF':  # fund
            record_list = TushareKDataSource.db_get_dict_from_mongodb(
                mongo_db_name='db_tushare',
                col_name='fund_daily',
                query_dict={
                    'ts_code': ts_code,
                    'trade_date': {
                        '$gte': start_dt.strftime('%Y%m%d'),
                        '$lte': end_dt.strftime('%Y%m%d')
                    }
                }
            )
            result = pd.DataFrame(record_list)
        else:
            return

        if not result.empty:
            result.rename(columns={
                'trade_date': 'datetime',
                'vol': 'volume'
            }, inplace=True)

        return result

    def get_bar(self, instrument, dt, frequency):
        if frequency != '1d':
            return super(TushareKDataSource, self).get_bar(instrument, dt, frequency)

        bar_data = self.get_tushare_k_data(instrument, dt, dt)

        if bar_data is None or bar_data.empty:
            return super(TushareKDataSource, self).get_bar(instrument, dt, frequency)
        else:
            return bar_data.iloc[0].to_dict()

    def history_bars(self, instrument, bar_count, frequency, fields, dt, skip_suspended=True, include_now=False, adjust_type='pre', adjust_orig=None):
        if frequency != '1d' or not skip_suspended:
            return super(TushareKDataSource, self).history_bars(instrument, bar_count, frequency, fields, dt, skip_suspended)

        start_dt_loc = self.get_trading_calendars()[TRADING_CALENDAR_TYPE.EXCHANGE].get_loc(
            dt.replace(hour=0, minute=0, second=0, microsecond=0)) - bar_count + 1
        start_dt = self.get_trading_calendars(
        )[TRADING_CALENDAR_TYPE.EXCHANGE][start_dt_loc]

        bar_data = self.get_tushare_k_data(instrument, start_dt, dt)

        if bar_data is None or bar_data.empty:
            return super(TushareKDataSource, self).get_bar(instrument, dt, frequency)
        else:
            if isinstance(fields, six.string_types):
                fields = [fields]
            fields = [field for field in fields if field in bar_data.columns]

            # return bar_data[fields].values
            return bar_data[fields]

    def available_data_range(self, frequency):
        return date(2005, 1, 1), date.today() - relativedelta(days=1)

    @staticmethod
    def db_get_dict_from_mongodb(mongo_db_name: str, col_name: str,
                                 query_dict: dict = {}, field_dict: dict = {}, inc_id: bool = False):
        '''

        :param mongo_db_name:
        :param col_name:
        :param query_dict:
        :param field_dict: {'column1':1, 'column2':1}
        :return:
        '''
        c = pymongo.MongoClient(
            host="mongodb://layewang:toorroot!@mongo:27017/",
            tz_aware=True,
            tzinfo=pytz.timezone('Asia/Shanghai')
        )
        db = c[mongo_db_name]
        db_col = db[col_name]
        if not inc_id:
            field_dict['_id'] = 0
        result_dict_list = [x for x in db_col.find(query_dict, field_dict)]
        return result_dict_list
