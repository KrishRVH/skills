## Pilot summary

Outputs: 36. Source documents scored: 18. Uncalibrated reference line = lowest strong-human source score = 0.928.

### Binoculars on sources (lower = more model-like)

| Source class | n   | mean  | median | min   | max   |
| ------------ | --- | ----- | ------ | ----- | ----- |
| ai           | 6   | 0.996 | 1.003  | 0.954 | 1.026 |
| human        | 6   | 0.979 | 0.980  | 0.928 | 1.022 |
| human_defect | 6   | 1.003 | 1.009  | 0.956 | 1.047 |

### Binoculars on outputs, paired with their sources

| Source class | Regime    | Budget | n   | source mean | output mean | mean delta | outputs lower than source | outputs below reference line (source below) |
| ------------ | --------- | ------ | --- | ----------- | ----------- | ---------- | ------------------------- | ------------------------------------------- |
| ai           | recompose | 0.15   | 6   | 0.996       | 1.002       | 0.0057     | 3                         | 0 (0)                                       |
| human        | preserve  | 0.15   | 6   | 0.979       | 0.968       | -0.0110    | 4                         | 2 (0)                                       |
| human_defect | preserve  | 0.05   | 6   | 1.003       | 0.985       | -0.0180    | 4                         | 1 (0)                                       |
| human_defect | preserve  | 0.15   | 6   | 1.003       | 0.990       | -0.0134    | 4                         | 0 (0)                                       |
| human_defect | preserve  | 0.3    | 6   | 1.003       | 0.977       | -0.0259    | 5                         | 1 (0)                                       |
| human_defect | recompose | 0.15   | 6   | 1.003       | 0.997       | -0.0059    | 3                         | 1 (0)                                       |

### Preserve clause-diff accounting

| Source class | Budget | n   | kept | edited | deleted | added | reordered | mean share | max share | within budget | violations |
| ------------ | ------ | --- | ---- | ------ | ------- | ----- | --------- | ---------- | --------- | ------------- | ---------- |
| human        | 0.15   | 6   | 99   | 11     | 2       | 0     | 0         | 0.015      | 0.032     | 6/6           | 0          |
| human_defect | 0.05   | 6   | 98   | 11     | 35      | 0     | 0         | 0.002      | 0.014     | 6/6           | 0          |
| human_defect | 0.15   | 6   | 105  | 7      | 32      | 0     | 0         | 0.002      | 0.009     | 6/6           | 0          |
| human_defect | 0.3    | 6   | 101  | 8      | 35      | 0     | 0         | 0.000      | 0.000     | 6/6           | 0          |

### Injected-defect repair on human_defect drafts

| Regime    | Budget | n   | generic opening | generic closing | filler phrase | -ing significance tail | empty adverb | all five |
| --------- | ------ | --- | --------------- | --------------- | ------------- | ---------------------- | ------------ | -------- |
| preserve  | 0.05   | 6   | 6/6             | 6/6             | 6/6           | 6/6                    | 6/6          | 6/6      |
| preserve  | 0.15   | 6   | 6/6             | 6/6             | 6/6           | 6/6                    | 6/6          | 6/6      |
| preserve  | 0.3    | 6   | 6/6             | 6/6             | 6/6           | 6/6                    | 6/6          | 6/6      |
| recompose | 0.15   | 6   | 6/6             | 6/6             | 6/6           | 6/6                    | 6/6          | 6/6      |

### Automated fidelity checks

| Source class | Regime    | Budget | n   | source numbers missing from output | outputs with a generated dash |
| ------------ | --------- | ------ | --- | ---------------------------------- | ----------------------------- |
| ai           | recompose | 0.15   | 6   | 0                                  | 0                             |
| human        | preserve  | 0.15   | 6   | 0                                  | 0                             |
| human_defect | preserve  | 0.05   | 6   | 0                                  | 0                             |
| human_defect | preserve  | 0.15   | 6   | 0                                  | 0                             |
| human_defect | preserve  | 0.3    | 6   | 0                                  | 0                             |
| human_defect | recompose | 0.15   | 6   | 0                                  | 0                             |

### Routing decisions

| Hidden class | Caller statement       | n   | preserve | recompose | ask | wrong guesses |
| ------------ | ---------------------- | --- | -------- | --------- | --- | ------------- |
| human        | says it is their draft | 6   | 6        | 0         | 0   | 0             |
| human_defect | none                   | 6   | 0        | 3         | 3   | 0             |
| ai           | none                   | 6   | 0        | 3         | 3   | 0             |

Wrong guesses: 0/18 (a wrong guess is Preserve without a caller statement, or anything but Preserve with one). Routing accuracy without a wrong guess: 1.000.
