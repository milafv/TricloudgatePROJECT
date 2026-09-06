import sys
sys.path.append("stage4_deployment")
from state_store_manager import StateStoreManager
def run_test():
    print("Creating StateStoreManager with a test run_id...")
    store = StateStoreManager(run_id="test_run_001")

    print("\nSaving mock stage2_ir_json data...")
    mock_ir = {"blueprint_id": "abc123", "nodes": [{"id": "web_server"}]}
    store.save_stage_output("stage2_ir_json", mock_ir)

    print("\nLoading it back...")
    loaded = store.load_stage_output("stage2_ir_json")
    print("Loaded data:", loaded)
    assert loaded == mock_ir, "Loaded data does not match what was saved!"

    print("\nChecking stage_completed for 'stage2_ir_json' (should be True)...")
    print(store.stage_completed("stage2_ir_json"))

    print("\nChecking stage_completed for 'stage3_mapped_spec' (should be False)...")
    print(store.stage_completed("stage3_mapped_spec"))

    print("\nTrying to load a stage that was never saved (should print None)...")
    print(store.load_stage_output("stage3_mapped_spec"))

    print("\nSaving a mock deployment log...")
    store.save_deployment_log({"success": True, "message": "Deployment successful"})

    print("\nGetting run summary...")
    summary = store.get_run_summary()
    print(summary)

    print("\nALL TESTS PASSED")


if __name__ == "__main__":
    run_test()