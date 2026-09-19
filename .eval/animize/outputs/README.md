# outputs

Drop agent-session results here as `*.jsonl`. Each row needs `job_id`
(from `jobs.jsonl`), `output_text`, `notes`, `regime_assigned`, and
`asked_question` (true or false). `run_animize.py merge` joins them to
their jobs and writes `outputs.jsonl` one level up.
