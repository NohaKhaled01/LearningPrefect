# Exercises - Notes and Codes

[Exercises 1 & 2 Notes: Creating an ETL, Making it Dynamic](<./Exercises 1 & 2 Creating an ETL, Making it Dynamic/Exercises 1 & 2 Creating an ETL, Making it Dynamic.md>)
[Exercises 1 & 2 Code: Exercise 1](<./Exercises 1 & 2 Creating an ETL, Making it Dynamic/ETL_Exercise1.py>)
[Exercises 1 & 2 Code: Exercise 2](<./Exercises 1 & 2 Creating an ETL, Making it Dynamic/ETL_Exercise2_dynamic.py>)

[Exercises 3 Notes: Running in Parallel](<./Exercise 3 - Running in Parallel/Exercise 3 - Running in Parallel.md>)
[Exercises 3 Code: Exercise 3](<./Exercise 3 - Running in Parallel/Exercise3_mapping.py>)
[Exercises 3 Code: Exercise 3.1](<./Exercise 3 - Running in Parallel/Exercise3_mapping_flowcontinue.py>)

### Comparison summary across all four exercises

| | Ex. 1 | Ex. 2 | Ex. 3 | **Ex.3.1** |
| :--- | :--- | :--- | :--- | :--- |
| **Concept** | Basic ETL | Parameterized ETL | Dynamic mapping / concurrency | Fault-tolerant mapping |
| **Key API** | `@task`, `@flow`, `deploy + cron` | Flow params | `.map()`, `.result()` | `.result(raise_on_failure=False)` |
| **Failure behavior** | Flow fails on task failure | Flow fails on task failure | Flow crashes on any mapped failure | Flow continues; failures captured in list |
| **Retries** | 3 | 3 | 3 | 1 |
| **Schedule** | Daily 06:00 | Daily 06:00 | None | None |
| **Bugs** | — | Param not wired into deployment | No `raise_for_status` | No `raise_for_status` + wrong entrypoint filename |