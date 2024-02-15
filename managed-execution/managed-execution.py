from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/desertaxle/demo.git",
        entrypoint="flow.py:my_flow",
    ).deploy(
        name="test-managed-flow",
        work_pool_name="my-managed-pool",
        job_variables={"pip_packages": ["pandas", "prefect-aws"]},
    )
