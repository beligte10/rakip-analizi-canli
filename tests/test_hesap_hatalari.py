"""Ölçü formülü istisna verince değer None kalır ama artık günlüğe düşer (2026-11-05)."""
import datetime
import logging

import pipeline.compute as C


class _Ctx:
    def get_dates(self, banka):
        return [datetime.date(2026, 6, 30)]

    def has_period(self, banka, d):
        return True


def test_istisna_none_olur_ve_uyari_yazilir(caplog, monkeypatch):
    def bozuk(ctx, b, d):
        raise ZeroDivisionError('payda 0')
    monkeypatch.setattr(C, 'MEASURE_FUNCS', {'olcu_x': bozuk})
    monkeypatch.setattr(C, 'BASELINE_PASSTHROUGH', set())
    with caplog.at_level(logging.WARNING, logger='pipeline.compute'):
        out = C.compute_all(_Ctx(), {'olcu_x': {'Banka A': {}}}, [{'id': 'olcu_x'}], banks=['Banka A'])
    assert out['olcu_x']['Banka A']['2026-06-30'] is None            # değer değişmedi
    assert any('olcu_x' in r.getMessage() and 'ZeroDivisionError' in r.getMessage() for r in caplog.records)
