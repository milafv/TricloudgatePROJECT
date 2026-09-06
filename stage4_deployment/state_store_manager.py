import os
import json
from datetime import datetime
# this class manage the saving and loading pipeline stages
class StateStoreManager:
# the stages we except for now
    ALL_STAGES = [
        "stage1_parsed",
        "stage2_ir_json",
        "stage3_mapped_spec",
        "stage4_terraform_generated",
        "deployment_log",
        "stage5_consistency_report",
    ]

    def __init__(self, run_id=None):
        if run_id is None:
            run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.run_id = run_id
        self.run_folder = os.path.join("pipeline_state", self.run_id)


        os.makedirs(self.run_folder, exist_ok=True)

    def _stage_path(self, stage_name):
        return os.path.join(self.run_folder, f"{stage_name}.json")

    def save_stage_output(self, stage_name, data):
        path = self._stage_path(stage_name)
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"[StateStoreManager] Saved stage output: {path}")
            return True
        except (TypeError, OSError) as e:
            print(f"[StateStoreManager] ERROR saving {stage_name}: {e}")
            return False

    def load_stage_output(self, stage_name):
        path = self._stage_path(stage_name)
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[StateStoreManager] ERROR loading {stage_name}: {e}")
            return None

    def stage_completed(self, stage_name):
        return os.path.exists(self._stage_path(stage_name))

    def save_deployment_log(self, log_data):
        return self.save_stage_output("deployment_log", log_data)

    def get_run_summary(self):
        completed = [s for s in self.ALL_STAGES if self.stage_completed(s)]
        return {
            "run_id": self.run_id,
            "completed_stages": completed,
            "total_stages": len(self.ALL_STAGES),
        }