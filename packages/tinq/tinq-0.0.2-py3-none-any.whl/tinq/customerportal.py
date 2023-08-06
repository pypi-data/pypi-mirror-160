import datetime
import logging

from requests_html import HTML

from tinq import ClientExternal

logger = logging.getLogger(__name__)


class CustomerPortalClient(ClientExternal):

    def __init__(self, username: str, password: str):
        super().__init__(username, password)

    def asfd_query_all(
            self,
            start_dt:
            datetime.date,
            end_dt: datetime.date,
            iata_code: str
    ) -> str:
        # https://customerportal.livetv.net/sites/livetv/Pages/LiveQuery.aspx
        iata_codes = ('JB', 'UA')
        if iata_code not in iata_codes:
            raise Exception(f'iata_code must be one of: {iata_codes}')

        if iata_code == 'UA':
            iata_code = 'CO'

        self.login()

        end_dt += datetime.timedelta(days=1)  # querying 1st to 10th will provide 1st to 9th...
        r = self.session.get('https://customerportal.livetv.net/sites/livetv/_vti_bin/ReportServer'
                             '?https%3a%2f%2fcustomerportal.livetv.net%2fsites%2flivetv%2fReports%2fASFDQueryALL.rdl'
                             f'&StartDate={start_dt:%m}%2F{start_dt:%d}%2F{start_dt:%Y}%2000%3A00%3A00'
                             f'&EndDate={end_dt:%m}%2F{end_dt:%d}%2F{end_dt:%Y}%2000%3A00%3A00'
                             f'&AirLineCode={iata_code}'
                             '&rs%3ACommand=Render'
                             '&rs%3AFormat=CSV')
        assert r.status_code == 200, 'Error, not able to get the flight data'

        html = HTML(html=r.text)
        return html.html


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    load_dotenv()

    client = CustomerPortalClient(os.getenv('LIVETV_USERNAME'),  # make sure to set this env var first
                                  os.getenv('LIVETV_EXT_PASSWORD'),  # make sure to set this env var first
                                  )
    data0_ = client.asfd_query_all(datetime.date(2022, 5, 1), datetime.date(2022, 5, 31), "JB")
    with open('asdf_query_all_JB.csv', 'wt', newline='') as f:
        f.write(data0_)

    print('asdf')
