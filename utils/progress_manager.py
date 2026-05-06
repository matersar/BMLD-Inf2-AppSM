import pandas as pd
from utils.data_manager import DataManager


PROGRESS_COLUMNS = [
    "timestamp",
    "goal",
    "level",
    "training_days",
    "day_name",
    "completed",
]


class ProgressManager:
    def __init__(self):
        self.data_manager = DataManager(
            fs_protocol="webdav",
            fs_root_folder="Informatik_2_App"
        )

    def load_progress(self):
        return self.data_manager.load_user_data(
            "training_progress.csv",
            initial_value=pd.DataFrame(columns=PROGRESS_COLUMNS),
            parse_dates=["timestamp"],
        )

    def save_progress(self, progress_df):
        self.data_manager.save_user_data(
            progress_df,
            "training_progress.csv"
        )

    def update_day(self, goal, level, training_days, day_name, completed):
        progress_df = self.load_progress()

        new_record = {
            "goal": goal,
            "level": level,
            "training_days": training_days,
            "day_name": day_name,
            "completed": completed,
        }

        progress_df = self.data_manager.append_record(progress_df, new_record)
        self.save_progress(progress_df)

    def get_latest_status(self, goal, level, training_days, day_name):
        progress_df = self.load_progress()

        if progress_df.empty:
            return False

        filtered = progress_df[
            (progress_df["goal"] == goal) &
            (progress_df["level"] == level) &
            (progress_df["training_days"] == training_days) &
            (progress_df["day_name"] == day_name)
        ]

        if filtered.empty:
            return False

        return bool(filtered.iloc[-1]["completed"])