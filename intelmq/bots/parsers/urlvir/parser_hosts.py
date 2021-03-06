# -*- coding: utf-8 -*-
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import IPAddress


class URLVirHostsParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.splitlines():

            row = row.strip()
            if row == "" or row.startswith("#"):
                continue

            event = self.new_event(report)

            if IPAddress.is_valid(row):
                event.add('source.ip', row)
            else:
                event.add('source.fqdn', row)

            event.add('classification.type', 'malware')
            event.add('raw', row)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = URLVirHostsParserBot(sys.argv[1])
    bot.start()
