# -*- coding: utf-8 -*-
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class Malc0deIPBlacklistParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.splitlines():

            row = row.strip()
            if row == "" or row[:2] == "//":
                continue

            event = self.new_event(report)

            event.add('classification.type', 'malware')
            event.add('source.ip', row)
            event.add('raw', row)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = Malc0deIPBlacklistParserBot(sys.argv[1])
    bot.start()
