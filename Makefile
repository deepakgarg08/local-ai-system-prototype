.PHONY: confidence-calibration confidence-analysis telemetry-analysis cc

telemetry-analysis:
	python -m analysis.confidence_telemetry_analysis

confidence-analysis:
	python -m analysis.confidence_threshold_calibration

cc: confidence-calibration

confidence-calibration:
# 	python tools/check_llm_health.py
	@echo ">>> PART 1: running calibration questions"
	python -m evaluation.run_confidence_calibration_set
	@echo ">>> PART 2: analyzing telemetry"
	python -m analysis.confidence_telemetry_analysis
	@echo ">>> PART 3: calibrating thresholds"
	python -m analysis.confidence_threshold_calibration

test:
	pytest
	python -m tools.log_validation