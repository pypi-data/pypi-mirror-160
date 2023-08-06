import datetime
from typing import Optional, List, Union, Iterable

from tinq import ClientInternal

import logging

logger = logging.getLogger(__name__)


class KAPortalExtClient(ClientInternal):
    """  Reports extracted via this client access the ssrs report directly via ssrs reports.

    In the livetv reports, as they are all similar, you can determine the report url by clicking
    on the 'Export to Data Feed' button.  This will download a .atomsvc which will contain
    the required urls.  You need to make slight modification.

    """

    def __init__(self, username: str, password: str):
        super().__init__(username, password)

    @staticmethod
    def iter_airline(airlines: Iterable, airline: Optional[Union[List, str]] = None):
        if not airline:
            airlines_ = airlines
        elif isinstance(airline, str):
            if airline not in airlines:
                raise Exception(f'Cannot get data for {airline}\nhere are the airlines: {airlines}')
            airlines_ = [airline]
        else:  # airline is already a list
            airlines_ = airline

        for airline_ in airlines_:
            yield airline_

    def ka_purchase_v3(self, start_dt: datetime.date, end_dt: datetime.date,
                       airline: Optional[Union[List, str]] = None) -> str:

        data = []
        airlines = ['SPIRIT']  # todo need to get complete list of airlines
        for i, airline_ in enumerate(self.iter_airline(airlines=airlines, airline=airline)):
            url = ('https://kaportalext.livetv.net/sites/livetv/_vti_bin/ReportServer'
                   '?https%3a%2f%2fkaportalext.livetv.net%2fsites%2flivetv%2fReports%2fCRS%2fKaPurchaseV3.rdl'
                   f'&AirlineFullName={airline_}'
                   f'&StartDate={start_dt:%m}%2F{start_dt:%d}%2F{start_dt:%Y}%2000%3A00%3A00'
                   f'&EndDate={end_dt:%m}%2F{end_dt:%d}%2F{end_dt:%Y}%2000%3A00%3A00'
                   '&rs%3ACommand=Render'
                   '&rs%3AFormat=CSV'
                   '&rc%3AItemPath=table1')
            r = self.session.get(url)

            for j, _ in enumerate(r.text.split('\r\n')):
                if i > 0 and j == 0:  # only use the columns header once time (across multiple customers)
                    continue
                data.append(_)

        if not data:
            return ''
        data[0] = (data[0]
                   .replace('Textbox59', 'PIIShareOptOut')
                   .replace('Textbox37', 'Status')
                   .replace('\ufeff', ''))

        return '\r\n'.join(data)

    def sla_monthly_sa_report(self, start_dt: datetime.date, end_dt: datetime.date,
                              airline: Optional[Union[str, List]] = None) -> str:

        data = []
        airline_sk = {'SPIRIT': '14'}  # todo need to get complete list of airlines
        for i, airline_ in enumerate(self.iter_airline(airlines=airline_sk.keys(), airline=airline)):
            url = ('https://kaportalext.livetv.net/sites/livetv/_vti_bin/ReportServer'
                   '?https%3a%2f%2fkaportalext.livetv.net%2fsites%2flivetv%2fReports%2fSLAMonthlySA.rdl'
                   f"&AirlineSK={airline_sk[airline_]}"
                   f"&StartDate={start_dt:%m}%2F{start_dt:%d}%2F{start_dt:%Y}%2000%3A00%3A00"
                   f"&EndDate={end_dt:%m}%2F{end_dt:%d}%2F{end_dt:%Y}%2000%3A00%3A00"
                   '&ScoreTypes=SA%2CSAWAP'
                   '&rs%3ACommand=Render'
                   '&rs%3AFormat=CSV'
                   '&rc%3AItemPath=table2.ScoreName3')
            r = self.session.get(url)

            for j, _ in enumerate(r.text.split('\r\n')):
                if not _:  # this report has a secondary report after a line break we don't care about
                    break
                if i > 0 and j == 0:  # we don't want the column headers again
                    continue
                data.append(_)

        if not data:
            return ''
        data[0] = (data[0]
                   .replace('Textbox128', 'ScoreValue')
                   .replace('Textbox208', 'ScoreTarget')
                   .replace('Textbox210', 'ScoreStatus')
                   .replace('\ufeff', ''))

        return '\r\n'.join(data)


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    load_dotenv()

    client = KAPortalExtClient(os.getenv('LIVETV_USERNAME'),  # make sure to set this env var first
                               os.getenv('LIVETV_PASSWORD'),  # make sure to set this env var first
                               )
    data0_ = client.ka_purchase_v3(datetime.date(2021, 11, 1), datetime.date(2021, 11, 30))
    with open('purchase-report-nks.csv', 'wt', newline='') as f:
        f.write(data0_)
    # data_ = client.sla_monthly_sa_report(datetime.date(2022, 1, 14), datetime.date(2022, 1, 14))
    # with open('sla-monthly-sa-nks.csv', 'wt', newline='') as f:
    #     f.write(data_)
    print('asdf')
