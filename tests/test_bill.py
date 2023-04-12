import datetime
import os

import pytest

from power_bill_extractor.bill import PowerBill

samples_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../samples"))


class TestPowerBill:
    sample01 = os.path.join(samples_dir, "sample01.pdf")
    sample02 = os.path.join(samples_dir, "sample02.pdf")
    sample03 = os.path.join(samples_dir, "sample03.pdf")
    sample04 = os.path.join(samples_dir, "sample04.pdf")

    bill1 = PowerBill(sample01)
    bill2 = PowerBill(sample02)
    bill3 = PowerBill(sample03)
    bill4 = PowerBill(sample04)

    @pytest.mark.skip(
        reason="Will have to write out the lists that the boxes should return."
    )
    def test_boxes(self):
        ...

    def test_start_date(self):
        assert self.bill1.start_date == datetime.date(2021, 1, 27)
        assert self.bill2.start_date == datetime.date(2021, 7, 27)
        assert self.bill3.start_date == datetime.date(2022, 1, 26)
        assert self.bill4.start_date == datetime.date(2022, 7, 27)

    def test_end_date(self):
        assert self.bill1.end_date == datetime.date(2021, 2, 25)
        assert self.bill2.end_date == datetime.date(2021, 8, 27)
        assert self.bill3.end_date == datetime.date(2022, 2, 25)
        assert self.bill4.end_date == datetime.date(2022, 8, 26)

    def test_service_length(self):
        assert self.bill1.service_length == 29
        assert self.bill2.service_length == 31
        assert self.bill3.service_length == 30
        assert self.bill4.service_length == 30

    def test_bill_amount(self):
        assert self.bill1.bill_amount == 148.57
        assert self.bill2.bill_amount == 162.58
        assert self.bill3.bill_amount == 164.28
        assert self.bill4.bill_amount == 183.66

    def test_current_meter_reading(self):
        assert self.bill1.current_meter_reading == 10188
        assert self.bill2.current_meter_reading == 18599
        assert self.bill3.current_meter_reading == 25549
        assert self.bill4.current_meter_reading == 33617

    def test_previous_meter_reading(self):
        assert self.bill1.previous_meter_reading == 9220
        assert self.bill2.previous_meter_reading == 16938
        assert self.bill3.previous_meter_reading == 24563
        assert self.bill4.previous_meter_reading == 32223

    def test_kwh_used(self):
        assert self.bill1.kwh_used == 968
        assert self.bill2.kwh_used == 1661
        assert self.bill3.kwh_used == 986
        assert self.bill4.kwh_used == 1394

    def test_nonfuel_first_1000(self):
        assert self.bill1.nonfuel_first_1000 == 0.067
        assert self.bill2.nonfuel_first_1000 == 0.067
        assert self.bill3.nonfuel_first_1000 == 0.07371
        assert self.bill4.nonfuel_first_1000 == 0.07371

    def test_nonfuel_over_1000(self):
        assert self.bill1.nonfuel_over_1000 == 0.07762
        assert self.bill2.nonfuel_over_1000 == 0.07762
        assert self.bill3.nonfuel_over_1000 == 0.08371
        assert self.bill4.nonfuel_over_1000 == 0.08371

    def test_fuel_first_1000(self):
        assert self.bill1.fuel_first_1000 == 0.02123
        assert self.bill2.fuel_first_1000 == 0.0251
        assert self.bill3.fuel_first_1000 == 0.03487
        assert self.bill4.fuel_first_1000 == 0.03487

    def test_fuel_over_1000(self):
        assert self.bill1.fuel_over_1000 == 0.03123
        assert self.bill2.fuel_over_1000 == 0.0351
        assert self.bill3.fuel_over_1000 == 0.04487
        assert self.bill4.fuel_over_1000 == 0.04487
