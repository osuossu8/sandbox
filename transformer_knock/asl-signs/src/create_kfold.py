import pandas as pd
from pydantic import BaseModel, Field
from sklearn.model_selection import StratifiedGroupKFold


class DataSplitter(BaseModel):
    seed: int = Field(default=42)
    n_splits: int = Field(default=5)
    shuffle: bool = Field(default=True)
    target_col: str | None = Field(default=None)
    group_col: str | None = Field(default=None)

    def split(self, df: pd.DataFrame) -> pd.DataFrame:
        df["kfold"] = -1
        kf = StratifiedGroupKFold(n_splits=self.n_splits, shuffle=self.shuffle, random_state=self.seed)
        for n, (_, val_index) in enumerate(kf.split(X=df, y=df[self.target_col], groups=df[self.group_col])):
            df.loc[val_index, "kfold"] = int(n)
        df["kfold"] = df["kfold"].astype(int)
        return df
