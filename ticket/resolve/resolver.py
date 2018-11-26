# -*- coding: UTF-8 -*-

class Resolver(object):

    def left_ticket(self, results):
        for result in results:
            if self._has_ticket(result):
                return True
        return False

    def _has_ticket(self, item):
        return format(item['soft_bed']) or format(item['no_seat']) or format(item['hard_bed']) or format(
            item['hard_seat']) or format(item['crh_no_seat']) or format(item['second_seat']) or format(
            item['first_seat']) or format(item['business_seat']) or format(item['special_seat']) or format(
            item['crh_bed'])

    def format(self, value):
        if "有" in value:
            return True
        try:
            v = int(value)
            return v > 0
        except:
            return False
        return False
