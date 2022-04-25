import datetime as dt

import pandas as pd
import pytest
import save_life_in_ua as sliu


@pytest.fixture
def df_in() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "datetime": [44671, 44671.5, 44672],
            "amount": [1, 2, 3],
            "type": ["A"] * 3,
            "source": ["B"] * 3,
        }
    )
    return df


def test_process_date(df_in: pd.DataFrame):
    df = sliu.process_date(df_in)
    assert "date" in df
    assert "datetime" not in df
    assert df["date"].apply(lambda x: isinstance(x, dt.date)).all()
